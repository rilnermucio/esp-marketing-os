"""Tests for pdf_generator.py (markdown → PDF, white-label aware)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from pdf_generator import generate, _build_html


class TestBasicGenerate:
    def test_generate_creates_non_empty_pdf(self, tmp_path: Path):
        md_path = tmp_path / "report.md"
        md_path.write_text("# Test\n\nSome content.")
        out_path = tmp_path / "report.pdf"
        result = generate(md_path, out_path)
        assert result == out_path
        assert out_path.exists()
        assert out_path.stat().st_size > 100

    def test_generate_renders_tables(self, tmp_path: Path):
        md_path = tmp_path / "report.md"
        md_path.write_text("| A | B |\n|---|---|\n| 1 | 2 |\n")
        out_path = tmp_path / "report.pdf"
        generate(md_path, out_path)
        assert out_path.exists()


class TestBuildHTML:
    def test_html_contains_markdown_h1(self):
        html = _build_html("# Hello\n\nBody.", config=None)
        assert "<h1>" in html
        assert "Hello" in html

    def test_html_default_theme_when_no_config(self):
        html = _build_html("# X", config=None)
        assert "marketing-os" in html.lower()
        assert "#1a73e8" in html


class TestWhiteLabel:
    def test_config_brand_name_in_html(self, tmp_path: Path):
        config = {"brand_name": "Agência X"}
        html = _build_html("# X", config=config)
        assert "Agência X" in html

    def test_config_accent_color_in_html(self):
        config = {"brand_name": "X", "accent_color": "#ff0000"}
        html = _build_html("# X", config=config)
        assert "#ff0000" in html
        assert "#1a73e8" not in html

    def test_config_footer_text_in_html(self):
        config = {"brand_name": "X", "footer_text": "© Cliente Y"}
        html = _build_html("# X", config=config)
        assert "© Cliente Y" in html

    def test_logo_present_when_path_exists(self, tmp_path: Path):
        logo = tmp_path / "logo.png"
        logo.write_bytes(b"fake png")
        config = {"brand_name": "X", "logo_path": str(logo)}
        html = _build_html("# X", config=config)
        assert '<img class="header-logo"' in html

    def test_logo_omitted_when_path_missing(self, tmp_path: Path):
        config = {"brand_name": "X", "logo_path": str(tmp_path / "nonexistent.png")}
        html = _build_html("# X", config=config)
        assert '<img class="header-logo"' not in html

    def test_generate_with_config_path(self, tmp_path: Path):
        md = tmp_path / "r.md"
        md.write_text("# Title")
        cfg = tmp_path / "cfg.json"
        cfg.write_text(json.dumps({"brand_name": "Acme"}))
        out = tmp_path / "r.pdf"
        generate(md, out, cfg)
        assert out.exists()
        assert out.stat().st_size > 100

    def test_footer_with_double_quotes_escaped(self):
        config = {"brand_name": "X", "footer_text": 'He said "hi"'}
        html = _build_html("# X", config=config)
        # Backslash-escaped double quotes appear in CSS
        assert 'said \\"hi\\"' in html


class TestBuildHTMLBraces:
    def test_html_handles_braces_in_markdown(self):
        # Markdown with code block containing braces should not crash format()
        md_text = '# Title\n\nExample: `{"key": "value"}` and `{x: 1, y: 2}`'
        html = _build_html(md_text, config=None)
        # markdown-it HTML-encodes quotes inside code spans: " → &quot;
        assert "key" in html
        assert "y: 2" in html
        # Verify <code> tags rendered, not crashed
        assert "<code>" in html


class TestPDFCLI:
    def test_cli_basic(self, tmp_path: Path):
        md = tmp_path / "r.md"
        md.write_text("# CLI Test")
        out = tmp_path / "r.pdf"
        script = Path(__file__).resolve().parent.parent / "pdf_generator.py"
        result = subprocess.run(
            [sys.executable, str(script), str(md), str(out)],
            capture_output=True, text=True, check=True,
        )
        assert out.exists()

    def test_cli_with_config(self, tmp_path: Path):
        md = tmp_path / "r.md"
        md.write_text("# Configured")
        cfg = tmp_path / "cfg.json"
        cfg.write_text(json.dumps({"brand_name": "Brand X"}))
        out = tmp_path / "r.pdf"
        script = Path(__file__).resolve().parent.parent / "pdf_generator.py"
        result = subprocess.run(
            [sys.executable, str(script), str(md), str(out), str(cfg)],
            capture_output=True, text=True, check=True,
        )
        assert out.exists()

    def test_cli_too_few_args_exits_nonzero(self):
        script = Path(__file__).resolve().parent.parent / "pdf_generator.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True,
        )
        assert result.returncode != 0
        assert "Usage" in result.stderr
