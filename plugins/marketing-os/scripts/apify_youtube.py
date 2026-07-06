#!/usr/bin/env python3
"""
Apify YouTube Channel Scraper — opcional, requer APIFY_TOKEN.

Despacha o Actor streamers/youtube-scraper para extrair vídeos recentes
de um canal do YouTube com métricas (views, likes, comments).
Usado pelo mos-video, mos-research, mos-seo.

Uso:
    python apify_youtube.py --channel @mrbeast
    python apify_youtube.py --channel https://youtube.com/@aliabdaal --max-videos 30
    python apify_youtube.py --channel @x --dry-run
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

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

YOUTUBE_ACTOR_ID = "streamers/youtube-scraper"
DEFAULT_OUTPUT_DIR = "workspace/research/apify"
DEFAULT_MAX_VIDEOS = 20
HARD_CAP_VIDEOS = 100
DEFAULT_TIMEOUT = 240  # YT scraping é lento


def build_channel_url(raw: str) -> str:
    """
    Constrói URL canônica de canal do YouTube terminando em /videos.

    Aceita:
      - @handle
      - handle (assume @)
      - URL completa (channel/, /c/, /user/, /@handle)
    """
    if not raw:
        return ""
    s = raw.strip()

    # URL completa
    if s.startswith("http"):
        # Garante /videos no final pra capturar a aba de vídeos
        s = s.rstrip("/")
        if "/videos" not in s and "/playlists" not in s:
            return f"{s}/videos"
        return s

    # Handle puro
    handle = s.lstrip("@")
    return f"https://www.youtube.com/@{handle}/videos"


def build_input(channel: str, max_videos: int = DEFAULT_MAX_VIDEOS) -> Dict[str, Any]:
    """Constrói input do Actor streamers/youtube-scraper."""
    capped = max(1, min(max_videos, HARD_CAP_VIDEOS))
    url = build_channel_url(channel)
    return {
        "startUrls": [{"url": url}],
        "maxResults": capped,
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
    }


def parse_youtube_results(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extrai vídeos, canal e métricas agregadas."""
    if not raw:
        return {
            "videos": [],
            "channel": {},
            "metrics": {
                "total_videos": 0,
                "avg_views": 0,
                "avg_likes": 0,
                "avg_comments": 0,
            },
        }

    videos = []
    channel_name = ""
    channel_url = ""

    for item in raw:
        if not isinstance(item, dict):
            continue

        video = {
            "id": str(item.get("id", "")),
            "title": item.get("title", "") or "",
            "url": item.get("url", "") or "",
            "views": int(item.get("viewCount") or 0),
            "likes": int(item.get("likes") or 0),
            "comments": int(item.get("commentsCount") or 0),
            "duration": item.get("duration", "") or "",
            "date": item.get("date", "") or "",
        }
        videos.append(video)

        if not channel_name:
            channel_name = item.get("channelName") or ""
        if not channel_url:
            channel_url = item.get("channelUrl") or ""

    total = len(videos)
    if total > 0:
        avg_views = sum(v["views"] for v in videos) // total
        avg_likes = sum(v["likes"] for v in videos) // total
        avg_comments = sum(v["comments"] for v in videos) // total
    else:
        avg_views = avg_likes = avg_comments = 0

    return {
        "videos": videos,
        "channel": {
            "name": channel_name,
            "url": channel_url,
        },
        "metrics": {
            "total_videos": total,
            "avg_views": avg_views,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
        },
    }


def format_summary_md(parsed: Dict[str, Any], target: str) -> str:
    """Formata resultado em Markdown."""
    channel = parsed.get("channel", {})
    metrics = parsed.get("metrics", {})
    videos = parsed.get("videos", [])

    title = channel.get("name") or target

    lines = [f"## YouTube: {title}"]
    if channel.get("url"):
        lines.append(channel["url"])
    lines.append("")

    lines.append("### Métricas agregadas")
    lines.append(f"- Vídeos analisados: **{metrics.get('total_videos', 0)}**")
    lines.append(f"- Média de views: **{metrics.get('avg_views', 0):,}**")
    lines.append(f"- Média de likes: **{metrics.get('avg_likes', 0):,}**")
    lines.append(f"- Média de comments: **{metrics.get('avg_comments', 0):,}**")
    lines.append("")

    if videos:
        top = sorted(videos, key=lambda v: v.get("views", 0), reverse=True)[:5]
        lines.append("### Top 5 vídeos por views")
        for v in top:
            duration = v.get("duration", "")
            duration_str = f" [{duration}]" if duration else ""
            lines.append(f"- **{v.get('title', '?')}**{duration_str}")
            lines.append(
                f"  {v['views']:,} views, {v['likes']:,} likes, "
                f"{v['comments']:,} comments"
            )
            if v.get("url"):
                lines.append(f"  {v['url']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apify_youtube.py",
        description="YouTube channel scraper via Apify (opcional, requer APIFY_TOKEN)",
    )
    parser.add_argument(
        "--channel",
        "-c",
        required=True,
        help="Canal: @handle, handle, ou URL completa",
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

    if not args.channel.strip():
        print("Channel inválido ou vazio.", file=sys.stderr)
        return 1

    actor_input = build_input(args.channel, args.max_videos)
    cost = estimate_cost(YOUTUBE_ACTOR_ID, actor_input)

    if args.dry_run:
        print(f"Dry-run: YouTube scraping de '{args.channel}'")
        print(f"  Actor: {YOUTUBE_ACTOR_ID}")
        print(f"  Channel URL: {actor_input['startUrls'][0]['url']}")
        print(f"  Max videos: {actor_input['maxResults']}")
        print(f"  Custo estimado: ${cost:.4f} USD")
        return 0

    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"{ENV_TOKEN} não configurado. Pulando YouTube scraping. "
            f"Use mos-video com WebSearch como fallback.",
            file=sys.stderr,
        )
        return 0

    try:
        raw = run_actor_sync(
            YOUTUBE_ACTOR_ID, actor_input, token=token, timeout=args.timeout
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

    parsed = parse_youtube_results(raw)
    summary_md = format_summary_md(parsed, args.channel)

    output = {
        "source": YOUTUBE_ACTOR_ID,
        "channel": args.channel,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cost_estimate_usd": cost,
        "results": parsed,
        "summary_md": summary_md,
    }

    saved_path = save_result(
        output, slug=args.channel.lstrip("@"), output_dir=args.output_dir
    )
    print(f"# Saved: {saved_path}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(summary_md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
