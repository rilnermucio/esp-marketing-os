"""Tests for audit_scoring.py."""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from audit_scoring import RUBRICS, validate_rubrics


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
