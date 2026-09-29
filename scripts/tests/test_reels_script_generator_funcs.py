#!/usr/bin/env python3
"""
Testes funcionais para reels_script_generator.py.
"""

from __future__ import annotations

import os
import random
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import reels_script_generator as rsg


def _gerar_roteiro_estavel(tema, duracao, formato):
    """Chamada direta. Até 2026-09 este helper tentava 30 vezes para esconder um
    KeyError de templates com campo sem valor (F-EVAL-05); o bug foi corrigido e
    test_todos_os_templates_formatam trava a classe."""
    return rsg.gerar_roteiro(tema, duracao, formato)


# ----------------------------------------------------------- gerar_roteiro
def test_gerar_roteiro_formato_valido():
    r = _gerar_roteiro_estavel("produtividade", 30, "tutorial")
    assert r["tema"] == "produtividade"
    assert r["formato"] == rsg.ESTRUTURAS["tutorial"]["nome"]
    assert "30" in r["duracao"]


def test_gerar_roteiro_formato_invalido_default():
    r = _gerar_roteiro_estavel("X", 30, "formato_inexistente")
    assert r["formato"] == rsg.ESTRUTURAS["tutorial"]["nome"]


def test_gerar_roteiro_estrutura_completa():
    r = _gerar_roteiro_estavel("X", 30, "tutorial")
    assert "estrutura" in r
    assert "hook_sugerido" in r
    assert "cta_sugerido" in r
    assert "direcoes_camera" in r
    assert isinstance(r["estrutura"], list)
    assert len(r["estrutura"]) >= 3


def test_gerar_roteiro_cada_etapa_tem_campos():
    r = _gerar_roteiro_estavel("X", 30, "tutorial")
    for parte in r["estrutura"]:
        assert "tempo" in parte
        assert "tipo" in parte
        assert "descricao" in parte
        assert "direcao" in parte


def test_gerar_roteiro_todos_formatos():
    for fmt in rsg.ESTRUTURAS:
        r = _gerar_roteiro_estavel("X", 30, fmt)
        assert r["formato"] == rsg.ESTRUTURAS[fmt]["nome"]
        assert len(r["estrutura"]) >= 1


def test_gerar_roteiro_hook_sem_placeholders():
    r = _gerar_roteiro_estavel("vendas", 30, "tutorial")
    # Hooks padrão usam {tema} mas devem ser substituídos
    assert "{tema}" not in r["hook_sugerido"]


def test_gerar_roteiro_duracao_diferente():
    r60 = _gerar_roteiro_estavel("X", 60, "tutorial")
    assert "60" in r60["duracao"]


# ----------------------------------------------------------- formatar_saida
def test_formatar_saida_inclui_tema():
    r = _gerar_roteiro_estavel("produtividade", 30, "tutorial")
    out = rsg.formatar_saida(r)
    assert "produtividade" in out


def test_formatar_saida_titulo_e_secoes():
    r = _gerar_roteiro_estavel("X", 30, "tutorial")
    out = rsg.formatar_saida(r)
    assert "ROTEIRO PARA REELS" in out
    assert "HOOK SUGERIDO" in out
    assert "ESTRUTURA DO ROTEIRO" in out
    assert "CTA SUGERIDO" in out
    assert "DICAS DE GRAVAÇÃO" in out


def test_formatar_saida_inclui_etapas():
    r = _gerar_roteiro_estavel("X", 30, "listicle")
    out = rsg.formatar_saida(r)
    for parte in r["estrutura"]:
        assert parte["tipo"] in out


# ----------------------------------------------------------- listar_formatos
def test_listar_formatos_imprime_todos(capsys):
    rsg.listar_formatos()
    out = capsys.readouterr().out
    for k in rsg.ESTRUTURAS:
        assert k in out


# ----------------------------------------------------------- main / CLI
def test_main_sem_args(capsys):
    with patch.object(sys, "argv", ["reels_script_generator.py"]):
        rsg.main()
    out = capsys.readouterr().out
    assert "Uso" in out
    assert "FORMATOS DE REELS" in out


def test_main_flag_formatos(capsys):
    with patch.object(sys, "argv", ["reels_script_generator.py", "--formatos"]):
        rsg.main()
    out = capsys.readouterr().out
    assert "FORMATOS" in out


def _main_estavel(argv, capsys):
    with patch.object(sys, "argv", argv):
        rsg.main()
    return capsys.readouterr().out


def test_main_tema_e_duracao(capsys):
    out = _main_estavel(
        ["reels_script_generator.py", "vendas", "30", "tutorial"], capsys
    )
    assert "vendas" in out
    assert "ROTEIRO PARA REELS" in out


def test_main_duracao_invalida_avisa_e_usa_30(capsys):
    """45 não está nas durações padrão → avisa e usa 30."""
    out = _main_estavel(["reels_script_generator.py", "X", "45", "tutorial"], capsys)
    assert "padrão" in out.lower() or "recomendadas" in out.lower()


def test_main_duracao_valida_60(capsys):
    out = _main_estavel(["reels_script_generator.py", "X", "60", "tutorial"], capsys)
    assert "60" in out


def test_main_formato_default_quando_nao_passado(capsys):
    out = _main_estavel(["reels_script_generator.py", "X"], capsys)
    # Sem formato → default tutorial
    assert "Tutorial" in out or "tutorial" in out.lower()


def test_todos_os_templates_formatam():
    """Todo template de HOOKS e CTAS formata com os campos do gerador (sem sorteio)."""
    campos_hook = rsg._hook_fields("produtividade")
    campos_cta = rsg._cta_fields("produtividade")
    for categoria, templates in rsg.HOOKS.items():
        for template in templates:
            assert "{" not in template.format(**campos_hook), (categoria, template)
    for categoria, templates in rsg.CTAS.items():
        for template in templates:
            template.format(**campos_cta)


def test_gerar_roteiro_nunca_levanta_keyerror():
    for semente in range(200):
        random.seed(semente)
        rsg.gerar_roteiro("produtividade", 30, "tutorial")
