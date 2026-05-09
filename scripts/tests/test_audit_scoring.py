"""Tests for audit_scoring.py."""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from audit_scoring import RUBRICS, validate_rubrics, compute


class TestRubrics:
    def test_landing_sums_to_100(self):
        assert sum(RUBRICS["landing"].values()) == 100

    def test_instagram_sums_to_100(self):
        assert sum(RUBRICS["instagram"].values()) == 100

    def test_meta_ads_sums_to_100(self):
        assert sum(RUBRICS["meta_ads"].values()) == 100

    def test_youtube_sums_to_100(self):
        assert sum(RUBRICS["youtube"].values()) == 100

    def test_validate_rubrics_passes(self):
        validate_rubrics()

    def test_all_4_types_present(self):
        assert set(RUBRICS.keys()) == {"landing", "instagram", "meta_ads", "youtube"}


class TestCompute:
    def test_full_input_landing(self):
        scores = {
            "Conversão (CTA, friction, funil)": 80,
            "Copy (headline, value prop)": 70,
            "SEO (technical + content)": 60,
            "Trust signals": 50,
            "Design (hierarquia visual)": 90,
            "Brand (consistência, voice)": 75,
            "Diferenciação competitiva": 65,
        }
        evidences = {k: f"evidence for {k}" for k in scores}
        fixes = {k: {"text": f"fix {k}", "priority": "media"} for k in scores}
        result = compute("landing", scores, evidences, fixes)
        # Weighted: 80*25 + 70*20 + 60*15 + 50*10 + 90*10 + 75*10 + 65*10 = 7100 / 100 = 71
        assert result["overall"] == 71
        assert result["partial"] is False
        assert len(result["dimensions"]) == 7

    def test_partial_input_recalcs(self):
        scores = {
            "Conversão (CTA, friction, funil)": 80,
            "Copy (headline, value prop)": 70,
            "SEO (technical + content)": None,
            "Trust signals": 50,
            "Design (hierarquia visual)": 90,
            "Brand (consistência, voice)": 75,
            "Diferenciação competitiva": 65,
        }
        evidences = {k: "" for k in scores if scores[k] is not None}
        fixes = {k: {"text": "", "priority": "baixa"} for k in scores if scores[k] is not None}
        result = compute("landing", scores, evidences, fixes)
        assert result["partial"] is True
        # 6 scored: (80*25+70*20+50*10+90*10+75*10+65*10)/85 = 6200/85 ≈ 72.94 → 73
        assert result["overall"] == 73

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError, match="tipo desconhecido"):
            compute("invalid_type", {}, {}, {})

    def test_missing_dimension_raises(self):
        with pytest.raises(ValueError, match="dimensão"):
            compute("landing", {"Copy (headline, value prop)": 70}, {}, {})

    def test_score_out_of_range_raises(self):
        scores = {k: 50 for k in RUBRICS["landing"]}
        scores["Copy (headline, value prop)"] = 150
        with pytest.raises(ValueError, match="0-100"):
            compute("landing", scores, {}, {})

    def test_all_none_raises(self):
        scores = {k: None for k in RUBRICS["landing"]}
        with pytest.raises(ValueError, match="todas as dimensões"):
            compute("landing", scores, {}, {})
