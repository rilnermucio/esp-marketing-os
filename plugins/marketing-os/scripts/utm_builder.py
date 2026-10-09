#!/usr/bin/env python3
"""Monta links com UTM e um piece_id estável para cada peça.

O /aprender casava métrica com peça por título ou por tipo de peça, então a
atribuição era aproximada (docs/ROADMAP.md, Fase 4). Gerar o link junto com a
peça, com um piece_id no utm_content, faz o export de métricas (GA4, Meta,
encurtadores) carregar o identificador exato que o metrics_collector usa.

Uso:
    python3 scripts/utm_builder.py --url https://site.com/curso \\
        --source instagram --medium social --campaign lancamento-outubro \\
        --content reels-hook-a
    python3 scripts/utm_builder.py --url https://site.com --source meta \\
        --medium paid --campaign black-friday --piece-id auto --json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

UTM_KEYS = ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term")


def slug(value: str) -> str:
    """Minúsculas, sem acento, espaço vira hífen: valor seguro para UTM."""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return normalized


def make_piece_id(campaign: str, content: str, day: date) -> str:
    """Identificador curto e estável da peça: campanha, conteúdo, data e hash."""
    base = f"{slug(campaign)}-{slug(content) or 'peca'}-{day:%Y%m%d}"
    digest = hashlib.sha1(base.encode()).hexdigest()[:6]
    return f"{base}-{digest}"


def build_url(
    url: str,
    source: str,
    medium: str,
    campaign: str,
    content: str = "",
    term: str = "",
    piece_id: str = "",
) -> dict:
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ValueError(f"URL inválida (use http ou https): {url}")
    utm = {
        "utm_source": slug(source),
        "utm_medium": slug(medium),
        "utm_campaign": slug(campaign),
        "utm_content": slug(content) if content else piece_id,
        "utm_term": slug(term),
    }
    if not (utm["utm_source"] and utm["utm_medium"] and utm["utm_campaign"]):
        raise ValueError(
            "source, medium e campaign são obrigatórios e não podem ficar vazios"
        )
    kept = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if k not in UTM_KEYS
    ]
    query = kept + [(k, v) for k, v in utm.items() if v]
    final = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)
    )
    return {"url": final, "piece_id": piece_id, **{k: v for k, v in utm.items() if v}}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", required=True, help="URL de destino (http ou https)")
    parser.add_argument(
        "--source", required=True, help="Origem: instagram, meta, google, email..."
    )
    parser.add_argument(
        "--medium", required=True, help="Meio: social, paid, email, cpc..."
    )
    parser.add_argument("--campaign", required=True, help="Nome da campanha")
    parser.add_argument(
        "--content", default="", help="Variação da peça (vira utm_content)"
    )
    parser.add_argument("--term", default="", help="Palavra-chave paga (utm_term)")
    parser.add_argument(
        "--piece-id",
        default="",
        help="Identificador da peça; 'auto' gera um estável. Vai no utm_content se --content faltar",
    )
    parser.add_argument(
        "--data", default="", help="Data da peça AAAA-MM-DD (padrão: hoje)"
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    day = date.fromisoformat(args.data) if args.data else date.today()
    piece_id = args.piece_id
    if piece_id == "auto":
        piece_id = make_piece_id(args.campaign, args.content, day)
    try:
        result = build_url(
            args.url,
            args.source,
            args.medium,
            args.campaign,
            args.content,
            args.term,
            piece_id,
        )
    except ValueError as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["url"])
        if piece_id:
            print(f"piece_id: {piece_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
