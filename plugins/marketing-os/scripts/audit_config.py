"""Loader/validator for .auditoria-config.json (white-label PDF branding).

Returns dict on valid input, None on missing or invalid (with stderr warning).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

SCHEMA = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["brand_name"],
    "properties": {
        "brand_name": {"type": "string", "minLength": 1},
        "logo_path": {"type": "string"},
        "primary_color": {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
        "accent_color": {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
        "footer_text": {"type": "string"},
    },
    "additionalProperties": False,
}


def load(config_path: Path | str | None) -> dict | None:
    """Load and validate config. Returns None on missing or invalid."""
    if config_path is None:
        return None

    path = Path(config_path)
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[audit_config] JSON inválido em {path}: {e}", file=sys.stderr)
        return None

    try:
        jsonschema.validate(data, SCHEMA)
    except jsonschema.ValidationError as e:
        print(f"[audit_config] Schema inválido em {path}: {e.message}", file=sys.stderr)
        return None

    return data
