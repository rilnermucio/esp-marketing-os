#!/usr/bin/env python3
"""
Apify Meta Ad Library Scraper — opcional, requer APIFY_TOKEN.

Despacha o Actor apify/facebook-ads-scraper para extrair anúncios ativos
e arquivados na Meta Ad Library (Facebook + Instagram) por keyword/marca.
Usado pelo mos-ads e mos-launch para inteligência de criativo competitivo.

Output:
- JSON em workspace/research/apify/<timestamp>-<slug>.json
- summary_md em stdout (consumível pelo mos-ads)

Sem APIFY_TOKEN: exit 0 com mensagem (agent decide fallback).
Erro Apify (401, 429, timeout): exit 2.

Uso:
    python apify_meta_ads.py --query "hotmart"
    python apify_meta_ads.py --query "infoproduto" --max-ads 50 --country BR
    python apify_meta_ads.py --query "x" --dry-run
"""

import argparse
import json
import os
import sys
import urllib.parse
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

META_ADS_ACTOR_ID = "curious_coder/facebook-ads-library-scraper"
DEFAULT_OUTPUT_DIR = "workspace/research/apify"
DEFAULT_MAX_ADS = 30
HARD_CAP_ADS = 100
MIN_ADS = 10  # Actor exige no mínimo 10 results pra rodar
DEFAULT_COUNTRY = "BR"
DEFAULT_TIMEOUT = 180  # Ad Library scraping é mais lento


def build_search_url(query: str, country: str = DEFAULT_COUNTRY) -> str:
    """
    Constrói URL de busca da Meta Ad Library.

    Formato canônico:
    https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BR&q={query}&search_type=keyword_unordered
    """
    params = {
        "active_status": "all",
        "ad_type": "all",
        "country": country,
        "q": query,
        "search_type": "keyword_unordered",
    }
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(params)


def build_input(
    query: str,
    max_ads: int = DEFAULT_MAX_ADS,
    country: str = DEFAULT_COUNTRY,
) -> Dict[str, Any]:
    """
    Constrói input do Actor curious_coder/facebook-ads-library-scraper.

    Actor exige count >= MIN_ADS (10) pra rodar. Se o usuário passar valor menor,
    elevamos pra MIN_ADS (custo idêntico, dado extra desperdiçado).
    """
    capped = max(MIN_ADS, min(max_ads, HARD_CAP_ADS))
    url = build_search_url(query, country=country)
    return {
        "urls": [{"url": url}],
        "count": capped,
    }


def _extract_body_text(snapshot: Dict[str, Any]) -> str:
    """
    Extrai texto do body. Pode ser dict {"text": "..."} ou string direto.
    Em ads dinâmicos, vem com placeholders {{product.brand}} — preserva como está.
    """
    body = snapshot.get("body")
    if isinstance(body, dict):
        return body.get("text", "") or ""
    if isinstance(body, str):
        return body
    return ""


