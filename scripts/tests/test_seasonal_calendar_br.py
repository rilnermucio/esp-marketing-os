#!/usr/bin/env python3
"""Testes do seasonal_calendar_br (datas comerciais BR, determinístico)."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import seasonal_calendar_br as sc


def _by_name(dates, nome):
    for d in dates:
        if d["nome"] == nome:
            return d
    raise AssertionError(f"data '{nome}' não encontrada")


# ----------------------------------------------------------- Computus
@pytest.mark.parametrize("ano,esperado", [(2026, (4, 5)), (2027, (3, 28))])
def test_easter(ano, esperado):
    e = sc.easter(ano)
    assert (e.month, e.day) == esperado


def test_datas_moveis_2026():
    d = sc.seasonal_dates(2026)
    assert _by_name(d, "Carnaval")["data"] == "2026-02-17"
    assert _by_name(d, "Sexta-feira Santa")["data"] == "2026-04-03"
    assert _by_name(d, "Páscoa")["data"] == "2026-04-05"
    assert _by_name(d, "Corpus Christi")["data"] == "2026-06-04"


def test_datas_por_regra_2026():
    d = sc.seasonal_dates(2026)
    assert _by_name(d, "Dia das Mães")["data"] == "2026-05-10"
    assert _by_name(d, "Dia dos Pais")["data"] == "2026-08-09"
    assert _by_name(d, "Black Friday")["data"] == "2026-11-27"


def test_datas_fixas_2026():
    d = sc.seasonal_dates(2026)
    assert _by_name(d, "Dia dos Namorados")["data"] == "2026-06-12"
    assert _by_name(d, "Natal")["data"] == "2026-12-25"


def test_outro_ano_recalcula():
    d = sc.seasonal_dates(2027)
    assert _by_name(d, "Carnaval")["data"] == "2027-02-09"
    assert _by_name(d, "Black Friday")["data"] == "2027-11-26"


# ----------------------------------------------------------- schema
def test_schema_completo_e_ordenado():
    d = sc.seasonal_dates(2026)
    assert d == sorted(d, key=lambda x: x["data"])
    for item in d:
        assert set(item) == {"data", "nome", "tipo", "dias_antecedencia_ideal", "nichos_fortes"}
        assert item["tipo"] in {"comercial", "cultural", "religiosa"}
        assert isinstance(item["dias_antecedencia_ideal"], int) and item["dias_antecedencia_ideal"] >= 0
        assert isinstance(item["nichos_fortes"], list)


# ----------------------------------------------------------- janela
def test_dates_in_range_filtra_e_ordena():
    janela = sc.dates_in_range(dt.date(2026, 11, 1), dt.date(2026, 12, 1))
    nomes = [x["nome"] for x in janela]
    assert "Black Friday" in nomes
    assert "Carnaval" not in nomes
    assert janela == sorted(janela, key=lambda x: x["data"])


def test_proximos_respeita_janela():
    hoje = dt.date(2026, 11, 20)
    prox = sc.proximos(15, hoje=hoje)
    nomes = [x["nome"] for x in prox]
    assert "Black Friday" in nomes  # 27/11 está dentro de 15 dias
    assert all(x["data"] >= "2026-11-20" for x in prox)


# ----------------------------------------------------------- CLI
def test_main_json(capsys):
    with patch.object(sys, "argv", ["seasonal_calendar_br.py", "--ano", "2026", "--json"]):
        sc.main()
    out = capsys.readouterr().out
    data = json.loads(out)
    assert any(x["nome"] == "Black Friday" for x in data)


def test_main_humano(capsys):
    with patch.object(sys, "argv", ["seasonal_calendar_br.py", "--ano", "2026"]):
        sc.main()
    out = capsys.readouterr().out
    assert "Black Friday" in out
