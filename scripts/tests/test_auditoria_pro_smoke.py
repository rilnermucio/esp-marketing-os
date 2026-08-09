"""Offline integration test for /auditoria-pro with deterministic fixtures."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audit_detector import detect
from audit_scoring import RUBRICS, compute
from audit_radar_chart import generate as generate_radar
from audit_roadmap_generator import generate as generate_roadmap
from audit_premium_template import render
from pdf_generator import generate as generate_pdf

def _mock_synthesis() -> dict:
    """Returns a complete synthesis dict for landing audit."""
    rubric = RUBRICS["landing"]
    return {
        "type": "landing",
        "dimension_scores": {dim: 70 for dim in rubric},
        "evidences": {dim: [f"evidence {i}" for i in range(3)] for dim in rubric},
        "fixes": {dim: {"text": f"fix {dim}", "priority": "alta"} for dim in rubric},
    }


def test_full_pipeline_landing(tmp_path: Path):
    # 1. Detect
    detected = detect("https://stripe.com")
    assert detected["type"] == "landing"

    # 2. Mock synthesis
    payload = _mock_synthesis()

    # 3. Compute scoring
    result = compute(
        payload["type"],
        payload["dimension_scores"],
        {dim: e[0] for dim, e in payload["evidences"].items()},
        payload["fixes"],
    )
    assert result["overall"] == 70

    # 4. Generate radar chart
    radar_path = tmp_path / "radar.png"
    scores = {d: i["score"] for d, i in result["dimensions"].items()}
    fixes = {d: i["fix"] for d, i in result["dimensions"].items()}
    generate_radar(scores, fixes, radar_path)
    assert radar_path.exists()

    # 5. Generate roadmap
    fixes_list = [
        {"dimension": d, "score": i["score"], "fix": i["fix"]}
        for d, i in result["dimensions"].items()
    ]
    weights = {d: i["weight"] for d, i in result["dimensions"].items()}
    roadmap = generate_roadmap(fixes_list, weights)
    assert "30_days" in roadmap

    # 6. Build report data
    report_data = {
        "client_url": "https://stripe.com",
        "client_name": "stripe.com",
        "audit_type": "landing",
        "timestamp": "2026-05-09 10:00:00",
        "overall_score": result["overall"],
        "partial": result["partial"],
        "exec_summary": "Stripe entrega execução de classe mundial.",
        "dimensions": {
            d: {
                "score": i["score"],
                "weight": i["weight"],
                "prose": "Análise detalhada da dimensão. " * 20,
                "evidences": payload["evidences"][d],
                "fixes": [i["fix"]],
                "before_after": [],
                "agent_citation": f"Conforme análise mos-X: '{i['evidence'][:60]}...'",
            }
            for d, i in result["dimensions"].items()
        },
        "competitive": {
            "competitors": [{"name": "Adyen", "differentiation": "Foco europeu"}],
            "table_md": "| A |\n|---|\n| 1 |",
        },
        "roadmap": roadmap,
        "appendix": {"research": "raw...", "seo": "raw..."},
        "used_terms": ["CTA", "value proposition", "CWV"],
    }

    # 7. Render HTML
    html = render(
        report_data,
        {"homepage": str(radar_path)},
        {"radar": str(radar_path)},
        config=None,
    )
    html_path = tmp_path / "RELATORIO.html"
    html_path.write_text(html)
    assert "<!DOCTYPE html>" in html
    assert "stripe.com" in html

    # 8. Generate PDF
    pdf_path = tmp_path / "RELATORIO.pdf"
    generate_pdf(html_path, pdf_path, from_html=True)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 5000
