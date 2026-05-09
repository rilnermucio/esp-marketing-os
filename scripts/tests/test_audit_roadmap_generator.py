"""Tests for audit_roadmap_generator.py."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from audit_roadmap_generator import (
    generate,
    _estimate_effort,
    _suggest_owner,
)


class TestGenerate:
    def test_alta_priority_low_score_high_weight_to_30_days(self):
        fixes = [{
            "dimension": "Conversão (CTA, friction, funil)",
            "score": 50,
            "fix": {"text": "Adicionar CTA secundário", "priority": "alta"},
        }]
        rubric_weights = {"Conversão (CTA, friction, funil)": 25}
        result = generate(fixes, rubric_weights)
        assert any(item["dimension"].startswith("Conversão")
                   for item in result["30_days"])

    def test_media_priority_to_90_days(self):
        fixes = [{
            "dimension": "Trust signals",
            "score": 70,
            "fix": {"text": "Adicionar depoimentos", "priority": "media"},
        }]
        rubric_weights = {"Trust signals": 10}
        result = generate(fixes, rubric_weights)
        assert any(item["dimension"] == "Trust signals" for item in result["90_days"])

    def test_baixa_priority_to_180_days(self):
        fixes = [{
            "dimension": "Brand (consistência, voice)",
            "score": 85,
            "fix": {"text": "Refinar voz em FAQ", "priority": "baixa"},
        }]
        rubric_weights = {"Brand (consistência, voice)": 10}
        result = generate(fixes, rubric_weights)
        assert any(item["dimension"].startswith("Brand")
                   for item in result["180_days"])

    def test_each_item_has_required_fields(self):
        fixes = [{
            "dimension": "Conversão",
            "score": 60,
            "fix": {"text": "X", "priority": "alta"},
        }]
        rubric_weights = {"Conversão": 25}
        result = generate(fixes, rubric_weights)
        for bucket in ("30_days", "90_days", "180_days"):
            for item in result[bucket]:
                assert "action" in item
                assert "dimension" in item
                assert "effort" in item
                assert item["effort"] in ("S", "M", "L")
                assert "impact" in item
                assert item["impact"] in ("alto", "medio", "baixo")
                assert "owner" in item


class TestEstimateEffort:
    def test_redesign_keyword_returns_L(self):
        assert _estimate_effort("Redesign do hero section") == "L"

    def test_reescrever_keyword_returns_M(self):
        assert _estimate_effort("Reescrever title tag") == "M"

    def test_simple_returns_S(self):
        assert _estimate_effort("Adicionar 1 selo de segurança") == "S"

    def test_create_keyword_returns_M(self):
        assert _estimate_effort("Criar lead magnet") == "M"


class TestSuggestOwner:
    def test_conversao_to_growth(self):
        assert _suggest_owner("Conversão (CTA, friction, funil)") == "Growth Lead"

    def test_copy_to_copywriter(self):
        assert _suggest_owner("Copy (headline, value prop)") == "Copywriter"

    def test_seo_to_seo_specialist(self):
        assert _suggest_owner("SEO (technical + content)") == "SEO Specialist"

    def test_design_to_design(self):
        assert _suggest_owner("Design (hierarquia visual)") == "Designer"

    def test_unknown_to_marketing_lead(self):
        assert _suggest_owner("Unknown Dimension") == "Marketing Lead"
