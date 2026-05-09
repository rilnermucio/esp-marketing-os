"""Tests for audit_glossary.py."""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from audit_glossary import GLOSSARY, render_glossary_md


class TestGlossaryDict:
    def test_has_at_least_50_terms(self):
        assert len(GLOSSARY) >= 50

    def test_all_entries_have_strings(self):
        for term, definition in GLOSSARY.items():
            assert isinstance(term, str)
            assert isinstance(definition, str)
            assert len(definition) > 20  # meaningful definition

    def test_includes_core_terms(self):
        # Core terms used in audit reports
        for term in ["CWV", "schema markup", "CTA", "value proposition", "SEO"]:
            assert any(term.lower() in k.lower() for k in GLOSSARY.keys()), f"Missing: {term}"


class TestRenderGlossary:
    def test_render_all_when_no_filter(self):
        md = render_glossary_md()
        for term in GLOSSARY:
            assert term in md or term.lower() in md.lower()

    def test_filter_by_used_terms(self):
        used = {"CWV", "schema markup"}
        md = render_glossary_md(used_terms=used)
        # Verify only filtered terms appear
        for term in used:
            assert term in md or term.lower() in md.lower()
        # Verify a non-used term does not appear (pick one not in used set)
        unused_term = next(k for k in GLOSSARY if k not in used)
        # Only check if unused_term has unique enough name
        if len(unused_term) > 5 and unused_term.lower() not in " ".join(used).lower():
            assert unused_term not in md

    def test_render_returns_markdown(self):
        md = render_glossary_md()
        assert "## Glossário" in md
        assert "**" in md  # bold formatting
