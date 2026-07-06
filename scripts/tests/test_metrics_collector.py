#!/usr/bin/env python3
"""
Testes para metrics_collector.py — normalização de métricas para /aprender.
"""

from __future__ import annotations

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import metrics_collector as mc

SAMPLE_ITEMS = [
    {"id": "reel-1", "retention": 80, "views": 1000},
    {"titulo": "reel-2", "retention": 60, "views": 900},
    {"title": "reel-3", "retention": 50, "views": 800},
    {"name": "reel-4", "retention": 40, "views": 700},
    {"id": "reel-5", "retention": 30, "views": 600},
    {"id": "reel-6", "retention": 70, "views": 500},
]


class TestSummarize:
    def test_schema_tolerante_id_vs_titulo(self):
        report = mc.summarize(SAMPLE_ITEMS, "retention", min_sample=5)
        assert "reel-1" in report
        assert "reel-2" in report

    def test_top_e_bottom_corretos(self):
        report = mc.summarize(SAMPLE_ITEMS, "retention", min_sample=5)
        top_idx = report.index("## Top 3")
        bottom_idx = report.index("## Bottom 3")
        top_block = report[top_idx:bottom_idx]
        bottom_block = report[bottom_idx:]

        assert "reel-1" in top_block
        assert "80" in top_block
        assert "reel-5" in bottom_block
        assert "30" in bottom_block

    def test_media_calculada(self):
        report = mc.summarize(SAMPLE_ITEMS, "retention", min_sample=5)
        # média = (80+60+50+40+30+70)/6 = 55
        assert "55" in report

    def test_candidatos_somente_acima_desvio(self):
        report = mc.summarize(SAMPLE_ITEMS, "retention", min_sample=5)
        cand_idx = report.index("## Candidatos a aprendizado")
        cand_block = report[cand_idx:]
        assert "reel-1" in cand_block
        assert "reel-5" in cand_block
        # reel-3 (50) está a ~9% da média 55, não deve ser candidato
        lines_with_reel3 = [ln for ln in cand_block.splitlines() if "reel-3" in ln]
        assert not lines_with_reel3

    def test_min_amostra_barra_lista_pequena(self):
        small = SAMPLE_ITEMS[:3]
        with pytest.raises(ValueError, match="insufficient"):
            mc.summarize(small, "retention", min_sample=5)


class TestCli:
    def test_input_malformado_exit_1(self, tmp_path, capsys):
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "metrics_collector.py",
                "--input",
                str(bad),
                "--metrica",
                "retention",
            ],
        )
        try:
            assert mc.main() == 1
            err = capsys.readouterr().err
            assert "JSON" in err or "inválido" in err
        finally:
            monkeypatch.undo()

    def test_lista_vazia_exit_1(self, tmp_path):
        empty = tmp_path / "empty.json"
        empty.write_text("[]", encoding="utf-8")
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "metrics_collector.py",
                "--input",
                str(empty),
                "--metrica",
                "retention",
            ],
        )
        try:
            assert mc.main() == 1
        finally:
            monkeypatch.undo()

    def test_amostra_insuficiente_exit_1(self, tmp_path, capsys):
        small = tmp_path / "small.json"
        small.write_text(json.dumps(SAMPLE_ITEMS[:3]), encoding="utf-8")
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "metrics_collector.py",
                "--input",
                str(small),
                "--metrica",
                "retention",
                "--min-amostra",
                "5",
            ],
        )
        try:
            assert mc.main() == 1
            err = capsys.readouterr().err
            assert "amostra insuficiente" in err
        finally:
            monkeypatch.undo()

    def test_stdout_markdown_valido(self, tmp_path, capsys):
        data = tmp_path / "data.json"
        data.write_text(json.dumps(SAMPLE_ITEMS), encoding="utf-8")
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "metrics_collector.py",
                "--input",
                str(data),
                "--metrica",
                "retention",
            ],
        )
        try:
            assert mc.main() == 0
            out = capsys.readouterr().out
            assert "# Resumo de métricas" in out
            assert "## Top 3" in out
        finally:
            monkeypatch.undo()

    def test_sem_metrica_pedida_exit_1(self, tmp_path, capsys):
        data = tmp_path / "data.json"
        data.write_text(json.dumps(SAMPLE_ITEMS), encoding="utf-8")
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "metrics_collector.py",
                "--input",
                str(data),
                "--metrica",
                "ctr",
            ],
        )
        try:
            assert mc.main() == 1
        finally:
            monkeypatch.undo()
