"""Generate 30/90/180 day roadmap from audit fixes.

Heuristic bucketing:
- 30 days: priority alta + score < 70 + weight >= 15 (high impact, urgent)
- 90 days: priority alta + medium weight, OR priority media + low score
- 180 days: priority baixa, OR priority media + high score, OR remaining

Each item has: action, dimension, effort (S/M/L), impact (alto/medio/baixo), owner.
"""

from __future__ import annotations

import json
import sys

_OWNER_MAP = {
    "Conversão": "Growth Lead",
    "Copy": "Copywriter",
    "SEO": "SEO Specialist",
    "Trust": "Growth Lead",
    "Design": "Designer",
    "Brand": "Brand Manager",
    "Diferenciação": "Marketing Lead",
    "Bio": "Social Media Manager",
    "Hooks": "Content Lead",
    "Strategy": "Content Lead",
    "Engagement": "Social Media Manager",
    "Cadência": "Content Lead",
    "Visual": "Designer",
}


_EFFORT_KEYWORDS_L = ["redesign", "refazer", "reestruturar", "criar do zero", "rebuild"]
_EFFORT_KEYWORDS_M = [
    "reescrever",
    "criar",
    "implementar",
    "adicionar lead magnet",
    "construir",
    "desenvolver",
    "configurar",
]


def _estimate_effort(fix_text: str) -> str:
    """S = small (<1 day), M = medium (1-5 days), L = large (>1 week)."""
    text_lower = fix_text.lower()
    for kw in _EFFORT_KEYWORDS_L:
        if kw in text_lower:
            return "L"
    for kw in _EFFORT_KEYWORDS_M:
        if kw in text_lower:
            return "M"
    return "S"


def _suggest_owner(dimension: str) -> str:
    """Map dimension name to suggested owner role."""
    for prefix, owner in _OWNER_MAP.items():
        if prefix.lower() in dimension.lower():
            return owner
    return "Marketing Lead"


def _impact_from_priority_and_weight(priority: str, weight: int) -> str:
    if priority == "alta" and weight >= 15:
        return "alto"
    if priority == "alta" or weight >= 20:
        return "alto"
    if priority == "media":
        return "medio"
    return "baixo"


def _bucket_for(priority: str, score: int, weight: int) -> str:
    """Decide which bucket a fix belongs to."""
    if priority == "alta" and score < 70 and weight >= 15:
        return "30_days"
    if priority == "alta":
        return "30_days" if score < 80 else "90_days"
    if priority == "media":
        return "90_days" if score < 75 else "180_days"
    return "180_days"


def generate(fixes: list[dict], rubric_weights: dict[str, int]) -> dict:
    """Generate roadmap dict with 3 buckets."""
    result = {"30_days": [], "90_days": [], "180_days": []}

    for fix_entry in fixes:
        dim = fix_entry["dimension"]
        score = fix_entry.get("score", 50)
        fix_data = fix_entry.get("fix", {})
        text = fix_data.get("text", "")
        priority = fix_data.get("priority", "baixa")
        weight = rubric_weights.get(dim, 10)

        bucket = _bucket_for(priority, score, weight)
        item = {
            "action": text,
            "dimension": dim,
            "effort": _estimate_effort(text),
            "impact": _impact_from_priority_and_weight(priority, weight),
            "owner": _suggest_owner(dim),
            "priority": priority,
        }
        result[bucket].append(item)

    return result


def _cli() -> int:
    payload = json.loads(sys.stdin.read())

    # Accept either scoring_output.json structure or simpler {fixes, weights}
    if "dimensions" in payload:
        # scoring_output.json format
        fixes = []
        weights = {}
        for dim, info in payload["dimensions"].items():
            fixes.append(
                {
                    "dimension": dim,
                    "score": info["score"] if info["score"] is not None else 50,
                    "fix": info["fix"],
                }
            )
            weights[dim] = info["weight"]
    else:
        fixes = payload["fixes"]
        weights = payload.get("rubric_weights", {})

    result = generate(fixes, weights)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
