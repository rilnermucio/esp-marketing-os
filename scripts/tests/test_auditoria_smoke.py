"""Offline integration test for /auditoria with deterministic agent outputs."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audit_detector import detect
from audit_scoring import RUBRICS, compute, format_priorities_md, format_scorecard_md
from pdf_generator import generate


def _mock_synthesis_landing() -> dict:
    """Returns scores/evidences/fixes that a real synthesis step would produce."""
    rubric = RUBRICS["landing"]
    return {
        "type": "landing",
        "dimension_scores": {dim: 70 for dim in rubric},
        "evidences": {dim: f"saw evidence in {dim}" for dim in rubric},
        "fixes": {
            dim: {"text": f"fix {dim}", "priority": "media"} for dim in rubric
        },
    }


def test_full_pipeline_landing(tmp_path: Path):
    detected = detect("https://stripe.com")
    assert detected["type"] == "landing"

    payload = _mock_synthesis_landing()

    result = compute(
        payload["type"],
        payload["dimension_scores"],
        payload["evidences"],
        payload["fixes"],
    )
    assert result["overall"] == 70
    assert result["partial"] is False

    md_content = f"""# Auditoria: stripe.com

**Tipo:** landing
**Score Geral:** {result["overall"]}/100

## Scorecard

{format_scorecard_md(result)}

## Prioridades

{format_priorities_md(result)}
"""
    md_path = tmp_path / "RELATORIO.md"
    md_path.write_text(md_content)

    pdf_path = tmp_path / "RELATORIO.pdf"
    generate(md_path, pdf_path)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000


def test_full_pipeline_with_white_label_config(tmp_path: Path):
    cfg_path = tmp_path / ".auditoria-config.json"
    cfg_path.write_text(json.dumps({
        "brand_name": "Agência Smoke Test",
        "accent_color": "#ff5500",
    }))

    md_path = tmp_path / "RELATORIO.md"
    md_path.write_text("# Auditoria: example.com\n\nContent.")

    pdf_path = tmp_path / "RELATORIO.pdf"
    generate(md_path, pdf_path, cfg_path)
    assert pdf_path.exists()


def test_pipeline_handles_partial_input(tmp_path: Path):
    rubric = RUBRICS["landing"]
    scores = {dim: 70 for dim in rubric}
    scores["SEO (technical + content)"] = None
    evidences = {dim: "" for dim in rubric if scores[dim] is not None}
    fixes = {
        dim: {"text": "", "priority": "baixa"}
        for dim in rubric if scores[dim] is not None
    }
    result = compute("landing", scores, evidences, fixes)
    assert result["partial"] is True
    md = f"# Partial\n\n{format_scorecard_md(result)}"
    md_path = tmp_path / "RELATORIO.md"
    md_path.write_text(md)
    pdf_path = tmp_path / "RELATORIO.pdf"
    generate(md_path, pdf_path)
    assert pdf_path.exists()
