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
            raise ValueError(f"Rubric {audit_type!r} sums to {total}, expected 100")


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

    for dim, fix_dict in fixes.items():
        prio = fix_dict.get("priority", "baixa")
        if prio not in VALID_PRIORITIES:
            raise ValueError(f"priority inválida em {dim!r}: {prio!r}")

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


VALID_PRIORITIES = {"alta", "media", "baixa"}

_PRIORITY_ORDER = {"alta": 0, "media": 1, "baixa": 2}


def top_wins(result: dict, n: int = 3) -> list[dict]:
    """Top N dimensions by score (descending). Skips None scores."""
    scored = [
        {"dimension": d, "score": v["score"], "evidence": v["evidence"]}
        for d, v in result["dimensions"].items()
        if v["score"] is not None
    ]
    return sorted(scored, key=lambda x: -x["score"])[:n]


def top_fixes(result: dict, n: int = 3) -> list[dict]:
    """Top N dimensions to fix, ordered by (priority, lowest score)."""
    scored = [
        {
            "dimension": d,
            "score": v["score"],
            "fix": v["fix"]["text"],
            "priority": v["fix"]["priority"],
        }
        for d, v in result["dimensions"].items()
        if v["score"] is not None
    ]
    return sorted(
        scored,
        key=lambda x: (_PRIORITY_ORDER.get(x["priority"], 99), x["score"]),
    )[:n]


def format_scorecard_md(result: dict) -> str:
    """Markdown table: Dimensão | Peso | Score | Status."""
    lines = [
        "| Dimensão | Peso | Score | Status |",
        "|---|---|---|---|",
    ]
    for dim, info in result["dimensions"].items():
        score = info["score"]
        if score is None:
            status = "N/D"
            score_str = "N/D"
        elif score >= 80:
            status = "Forte"
            score_str = str(score)
        elif score >= 60:
            status = "OK"
            score_str = str(score)
        else:
            status = "Atenção"
            score_str = str(score)
        lines.append(f"| {dim} | {info['weight']}% | {score_str} | {status} |")
    return "\n".join(lines)


def format_priorities_md(result: dict, n: int = 3) -> str:
    """Numbered list of top N fixes with priority markers."""
    fixes = top_fixes(result, n=n)
    if not fixes:
        return "Nenhuma prioridade identificada."
    lines = ["## Prioridades"]
    for i, fix in enumerate(fixes, start=1):
        prio = fix["priority"].upper()
        lines.append(
            f"{i}. **[{prio}] {fix['dimension']}** (score {fix['score']}): {fix['fix']}"
        )
    return "\n".join(lines)


def _cli() -> int:
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"Invalid JSON on stdin: {e}", file=sys.stderr)
        return 1

    try:
        result = compute(
            payload["type"],
            payload["dimension_scores"],
            payload.get("evidences", {}),
            payload.get("fixes", {}),
        )
    except (ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    out = {
        **result,
        "top_wins": top_wins(result),
        "top_fixes": top_fixes(result),
        "scorecard_md": format_scorecard_md(result),
        "priorities_md": format_priorities_md(result),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
