"""CLI de compliance: mesmas regras do hook, com trecho e norma."""

from __future__ import annotations

import json

import compliance_check as cc


def test_check_returns_rule_excerpt_and_norm():
    findings = cc.check("Agende sua consulta gratuita. Resultado garantido!")
    rules = {f["regra"] for f in findings}
    assert "Gratuidade em serviço profissional" in rules
    assert "Promessa de resultado" in rules
    assert all(f["trecho"] and f["mensagem"] for f in findings)


def test_clean_text_has_no_findings():
    assert cc.check("Receita de bolo de cenoura com cobertura de chocolate.") == []


def test_cli_markdown_and_strict(tmp_path, capsys):
    peca = tmp_path / "peca.md"
    peca.write_text("Fature R$ 20 mil no primeiro mês.", encoding="utf-8")
    assert cc.main(["--input", str(peca)]) == 0
    out = capsys.readouterr().out
    assert "## Promessa de ganho" in out and "não substitui parecer jurídico" in out
    assert cc.main(["--input", str(peca), "--strict"]) == 1


def test_cli_json(tmp_path, capsys):
    peca = tmp_path / "peca.md"
    peca.write_text("Sou o melhor advogado da cidade.", encoding="utf-8")
    assert cc.main(["--input", str(peca), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["regra"] == "Título de melhor profissional"


def test_cli_missing_file(tmp_path, capsys):
    assert cc.main(["--input", str(tmp_path / "nao-existe.md")]) == 1
    assert "não encontrado" in capsys.readouterr().err
