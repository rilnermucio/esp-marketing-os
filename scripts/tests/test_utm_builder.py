"""UTM e piece_id gerados junto com a peça (fecha a atribuição do /aprender)."""

from __future__ import annotations

import json
from datetime import date
from urllib.parse import parse_qs, urlsplit

import pytest

import utm_builder as utm


def _query(url: str) -> dict:
    return {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}


def test_normalizes_values_without_accents_or_spaces():
    result = utm.build_url(
        "https://site.com/curso",
        "Instagram",
        "Social",
        "Lançamento Outubro",
        "Reels Hook A",
    )
    q = _query(result["url"])
    assert q == {
        "utm_source": "instagram",
        "utm_medium": "social",
        "utm_campaign": "lancamento-outubro",
        "utm_content": "reels-hook-a",
    }


def test_keeps_existing_query_and_replaces_old_utms():
    result = utm.build_url(
        "https://site.com/p?ref=bio&utm_source=velho#topo", "meta", "paid", "bf"
    )
    q = _query(result["url"])
    assert q["ref"] == "bio" and q["utm_source"] == "meta"
    assert result["url"].endswith("#topo")


def test_piece_id_is_stable_and_goes_to_content_when_missing():
    pid = utm.make_piece_id("Black Friday", "", date(2026, 11, 20))
    assert pid == utm.make_piece_id("Black Friday", "", date(2026, 11, 20))
    assert pid.startswith("black-friday-peca-20261120-")
    result = utm.build_url(
        "https://site.com", "meta", "paid", "black friday", piece_id=pid
    )
    assert _query(result["url"])["utm_content"] == pid


def test_rejects_invalid_url_and_empty_required_fields():
    with pytest.raises(ValueError):
        utm.build_url("site.com/sem-esquema", "a", "b", "c")
    with pytest.raises(ValueError):
        utm.build_url("https://site.com", "   ", "b", "c")


def test_cli_json_with_auto_piece_id(capsys):
    code = utm.main(
        [
            "--url",
            "https://site.com",
            "--source",
            "email",
            "--medium",
            "email",
            "--campaign",
            "boas-vindas",
            "--piece-id",
            "auto",
            "--data",
            "2026-10-01",
            "--json",
        ]
    )
    data = json.loads(capsys.readouterr().out)
    assert code == 0
    assert data["piece_id"].startswith("boas-vindas-peca-20261001-")
    assert data["utm_content"] == data["piece_id"]
