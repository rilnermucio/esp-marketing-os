"""Tests for audit_config.py (white-label config loader)."""
from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path

from jsonschema.validators import validator_for

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from audit_config import SCHEMA, load


def test_schema_metaschema_is_registered():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        validator_for(SCHEMA)


class TestConfigLoad:
    def test_none_path_returns_none(self):
        assert load(None) is None

    def test_missing_file_returns_none(self, tmp_path: Path):
        assert load(tmp_path / "nonexistent.json") is None

    def test_valid_minimal_config(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({"brand_name": "Agência X"}))
        result = load(cfg_path)
        assert result == {"brand_name": "Agência X"}

    def test_valid_full_config(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg = {
            "brand_name": "Agência X",
            "logo_path": "./logo.png",
            "primary_color": "#1a1a1a",
            "accent_color": "#0066cc",
            "footer_text": "Custom footer",
        }
        cfg_path.write_text(json.dumps(cfg))
        assert load(cfg_path) == cfg

    def test_missing_brand_name_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({"logo_path": "./logo.png"}))
        assert load(cfg_path) is None

    def test_invalid_color_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({
            "brand_name": "X",
            "primary_color": "red",
        }))
        assert load(cfg_path) is None

    def test_malformed_json_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text("{not valid json")
        assert load(cfg_path) is None

    def test_extra_property_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({
            "brand_name": "X",
            "unknown_field": "value",
        }))
        assert load(cfg_path) is None
