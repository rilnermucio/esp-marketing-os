#!/usr/bin/env python3
"""
Apify Google SERP Scraper — opcional, requer APIFY_TOKEN.

Despacha o Actor apify/google-search-scraper para extrair top results,
PAA (people also ask) e related searches de uma query no Google.

Output:
- JSON em workspace/research/apify/<timestamp>-<slug>.json
- summary_md em stdout (consumível pelo mos-seo)

Sem APIFY_TOKEN: exit 0 com mensagem em stderr (agent decide fallback).
Com erro Apify (401, 429, timeout): exit 2 com mensagem em stderr.

Uso:
    python apify_serp.py --query "infoproduto bofu" --max-results 10
    python apify_serp.py --query "x" --dry-run
    python apify_serp.py --query "x" --format json
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

SERP_ACTOR_ID = "apify/google-search-scraper"
DEFAULT_OUTPUT_DIR = "workspace/research/apify"
DEFAULT_MAX_RESULTS = 10
HARD_CAP_RESULTS = 100
DEFAULT_TIMEOUT = 90


def build_input(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> Dict[str, Any]:
    """
    Constrói input do Actor apify/google-search-scraper para PT-BR.

    O Actor aceita 'queries' como string (queries separadas por newline pra batch).
    Pra uma query única, passamos a string direto.
    """
    capped = max(1, min(max_results, HARD_CAP_RESULTS))
    return {
        "queries": query,
        "resultsPerPage": capped,
        "maxPagesPerQuery": 1,
        "countryCode": "br",
        "languageCode": "pt-BR",
        "saveHtml": False,
        "mobileResults": False,
    }


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    """Remove duplicatas preservando a ordem da primeira ocorrência."""
    seen = set()
    out = []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def parse_serp_results(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extrai estrutura limpa do output do Actor.

    O Actor retorna lista de "search results" (um por query). Pegamos o primeiro.
    PAA e related vêm duplicados do Actor (top + footer da SERP) — dedupa.
    """
    empty = {"organic": [], "people_also_ask": [], "related": []}
    if not raw or not isinstance(raw, list):
        return empty

    first = raw[0] if isinstance(raw[0], dict) else {}
    organic_raw = first.get("organicResults") or []
    organic = [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "position": idx + 1,
        }
        for idx, item in enumerate(organic_raw)
    ]

    paa_raw = first.get("peopleAlsoAsk") or []
    paa = [q.get("question", "") for q in paa_raw]

    related_raw = first.get("relatedQueries") or []
    related = [r.get("title", "") for r in related_raw]

    return {
        "organic": organic,
        "people_also_ask": _dedupe_preserve_order(paa),
        "related": _dedupe_preserve_order(related),
    }


def format_summary_md(parsed: Dict[str, Any], query: str) -> str:
    """Formata resultado em Markdown para consumo do agent."""
    lines = [f"## SERP: {query}", ""]

    if parsed.get("organic"):
        lines.append("### Top resultados")
        for r in parsed["organic"]:
            lines.append(f"{r['position']}. **{r['title']}** — {r['url']}")
            if r.get("description"):
                lines.append(f"   {r['description']}")
        lines.append("")

    if parsed.get("people_also_ask"):
        lines.append("### People Also Ask")
        for q in parsed["people_also_ask"]:
            lines.append(f"- {q}")
        lines.append("")

    if parsed.get("related"):
        lines.append("### Related searches")
        for r in parsed["related"]:
            lines.append(f"- {r}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apify_serp.py",
        description="Google SERP scraper via Apify (opcional, requer APIFY_TOKEN)",
    )
    parser.add_argument(
        "--query", "-q", required=True, help="Termo de pesquisa no Google"
    )
    parser.add_argument(
        "--max-results",
        "-n",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Máximo de resultados orgânicos (default: {DEFAULT_MAX_RESULTS}, cap: {HARD_CAP_RESULTS})",
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

    actor_input = build_input(args.query, args.max_results)
    cost = estimate_cost(SERP_ACTOR_ID, actor_input)

    if args.dry_run:
        print(f"Dry-run: SERP scraping de '{args.query}'")
        print(f"  Actor: {SERP_ACTOR_ID}")
        print(f"  Results per page: {actor_input['resultsPerPage']}")
        print(
            f"  Country/Lang: {actor_input['countryCode']}/{actor_input['languageCode']}"
        )
        print(f"  Custo estimado: ${cost:.4f} USD")
        return 0

    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"{ENV_TOKEN} não configurado. Pulando SERP scraping. "
            f"Use WebSearch como fallback.",
            file=sys.stderr,
        )
        return 0  # Graceful degrade

    try:
        raw = run_actor_sync(
            SERP_ACTOR_ID, actor_input, token=token, timeout=args.timeout
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

    parsed = parse_serp_results(raw)
    summary_md = format_summary_md(parsed, args.query)

    output = {
        "source": SERP_ACTOR_ID,
        "query": args.query,
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
