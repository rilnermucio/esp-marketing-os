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
