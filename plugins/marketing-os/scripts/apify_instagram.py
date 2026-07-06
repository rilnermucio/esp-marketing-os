#!/usr/bin/env python3
"""
Apify Instagram Profile Scraper — opcional, requer APIFY_TOKEN.

Despacha o Actor apify/instagram-scraper para extrair posts e métricas
agregadas de um perfil público do Instagram. Usado pelo mos-research
e /analisar-concorrencia para inteligência competitiva.

Output:
- JSON em workspace/research/apify/<timestamp>-<slug>.json
- summary_md em stdout (consumível pelo mos-research)

Sem APIFY_TOKEN: exit 0 com mensagem (agent decide fallback).
Erro Apify (401, 429, timeout): exit 2.

Uso:
    python apify_instagram.py --handle @conrado
    python apify_instagram.py --handle conrado --max-posts 50
    python apify_instagram.py --handle https://instagram.com/x --dry-run
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from apify_client import (
    ENV_TOKEN,
    ApifyAPIError,
    ApifyAuthError,
    ApifyRateLimitError,
    ApifyTimeoutError,
    estimate_cost,
    run_actor_sync,
    save_result,
)

INSTAGRAM_ACTOR_ID = "apify/instagram-scraper"
DEFAULT_OUTPUT_DIR = "workspace/research/apify"
DEFAULT_MAX_POSTS = 30
HARD_CAP_POSTS = 100
DEFAULT_TIMEOUT = 120  # IG scraping mais lento que SERP


def normalize_handle(raw: str) -> str:
    """
    Aceita @handle, handle, URL completa do Instagram. Retorna handle limpo.

    Exemplos:
        @conrado -> conrado
        https://www.instagram.com/conrado/?hl=pt -> conrado
    """
    if not raw:
        return ""
    s = raw.strip()
    # URL do Instagram
    m = re.match(
        r"https?://(www\.)?instagram\.com/([^/?#]+)",
        s,
        re.IGNORECASE,
    )
    if m:
        return m.group(2)
    # @handle
    if s.startswith("@"):
        return s[1:]
    return s


def build_input(handle: str, max_posts: int = DEFAULT_MAX_POSTS) -> Dict[str, Any]:
    """Constrói input do Actor apify/instagram-scraper."""
    clean = normalize_handle(handle)
    capped = max(1, min(max_posts, HARD_CAP_POSTS))
    return {
        "directUrls": [f"https://www.instagram.com/{clean}/"],
        "resultsType": "posts",
        "resultsLimit": capped,
        "addParentData": False,
        "searchType": "user",
    }


def parse_instagram_results(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extrai posts, perfil e métricas agregadas do output do Actor.

    O Actor retorna lista de posts. Cada post tem ownerUsername e ownerFullName
    que usamos para preencher o perfil.
    """
    if not raw:
        return {
            "posts": [],
            "profile": {},
            "metrics": {"total_posts": 0, "avg_likes": 0, "avg_comments": 0},
            "top_hashtags": [],
        }

    posts = []
    all_hashtags: List[str] = []
    profile_handle = ""
    profile_name = ""

    for item in raw:
        if not isinstance(item, dict):
            continue

        post = {
            "id": item.get("id", ""),
            "type": item.get("type", ""),
            "caption": item.get("caption", "") or "",
            "likes": int(item.get("likesCount") or 0),
            "comments": int(item.get("commentsCount") or 0),
            "timestamp": item.get("timestamp", "") or "",
            "hashtags": item.get("hashtags", []) or [],
            "url": item.get("url", "") or "",
        }
        if "videoViewCount" in item and item["videoViewCount"]:
            post["video_views"] = int(item["videoViewCount"])

        posts.append(post)
        all_hashtags.extend(post["hashtags"])

        if not profile_handle and item.get("ownerUsername"):
            profile_handle = item["ownerUsername"]
        if not profile_name and item.get("ownerFullName"):
            profile_name = item["ownerFullName"]

    total = len(posts)
    if total > 0:
        avg_likes = sum(p["likes"] for p in posts) // total
        avg_comments = sum(p["comments"] for p in posts) // total
    else:
        avg_likes = 0
        avg_comments = 0

    top_hashtags: List[Tuple[str, int]] = Counter(all_hashtags).most_common(10)

    return {
        "posts": posts,
        "profile": {
            "handle": profile_handle,
            "full_name": profile_name,
        },
        "metrics": {
            "total_posts": total,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
        },
        "top_hashtags": top_hashtags,
    }


