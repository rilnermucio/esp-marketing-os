#!/usr/bin/env python3
"""
metrics_collector.py — Normaliza métricas de conteúdo para o loop /aprender.

Lê JSON (arquivo ou stdin), ranqueia por métrica primária e emite resumo markdown
com top/bottom e candidatos a aprendizado. Stdlib pura, zero rede.

Uso:
    python3 scripts/metrics_collector.py --input reels.json --metrica retention \\
        --min-amostra 5
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

IDENTIFIER_KEYS = ("id", "titulo", "title", "name")
DEVIATION_THRESHOLD = 0.30


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _load_items(raw: str) -> list[dict[str, Any]]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _log(f"ERRO: JSON inválido ({exc})")
        raise ValueError("invalid json") from exc

    if not isinstance(data, list):
        _log("ERRO: entrada deve ser uma lista JSON de objetos")
        raise ValueError("not a list")

    if not data:
        _log("ERRO: lista vazia")
        raise ValueError("empty list")

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            _log(f"ERRO: item {i} não é um objeto")
            raise ValueError("item not dict")

    return data


def _identifier(item: dict[str, Any]) -> str | None:
    for key in IDENTIFIER_KEYS:
        val = item.get(key)
        if val is not None and str(val).strip():
            return str(val).strip()
    return None


def _metric_value(item: dict[str, Any], metric: str) -> float | None:
    if metric not in item:
        return None
    val = item[metric]
    if isinstance(val, bool) or val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _delta_pct(value: float, mean: float) -> float | None:
    if mean == 0:
        return None
    return ((value - mean) / mean) * 100.0


def _format_delta(delta: float | None) -> str:
    if delta is None:
        return "n/a"
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}%"


def summarize(
    items: list[dict[str, Any]],
    metric: str,
    min_sample: int = 5,
) -> str:
    """Gera resumo markdown. Levanta ValueError se amostra insuficiente ou métrica ausente."""
    scored: list[tuple[str, float]] = []
    missing_id = 0

    for item in items:
        ident = _identifier(item)
        if ident is None:
            missing_id += 1
            continue
        val = _metric_value(item, metric)
        if val is None:
            continue
        scored.append((ident, val))

    if missing_id:
        _log(f"AVISO: {missing_id} item(ns) sem identificador ignorado(s)")

    if not scored:
        _log(f"ERRO: nenhum item com métrica '{metric}'")
        raise ValueError("no metric values")

    if len(scored) < min_sample:
        _log(
            f"amostra insuficiente pra aprendizado: {len(scored)} itens com "
            f"'{metric}' (mínimo {min_sample})"
        )
        raise ValueError("insufficient sample")

    values = [v for _, v in scored]
    mean = sum(values) / len(values)

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    top3 = ranked[:3]
    bottom3 = (
        list(reversed(ranked[-3:])) if len(ranked) >= 3 else list(reversed(ranked))
    )

    candidates: list[tuple[str, float, float | None]] = []
    for ident, val in scored:
        delta = _delta_pct(val, mean)
        if delta is not None and abs(delta) / 100.0 > DEVIATION_THRESHOLD:
            candidates.append((ident, val, delta))
    candidates.sort(key=lambda x: abs(x[2] or 0), reverse=True)

    lines = [
        f"# Resumo de métricas: {metric}",
        "",
        f"- Itens analisados: {len(scored)}",
        f"- Média de {metric}: {mean:.4g}",
        "",
        "## Top 3",
    ]
    for ident, val in top3:
        lines.append(
            f"- **{ident}**: {val:.4g} ({_format_delta(_delta_pct(val, mean))} vs média)"
        )

    lines.append("")
    lines.append("## Bottom 3")
    for ident, val in bottom3:
        lines.append(
            f"- **{ident}**: {val:.4g} ({_format_delta(_delta_pct(val, mean))} vs média)"
        )

    lines.append("")
    lines.append("## Candidatos a aprendizado (>30% vs média)")
    if candidates:
        for ident, val, delta in candidates:
            lines.append(f"- **{ident}**: {val:.4g} ({_format_delta(delta)} vs média)")
    else:
        lines.append("- (nenhum desvio acima de 30%)")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normaliza métricas de conteúdo para o loop /aprender",
    )
    parser.add_argument(
        "--input",
        default="-",
        help="Arquivo JSON de entrada ou '-' para stdin (default: stdin)",
    )
    parser.add_argument(
        "--metrica",
        required=True,
        help="Nome da métrica primária de ranqueamento (ex: retention, ctr, views)",
    )
    parser.add_argument(
        "--min-amostra",
        type=int,
        default=5,
        help="Mínimo de itens com a métrica (default: 5)",
    )
    args = parser.parse_args()

    if args.min_amostra < 1:
        _log("ERRO: --min-amostra deve ser >= 1")
        return 1

    try:
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            with open(args.input, encoding="utf-8") as fh:
                raw = fh.read()
        items = _load_items(raw)
        report = summarize(items, args.metrica, args.min_amostra)
    except (ValueError, OSError) as exc:
        if isinstance(exc, OSError):
            _log(f"ERRO: não foi possível ler '{args.input}' ({exc})")
        return 1

    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
