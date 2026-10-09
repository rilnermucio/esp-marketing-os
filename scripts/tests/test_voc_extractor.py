"""Voz do cliente: frases literais por sinal e expressões repetidas."""

from __future__ import annotations

import json

import voc_extractor as voc

REVIEWS = [
    "Não consigo organizar minha rotina. Tenho medo de perder clientes.",
    "Queria um método simples. Já tentei vários cursos e não funciona pra mim.",
    "Consegui organizar a agenda em duas semanas! Recomendo muito.",
    "Achei caro demais, será que vale?",
    "Não consigo organizar minha rotina de novo.",
]


def test_classifies_literal_sentences_by_signal():
    result = voc.analyze(REVIEWS)
    frases = {cat: [r["frase"] for r in rows] for cat, rows in result["sinais"].items()}
    assert any("Não consigo organizar" in f for f in frases["dor"])
    assert any("Queria um método simples" in f for f in frases["desejo"])
    assert any("caro demais" in f for f in frases["objecao"])
    assert any("Consegui organizar" in f for f in frases["resultado"])


def test_counts_repeated_sentence():
    rows = voc.analyze(REVIEWS)["sinais"]["dor"]
    top = rows[0]
    assert top["vezes"] >= 1 and "Não consigo" in top["frase"]


def test_repeated_expressions_ignore_stopwords():
    expressions = [e["expressao"] for e in voc.analyze(REVIEWS)["expressoes"]]
    assert "consigo organizar" in expressions


def test_loads_csv_and_json(tmp_path):
    csv_file = tmp_path / "r.csv"
    csv_file.write_text(
        "autor,comentario\nana,Queria mais aulas práticas.\n", encoding="utf-8"
    )
    assert voc.load_items(
        csv_file.read_text(encoding="utf-8"), ".csv", "comentario"
    ) == ["Queria mais aulas práticas."]
    data = json.dumps([{"texto": "Muito caro demais."}, "Recomendo!"])
    assert voc.load_items(data, ".json", field="texto") == [
        "Muito caro demais.",
        "Recomendo!",
    ]


def test_cli_markdown(tmp_path, capsys):
    source = tmp_path / "reviews.txt"
    source.write_text("\n".join(REVIEWS), encoding="utf-8")
    assert voc.main(["--input", str(source)]) == 0
    out = capsys.readouterr().out
    assert "# Voz do cliente: 5 itens analisados" in out and "## Objeções" in out


def test_csv_without_column_is_an_error(tmp_path, capsys):
    source = tmp_path / "r.csv"
    source.write_text("a,b\n1,2\n", encoding="utf-8")
    assert voc.main(["--input", str(source)]) == 1