def parse_meta_ads_results(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extrai anúncios e métricas agregadas do output do Actor.

    Campos vêm do Actor curious_coder/facebook-ads-library-scraper:
    - top-level: ad_archive_id, page_name, page_id, publisher_platform, is_active,
                 start_date, end_date_formatted
    - snapshot.{body.text, title, caption, cta_text, cta_type, link_url}
    """
    if not raw:
        return {
            "ads": [],
            "metrics": {"total_ads": 0, "unique_pages": 0},
            "top_pages": [],
        }

    ads: List[Dict[str, Any]] = []
    page_counter: Counter = Counter()

    for item in raw:
        if not isinstance(item, dict):
            continue

        snapshot = item.get("snapshot") or {}

        # Top-level fields (formato curious_coder)
        page_name = item.get("page_name") or snapshot.get("page_name") or ""
        platforms_raw = (
            item.get("publisher_platform")
            or item.get("publisher_platforms")
            or item.get("publisherPlatforms")
            or []
        )
        if isinstance(platforms_raw, str):
            platforms_raw = [platforms_raw]

        # Body/title/CTA do snapshot
        body = _extract_body_text(snapshot)
        title = snapshot.get("title") or ""
        if isinstance(title, dict):
            title = title.get("text", "") or ""
        caption = snapshot.get("caption") or ""
        cta_text = snapshot.get("cta_text") or ""
        link_url = snapshot.get("link_url") or ""

        # Fallback pra formato apify/facebook-ads-scraper (legacy)
        if not body:
            bodies = (
                item.get("ad_creative_bodies") or item.get("adCreativeBodies") or []
            )
            body = " | ".join(b for b in bodies if b)
        if not title:
            titles = (
                item.get("ad_creative_link_titles")
                or item.get("adCreativeLinkTitles")
                or []
            )
            title = " | ".join(t for t in titles if t)

        ad = {
            "id": (
                item.get("ad_archive_id")
                or item.get("adArchiveID")
                or item.get("ad_id")
                or item.get("id", "")
            ),
            "page_name": page_name,
            "page_id": item.get("page_id") or item.get("pageID") or "",
            "body": body,
            "title": title,
            "caption": caption,
            "cta_text": cta_text,
            "platforms": list(platforms_raw),
            "snapshot_url": (
                item.get("ad_snapshot_url")
                or item.get("ad_library_url")
                or item.get("adSnapshotURL")
                or ""
            ),
            "link_url": link_url,
            "start_date": (
                item.get("start_date")
                or item.get("start_date_formatted")
                or item.get("startDate")
                or ""
            ),
            "end_date": (
                item.get("end_date_formatted")
                or item.get("end_date")
                or item.get("endDate")
            ),
            "is_active": item.get("is_active"),
        }
        ads.append(ad)
        if page_name:
            page_counter[page_name] += 1

    top_pages: List[Tuple[str, int]] = page_counter.most_common(10)

    return {
        "ads": ads,
        "metrics": {
            "total_ads": len(ads),
            "unique_pages": len(page_counter),
        },
        "top_pages": top_pages,
    }


def format_summary_md(parsed: Dict[str, Any], query: str) -> str:
    """Formata resultado em Markdown para consumo do agent."""
    metrics = parsed.get("metrics", {})
    ads = parsed.get("ads", [])
    top_pages = parsed.get("top_pages", [])

    lines = [f"## Meta Ad Library: {query}", ""]

    lines.append("### Métricas agregadas")
    lines.append(f"- Anúncios encontrados: **{metrics.get('total_ads', 0)}**")
    lines.append(f"- Páginas únicas anunciando: **{metrics.get('unique_pages', 0)}**")
    lines.append("")

    if top_pages:
        lines.append("### Top páginas (por volume de anúncios)")
        for page, count in top_pages:
            lines.append(f"- **{page}** ({count} anúncios)")
        lines.append("")

    if ads:
        lines.append("### Amostra de criativos (até 5)")
        for ad in ads[:5]:
            page = ad.get("page_name", "?")
            platforms = ", ".join(ad.get("platforms") or []) or "?"
            title = ad.get("title", "")
            caption = ad.get("caption", "")
            body = (ad.get("body") or "").replace("\n", " ").strip()
            preview = body[:200] + ("..." if len(body) > 200 else "")
            cta = ad.get("cta_text", "")
            link = ad.get("link_url", "")

            lines.append(f"- **{page}** [{platforms}]")
            if title:
                lines.append(f"  Título: _{title}_")
            if caption:
                lines.append(f"  Caption: {caption}")
            if preview:
                lines.append(f"  > {preview}")
            if cta:
                lines.append(f"  CTA: **{cta}**")
            if link:
                lines.append(f"  Link: {link}")
            if ad.get("snapshot_url"):
                lines.append(f"  Library: {ad['snapshot_url']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apify_meta_ads.py",
        description="Meta Ad Library scraper via Apify (opcional, requer APIFY_TOKEN)",
    )
    parser.add_argument(
        "--query", "-q", required=True, help="Marca, palavra-chave ou termo de busca"
    )
    parser.add_argument(
        "--country",
        "-c",
        default=DEFAULT_COUNTRY,
        help=f"Código do país (default: {DEFAULT_COUNTRY})",
    )
    parser.add_argument(
        "--max-ads",
        "-n",
        type=int,
        default=DEFAULT_MAX_ADS,
        help=f"Máximo de anúncios (default: {DEFAULT_MAX_ADS}, cap: {HARD_CAP_ADS})",
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

    actor_input = build_input(args.query, max_ads=args.max_ads, country=args.country)
    cost = estimate_cost(META_ADS_ACTOR_ID, actor_input)

    if args.dry_run:
        print(f"Dry-run: Meta Ad Library de '{args.query}' (country={args.country})")
        print(f"  Actor: {META_ADS_ACTOR_ID}")
        print(f"  Max ads: {actor_input['count']}")
        print(f"  Search URL: {actor_input['urls'][0]['url']}")
        print(f"  Custo estimado: ${cost:.4f} USD")
        return 0

    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"{ENV_TOKEN} não configurado. Pulando Meta Ad Library scraping. "
            f"Use mos-ads sem dados externos como fallback.",
            file=sys.stderr,
        )
        return 0

    try:
        raw = run_actor_sync(
            META_ADS_ACTOR_ID, actor_input, token=token, timeout=args.timeout
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

    parsed = parse_meta_ads_results(raw)
    summary_md = format_summary_md(parsed, args.query)

    output = {
        "source": META_ADS_ACTOR_ID,
        "query": args.query,
        "country": args.country,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cost_estimate_usd": cost,
        "results": parsed,
        "summary_md": summary_md,
    }

    saved_path = save_result(output, slug=args.query, output_dir=args.output_dir)
    print(f"# Saved: {saved_path}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(summary_md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
