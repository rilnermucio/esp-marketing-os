"""Scoring rubrics + weighted math for /auditoria.

Inputs: type-specific dimension scores (0-100 or None for "N/D"),
evidences, fixes. Output: overall + sorted top wins/fixes + formatted markdown.

CLI: reads JSON from stdin, writes JSON to stdout.
"""
from __future__ import annotations

import json
import sys


RUBRICS: dict[str, dict[str, int]] = {
    "landing": {
        "Conversão (CTA, friction, funil)": 25,
        "Copy (headline, value prop)": 20,
        "SEO (technical + content)": 15,
        "Trust signals": 10,
        "Design (hierarquia visual)": 10,
        "Brand (consistência, voice)": 10,
        "Diferenciação competitiva": 10,
    },
    "instagram": {
        "Bio + posicionamento": 20,
        "Consistência visual": 20,
        "Hooks últimos posts": 20,
        "Strategy/CTA": 15,
        "Engagement ratio": 15,
        "Cadência/frequência": 10,
    },
    "meta_ads": {
        "Hook do criativo (3s)": 25,
        "Copy (clarity + benefit)": 25,
        "Visual (composição)": 20,
        "CTA + landing match": 15,
        "Diferenciação vs concorrente": 15,
    },
    "youtube": {
        "Hook (30s)": 25,
        "Retention/pacing": 25,
        "Thumbnail + título": 20,
        "Estrutura narrativa": 15,
        "CTA/conversão": 15,
    },
}


def validate_rubrics() -> None:
    """Raise if any rubric does not sum to 100."""
    for audit_type, rubric in RUBRICS.items():
        total = sum(rubric.values())
        if total != 100:
            raise ValueError(
                f"Rubric {audit_type!r} sums to {total}, expected 100"
            )


# Validate at import time so misconfigured rubric fails fast.
validate_rubrics()


def compute(
    audit_type: str,
    dimension_scores: dict[str, int | None],
    evidences: dict[str, str],
    fixes: dict[str, dict],
) -> dict:
    """Compute overall + sort wins/fixes. Returns serializable dict."""
    if audit_type not in RUBRICS:
        raise ValueError(f"tipo desconhecido: {audit_type!r}")

    rubric = RUBRICS[audit_type]

    missing = set(rubric.keys()) - set(dimension_scores.keys())
    if missing:
        raise ValueError(f"dimensão ausente: {sorted(missing)!r}")

    for dim, score in dimension_scores.items():
        if score is None:
            continue
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError(f"score fora de 0-100 em {dim!r}: {score}")

    scored = [(d, s, rubric[d]) for d, s in dimension_scores.items() if s is not None]
    if not scored:
        raise ValueError("todas as dimensões são N/D, auditoria sem score possível")

    weight_sum = sum(w for _, _, w in scored)
    weighted_total = sum(s * w for _, s, w in scored)
    overall = round(weighted_total / weight_sum)
    partial = len(scored) < len(rubric)

    dimensions = {
        dim: {
            "score": dimension_scores[dim],
            "weight": rubric[dim],
            "evidence": evidences.get(dim, ""),
            "fix": fixes.get(dim, {"text": "", "priority": "baixa"}),
        }
        for dim in rubric
    }

    return {
        "overall": overall,
        "partial": partial,
        "dimensions": dimensions,
        "type": audit_type,
    }
