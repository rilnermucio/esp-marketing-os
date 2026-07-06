"""Generate radar chart PNG for /auditoria-pro reports.

Two layers:
- Solid colored polygon: current scores (filled with accent_color alpha 0.3)
- Dashed outline: potential scores after priority-alta fixes (estimated)

Uses matplotlib (Agg backend, no display required).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_PRIORITY_BOOST = {"alta": 15, "media": 5, "baixa": 2}


def _compute_potential_scores(
    scores: dict[str, int | None],
    fixes: dict[str, dict],
) -> dict[str, int | None]:
    """Estimate scores after applying priority-weighted fixes. Capped at 100."""
    potential = {}
    for dim, score in scores.items():
        if score is None:
            potential[dim] = None
            continue
        fix = fixes.get(dim, {})
        boost = _PRIORITY_BOOST.get(fix.get("priority", "baixa"), 2)
        potential[dim] = min(100, score + boost)
    return potential


def _truncate(label: str, max_len: int = 22) -> str:
    if len(label) <= max_len:
        return label
    return label[: max_len - 1].rstrip() + "…"


def generate(
    scores: dict[str, int | None],
    fixes: dict[str, dict],
    output_path: Path | str,
    primary_color: str = "#0a2540",
    accent_color: str = "#ff6b35",
) -> Path:
    """Render radar chart PNG. Returns output_path."""
    out_path = Path(output_path)
    dimensions = list(scores.keys())
    n = len(dimensions)

    # Replace None with 0 for plotting (visual only)
    current = [scores[d] if scores[d] is not None else 0 for d in dimensions]
    potential_scores = _compute_potential_scores(scores, fixes)
    potential = [
        potential_scores[d] if potential_scores[d] is not None else 0
        for d in dimensions
    ]

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    current += current[:1]
    potential += potential[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=200)

    # Potential outline (dashed, behind)
    ax.plot(
        angles,
        potential,
        color=accent_color,
        linewidth=1.5,
        linestyle="--",
        alpha=0.6,
        label="Potencial após fixes priorizados",
    )

    # Current scores (solid filled)
    ax.fill(angles, current, color=accent_color, alpha=0.25)
    ax.plot(angles, current, color=primary_color, linewidth=2.5, label="Score atual")

    # Axis labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        [_truncate(d) for d in dimensions], fontsize=9, color=primary_color
    )

    # Radial gridlines
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=8, color="#6b7280")
    ax.grid(color="#e5e7eb", linewidth=0.8)

    # Style
    ax.spines["polar"].set_color("#e5e7eb")
    ax.set_facecolor("#ffffff")

    # Legend
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=9, frameon=False)

    plt.tight_layout()
    plt.savefig(
        out_path,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
        transparent=False,
    )
    plt.close(fig)

    return out_path


def _cli() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scores-json", required=True, help="Path to scoring_output.json"
    )
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--primary-color", default="#0a2540")
    parser.add_argument("--accent-color", default="#ff6b35")
    args = parser.parse_args()

    data = json.loads(Path(args.scores_json).read_text(encoding="utf-8"))
    scores = {d: info["score"] for d, info in data["dimensions"].items()}
    fixes = {d: info["fix"] for d, info in data["dimensions"].items()}

    generate(
        scores,
        fixes,
        Path(args.output),
        primary_color=args.primary_color,
        accent_color=args.accent_color,
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
