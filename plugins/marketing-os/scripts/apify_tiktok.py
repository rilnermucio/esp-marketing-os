#!/usr/bin/env python3
"""
Apify TikTok Profile Scraper — opcional, requer APIFY_TOKEN.

Despacha o Actor clockworks/tiktok-scraper para extrair vídeos recentes
de um perfil público no TikTok com métricas (plays, likes, comments, shares).
Usado pelo mos-research, mos-social e mos-video.

Uso:
    python apify_tiktok.py --handle @usuario
    python apify_tiktok.py --handle https://tiktok.com/@usuario --max-videos 50
    python apify_tiktok.py --handle @x --dry-run
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

TIKTOK_ACTOR_ID = "clockworks/free-tiktok-scraper"
DEFAULT_OUTPUT_DIR = "workspace/research/apify"
DEFAULT_MAX_VIDEOS = 30
HARD_CAP_VIDEOS = 100
DEFAULT_TIMEOUT = 180


def normalize_handle(raw: str) -> str:
    """Aceita @handle, handle, URL completa do TikTok. Retorna handle limpo."""
    if not raw:
        return ""
    s = raw.strip()
    m = re.match(
        r"https?://(www\.)?tiktok\.com/@([^/?#]+)",
        s,
        re.IGNORECASE,
    )
    if m:
        return m.group(2)
    if s.startswith("@"):
        return s[1:]
    return s


def build_input(handle: str, max_videos: int = DEFAULT_MAX_VIDEOS) -> Dict[str, Any]:
    """Constrói input do Actor clockworks/tiktok-scraper."""
    clean = normalize_handle(handle)
    capped = max(1, min(max_videos, HARD_CAP_VIDEOS))
    return {
        "profiles": [clean],
        "resultsPerPage": capped,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": False,
        "proxyCountryCode": "None",
    }


def parse_tiktok_results(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extrai vídeos, perfil e métricas agregadas + top hashtags."""
    if not raw:
        return {
            "videos": [],
            "profile": {},
            "metrics": {
                "total_videos": 0,
                "avg_plays": 0,
                "avg_likes": 0,
                "avg_comments": 0,
            },
            "top_hashtags": [],
        }

    videos = []
    all_hashtags: List[str] = []
    profile_handle = ""
    profile_nickname = ""

    for item in raw:
        if not isinstance(item, dict):
            continue

        author = item.get("authorMeta") or {}
        hashtag_list = [h.get("name", "") for h in (item.get("hashtags") or [])]
        hashtag_list = [h for h in hashtag_list if h]

        video = {
            "id": str(item.get("id", "")),
            "text": item.get("text") or "",
            "create_time": item.get("createTime") or item.get("createTimeISO") or "",
            "plays": int(item.get("playCount") or 0),
            "likes": int(item.get("diggCount") or 0),
            "comments": int(item.get("commentCount") or 0),
            "shares": int(item.get("shareCount") or 0),
            "url": item.get("webVideoUrl") or item.get("videoUrl") or "",
            "hashtags": hashtag_list,
        }
        videos.append(video)
        all_hashtags.extend(hashtag_list)

        if not profile_handle:
            profile_handle = author.get("name") or ""
        if not profile_nickname:
            profile_nickname = author.get("nickName") or ""

    total = len(videos)
    if total > 0:
        avg_plays = sum(v["plays"] for v in videos) // total
        avg_likes = sum(v["likes"] for v in videos) // total
        avg_comments = sum(v["comments"] for v in videos) // total
    else:
        avg_plays = avg_likes = avg_comments = 0

    top_hashtags: List[Tuple[str, int]] = Counter(all_hashtags).most_common(10)

    return {
        "videos": videos,
        "profile": {
            "handle": profile_handle,
            "nickname": profile_nickname,
        },
        "metrics": {
            "total_videos": total,
            "avg_plays": avg_plays,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
        },
        "top_hashtags": top_hashtags,
    }


def format_summary_md(parsed: Dict[str, Any], handle: str) -> str:
    """Formata resultado em Markdown."""
    profile = parsed.get("profile", {})
    metrics = parsed.get("metrics", {})
    videos = parsed.get("videos", [])
    top_hashtags = parsed.get("top_hashtags", [])

    title_handle = profile.get("handle") or handle
    nickname = profile.get("nickname", "")

    lines = [f"## TikTok: @{title_handle}"]
    if nickname:
        lines.append(f"_{nickname}_")
    lines.append("")

    lines.append("### Métricas agregadas")
    lines.append(f"- Vídeos analisados: **{metrics.get('total_videos', 0)}**")
    lines.append(f"- Média de plays: **{metrics.get('avg_plays', 0):,}**")
    lines.append(f"- Média de likes: **{metrics.get('avg_likes', 0):,}**")
    lines.append(f"- Média de comments: **{metrics.get('avg_comments', 0):,}**")
    lines.append("")

    if videos:
        top = sorted(videos, key=lambda v: v.get("plays", 0), reverse=True)[:5]
        lines.append("### Top 5 vídeos por plays")
        for v in top:
            text = (v.get("text") or "").replace("\n", " ").strip()
            preview = text[:100] + ("..." if len(text) > 100 else "")
            lines.append(
                f"- {v['plays']:,} plays, {v['likes']:,} likes, "
                f"{v['comments']:,} comments, {v['shares']:,} shares"
            )
            if preview:
                lines.append(f"  > {preview}")
            if v.get("url"):
                lines.append(f"  {v['url']}")
        lines.append("")

    if top_hashtags:
        lines.append("### Top hashtags")
        for tag, count in top_hashtags:
            lines.append(f"- #{tag} ({count})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apify_tiktok.py",
        description="TikTok profile scraper via Apify (opcional, requer APIFY_TOKEN)",
    )
    parser.add_argument(
        "--handle",
        "-u",
        required=True,
        help="Handle do TikTok (@user, user, ou URL)",
    )
    parser.add_argument(
        "--max-videos",
        "-n",
        type=int,
        default=DEFAULT_MAX_VIDEOS,
        help=f"Máximo de vídeos (default: {DEFAULT_MAX_VIDEOS}, cap: {HARD_CAP_VIDEOS})",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Diretório de saída (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Mostra estimativa de custo sem executar"
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

    actor_input = build_input(handle, args.max_videos)
    cost = estimate_cost(TIKTOK_ACTOR_ID, actor_input)

    if args.dry_run:
        print(f"Dry-run: TikTok scraping de @{handle}")
        print(f"  Actor: {TIKTOK_ACTOR_ID}")
        print(f"  Max videos: {actor_input['resultsPerPage']}")
        print(f"  Custo estimado: ${cost:.4f} USD")
        return 0

    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"{ENV_TOKEN} não configurado. Pulando TikTok scraping. "
            f"Use scripts/tiktok_trends_scraper.py como fallback (lib local).",
            file=sys.stderr,
        )
        return 0

    try:
        raw = run_actor_sync(
            TIKTOK_ACTOR_ID, actor_input, token=token, timeout=args.timeout
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

    parsed = parse_tiktok_results(raw)
    summary_md = format_summary_md(parsed, handle)

    output = {
        "source": TIKTOK_ACTOR_ID,
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