def format_summary_md(parsed: Dict[str, Any], handle: str) -> str:
    """Formata resultado em Markdown para consumo do agent."""
    profile = parsed.get("profile", {})
    metrics = parsed.get("metrics", {})
    posts = parsed.get("posts", [])
    top_hashtags = parsed.get("top_hashtags", [])

    title_handle = profile.get("handle") or handle
    full_name = profile.get("full_name", "")

    lines = [f"## Instagram: @{title_handle}"]
    if full_name:
        lines.append(f"_{full_name}_")
    lines.append("")

    lines.append("### Métricas agregadas")
    lines.append(f"- Posts analisados: **{metrics.get('total_posts', 0)}**")
    lines.append(f"- Média de likes: **{metrics.get('avg_likes', 0):,}**")
    lines.append(f"- Média de comments: **{metrics.get('avg_comments', 0):,}**")
    lines.append("")

    if posts:
        # Top 5 posts por likes
        top_posts = sorted(posts, key=lambda p: p.get("likes", 0), reverse=True)[:5]
        lines.append("### Top 5 posts por engajamento")
        for p in top_posts:
            caption = (p.get("caption") or "").replace("\n", " ").strip()
            preview = caption[:80] + ("..." if len(caption) > 80 else "")
            views = f", {p.get('video_views', 0):,} views" if "video_views" in p else ""
            lines.append(
                f"- [{p.get('type', '?')}] {p['likes']:,} likes, "
                f"{p['comments']:,} comments{views}"
            )
            if preview:
                lines.append(f"  > {preview}")
            if p.get("url"):
                lines.append(f"  {p['url']}")
        lines.append("")

    if top_hashtags:
        lines.append("### Top hashtags")
        for tag, count in top_hashtags:
            lines.append(f"- #{tag} ({count})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apify_instagram.py",
        description="Instagram profile scraper via Apify (opcional, requer APIFY_TOKEN)",
    )
    parser.add_argument(
        "--handle",
        "-u",
        required=True,
        help="Handle do Instagram (@user, user, ou URL completa)",
    )
    parser.add_argument(
        "--max-posts",
        "-n",
        type=int,
        default=DEFAULT_MAX_POSTS,
        help=f"Máximo de posts a coletar (default: {DEFAULT_MAX_POSTS}, cap: {HARD_CAP_POSTS})",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Diretório de saída (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra estimativa de custo sem executar",
    )
    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Formato do stdout (default: md)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout em segundos (default: {DEFAULT_TIMEOUT})",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    handle = normalize_handle(args.handle)
    if not handle:
        print("Handle inválido ou vazio.", file=sys.stderr)
        return 1

    actor_input = build_input(handle, args.max_posts)
    cost = estimate_cost(INSTAGRAM_ACTOR_ID, actor_input)

    if args.dry_run:
        print(f"Dry-run: Instagram scraping de @{handle}")
        print(f"  Actor: {INSTAGRAM_ACTOR_ID}")
        print(f"  Posts limit: {actor_input['resultsLimit']}")
        print(f"  Custo estimado: ${cost:.4f} USD")
        return 0

    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"{ENV_TOKEN} não configurado. Pulando Instagram scraping. "
            f"Use mos-research com WebSearch como fallback.",
            file=sys.stderr,
        )
        return 0  # Graceful degrade

    try:
        raw = run_actor_sync(
            INSTAGRAM_ACTOR_ID, actor_input, token=token, timeout=args.timeout
        )
    except ApifyAuthError as e:
        print(f"Erro de autenticação Apify: {e}", file=sys.stderr)
        return 2
    except ApifyRateLimitError as e:
        print(f"Rate limit Apify: {e}", file=sys.stderr)
        return 2
    except ApifyTimeoutError as e:
        print(f"Timeout Apify: {e}", file=sys.stderr)
        return 2
    except ApifyAPIError as e:
        print(f"Erro Apify: {e}", file=sys.stderr)
        return 2

    parsed = parse_instagram_results(raw)
    summary_md = format_summary_md(parsed, handle)

    output = {
        "source": INSTAGRAM_ACTOR_ID,
        "handle": handle,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cost_estimate_usd": cost,
        "results": parsed,
        "summary_md": summary_md,
    }

    saved_path = save_result(output, slug=handle, output_dir=args.output_dir)
    print(f"# Saved: {saved_path}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(summary_md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
