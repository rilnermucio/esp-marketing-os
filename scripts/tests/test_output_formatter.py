#!/usr/bin/env python3
"""
Testes para output_formatter.py
"""

import argparse
import json
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from output_formatter import (
    _SafeEncoder,
    to_json,
    print_json,
    print_separator,
    print_table,
    print_key_value,
    print_list,
    OutputFormatter,
    add_output_args,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_args(**kwargs) -> argparse.Namespace:
    defaults = {"json": False, "output": None, "format": "human"}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


# ---------------------------------------------------------------------------
# _SafeEncoder / to_json
# ---------------------------------------------------------------------------

def test_to_json_dict():
    result = to_json({"chave": "valor"})
    data = json.loads(result)
    assert data["chave"] == "valor"


def test_to_json_datetime():
    from datetime import datetime, date
    dt = datetime(2026, 2, 17, 12, 0, 0)
    result = to_json({"data": dt})
    assert "2026-02-17" in result


def test_to_json_date():
    from datetime import date
    d = date(2026, 2, 17)
    result = to_json({"data": d})
    assert "2026-02-17" in result


def test_to_json_set():
    result = to_json({"items": {3, 1, 2}})
    data = json.loads(result)
    assert data["items"] == [1, 2, 3]  # sorted


def test_to_json_portuguese_chars():
    result = to_json({"texto": "ação, acentuação"})
    assert "ação" in result
    assert "acentuação" in result


def test_to_json_indent():
    result = to_json({"a": 1}, indent=4)
    assert "    " in result  # 4 espaços de indentação


# ---------------------------------------------------------------------------
# print_json
# ---------------------------------------------------------------------------

def test_print_json_imprime_json(capsys):
    print_json({"chave": "valor", "numero": 42})
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["chave"] == "valor"
    assert data["numero"] == 42


def test_print_json_lista(capsys):
    print_json([1, 2, 3])
    out = capsys.readouterr().out
    assert json.loads(out) == [1, 2, 3]


# ---------------------------------------------------------------------------
# print_separator
# ---------------------------------------------------------------------------

def test_print_separator_padrao(capsys):
    print_separator()
    out = capsys.readouterr().out.strip()
    assert out == "=" * 60


def test_print_separator_customizado(capsys):
    print_separator(char="-", width=30)
    out = capsys.readouterr().out.strip()
    assert out == "-" * 30


# ---------------------------------------------------------------------------
# print_table
# ---------------------------------------------------------------------------

COLUMNS = [
    {"key": "nome", "label": "NOME", "width": 20},
    {"key": "valor", "label": "VALOR", "width": 10, "align": "right"},
]

ROWS = [
    {"nome": "Item A", "valor": 100},
    {"nome": "Item B", "valor": 200},
]


def test_print_table_exibe_cabecalho(capsys):
    print_table(ROWS, COLUMNS)
    out = capsys.readouterr().out
    assert "NOME" in out
    assert "VALOR" in out


def test_print_table_exibe_dados(capsys):
    print_table(ROWS, COLUMNS)
    out = capsys.readouterr().out
    assert "Item A" in out
    assert "Item B" in out


def test_print_table_com_titulo(capsys):
    print_table(ROWS, COLUMNS, title="Minha Tabela")
    out = capsys.readouterr().out
    assert "Minha Tabela" in out


def test_print_table_lista_vazia(capsys):
    print_table([], COLUMNS)
    out = capsys.readouterr().out
    assert "sem dados" in out


def test_print_table_trunca_valores_longos(capsys):
    rows = [{"nome": "A" * 100, "valor": 999}]
    print_table(rows, COLUMNS)
    out = capsys.readouterr().out
    # Valor deve estar truncado para width=20
    lines = [l for l in out.split("\n") if "A" in l]
    assert any(len(l) < 200 for l in lines)


# ---------------------------------------------------------------------------
# print_key_value
# ---------------------------------------------------------------------------

def test_print_key_value_exibe_pares(capsys):
    print_key_value({"nome": "Orion", "versao": "4.0"})
    out = capsys.readouterr().out
    assert "nome" in out
    assert "Orion" in out
    assert "versao" in out


def test_print_key_value_com_titulo(capsys):
    print_key_value({"a": 1}, title="Resumo")
    out = capsys.readouterr().out
    assert "Resumo" in out


def test_print_key_value_dict_aninhado(capsys):
    print_key_value({"meta": {"clicks": 100, "impressions": 1000}})
    out = capsys.readouterr().out
    assert "clicks" in out
    assert "100" in out


def test_print_key_value_lista(capsys):
    print_key_value({"tags": ["seo", "marketing", "conteúdo"]})
    out = capsys.readouterr().out
    assert "seo" in out


# ---------------------------------------------------------------------------
# print_list
# ---------------------------------------------------------------------------

def test_print_list_exibe_itens(capsys):
    print_list(["item 1", "item 2", "item 3"])
    out = capsys.readouterr().out
    assert "item 1" in out
    assert "item 2" in out
    assert "item 3" in out


def test_print_list_com_titulo(capsys):
    print_list(["a", "b"], title="Lista")
    out = capsys.readouterr().out
    assert "Lista" in out


def test_print_list_bullet_customizado(capsys):
    print_list(["x"], bullet="→")
    out = capsys.readouterr().out
    assert "→" in out


# ---------------------------------------------------------------------------
# OutputFormatter
# ---------------------------------------------------------------------------

def test_output_formatter_modo_json():
    fmt = OutputFormatter(make_args(json=True))
    assert fmt.is_json() is True


def test_output_formatter_modo_humano():
    fmt = OutputFormatter(make_args(json=False))
    assert fmt.is_json() is False


def test_output_formatter_format_json():
    fmt = OutputFormatter(make_args(json=False, format="json"))
    assert fmt.is_json() is True


def test_print_human_suprimido_em_json_mode(capsys):
    fmt = OutputFormatter(make_args(json=True))
    fmt.print_human("Texto humano")
    out = capsys.readouterr().out
    assert out == ""


def test_print_human_exibe_em_modo_humano(capsys):
    fmt = OutputFormatter(make_args(json=False))
    fmt.print_human("Texto humano")
    out = capsys.readouterr().out
    assert "Texto humano" in out


def test_print_data_exibe_json_em_json_mode(capsys):
    fmt = OutputFormatter(make_args(json=True))
    fmt.print_data({"resultado": "ok"})
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["resultado"] == "ok"


def test_print_data_silencioso_em_modo_humano(capsys):
    fmt = OutputFormatter(make_args(json=False))
    fmt.print_data({"resultado": "ok"})
    out = capsys.readouterr().out
    assert out == ""


def test_print_com_human_fn_em_modo_humano(capsys):
    fmt = OutputFormatter(make_args(json=False))
    fmt.print({"val": 42}, human_fn=lambda d: print(f"Valor: {d['val']}"))
    out = capsys.readouterr().out
    assert "Valor: 42" in out


def test_print_json_em_json_mode(capsys):
    fmt = OutputFormatter(make_args(json=True))
    fmt.print({"val": 42}, human_fn=lambda d: print("humano"))
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["val"] == 42


def test_print_sem_human_fn_silencioso(capsys):
    fmt = OutputFormatter(make_args(json=False))
    fmt.print({"val": 42})
    out = capsys.readouterr().out
    assert out == ""


def test_save_cria_arquivo(tmp_path):
    output_file = str(tmp_path / "saida.json")
    fmt = OutputFormatter(make_args(json=False, output=output_file))
    path = fmt.save({"dados": [1, 2, 3]}, "teste")
    assert path == output_file
    with open(output_file) as f:
        data = json.load(f)
    assert data["dados"] == [1, 2, 3]


def test_save_sem_output_retorna_none():
    fmt = OutputFormatter(make_args(json=False, output=None))
    result = fmt.save({"dados": [1]}, "teste")
    assert result is None


# ---------------------------------------------------------------------------
# add_output_args
# ---------------------------------------------------------------------------

def test_add_output_args_adiciona_json():
    parser = argparse.ArgumentParser()
    add_output_args(parser)
    args = parser.parse_args(["--json"])
    assert args.json is True


def test_add_output_args_json_padrao_false():
    parser = argparse.ArgumentParser()
    add_output_args(parser)
    args = parser.parse_args([])
    assert args.json is False


def test_add_output_args_output():
    parser = argparse.ArgumentParser()
    add_output_args(parser)
    args = parser.parse_args(["--output", "resultado.json"])
    assert args.output == "resultado.json"


def test_add_output_args_output_shorthand():
    parser = argparse.ArgumentParser()
    add_output_args(parser)
    args = parser.parse_args(["-o", "resultado.json"])
    assert args.output == "resultado.json"


def test_add_output_args_com_format():
    parser = argparse.ArgumentParser()
    add_output_args(parser, include_format=True)
    args = parser.parse_args(["--format", "json"])
    assert args.format == "json"
