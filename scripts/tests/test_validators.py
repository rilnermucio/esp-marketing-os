#!/usr/bin/env python3
"""
Testes para o módulo validators.py
"""

import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validators import (
    ValidationError,
    PLATAFORMAS_VALIDAS,
    FORMATOS_VALIDOS,
    validar_texto,
    validar_inteiro,
    validar_float,
    validar_arquivo,
    validar_diretorio_saida,
    validar_plataforma,
    validar_lista_plataformas,
    validar_formato,
    validar_data,
    validar_semana_iso,
    validar_url,
    handle_validation_error,
)


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

def test_plataformas_validas_nao_vazio():
    assert len(PLATAFORMAS_VALIDAS) > 0


def test_plataformas_validas_contem_instagram():
    assert "instagram" in PLATAFORMAS_VALIDAS


def test_plataformas_validas_sao_minusculas():
    for p in PLATAFORMAS_VALIDAS:
        assert p == p.lower()


def test_formatos_validos_nao_vazio():
    assert len(FORMATOS_VALIDOS) > 0


def test_formatos_validos_contem_reels():
    assert "reels" in FORMATOS_VALIDOS


# ---------------------------------------------------------------------------
# validar_texto
# ---------------------------------------------------------------------------

def test_validar_texto_ok():
    assert validar_texto("marketing digital") == "marketing digital"


def test_validar_texto_strip():
    assert validar_texto("  marketing  ") == "marketing"


def test_validar_texto_vazio_raise():
    with pytest.raises(ValidationError, match="pelo menos 1"):
        validar_texto("")


def test_validar_texto_apenas_espacos_raise():
    with pytest.raises(ValidationError, match="pelo menos 1"):
        validar_texto("   ")


def test_validar_texto_muito_longo_raise():
    with pytest.raises(ValidationError, match="máximo"):
        validar_texto("a" * 501)


def test_validar_texto_min_len_customizado():
    with pytest.raises(ValidationError, match="pelo menos 10"):
        validar_texto("curto", min_len=10)


def test_validar_texto_max_len_customizado():
    resultado = validar_texto("abc", max_len=5)
    assert resultado == "abc"


def test_validar_texto_nao_string_raise():
    with pytest.raises(ValidationError, match="string"):
        validar_texto(123)  # type: ignore


# ---------------------------------------------------------------------------
# validar_inteiro
# ---------------------------------------------------------------------------

def test_validar_inteiro_ok():
    assert validar_inteiro(5) == 5


def test_validar_inteiro_de_string():
    assert validar_inteiro("10") == 10


def test_validar_inteiro_abaixo_minimo_raise():
    with pytest.raises(ValidationError, match="pelo menos 1"):
        validar_inteiro(0)


def test_validar_inteiro_acima_maximo_raise():
    with pytest.raises(ValidationError, match="no máximo"):
        validar_inteiro(1001)


def test_validar_inteiro_nao_numerico_raise():
    with pytest.raises(ValidationError, match="número inteiro"):
        validar_inteiro("abc")


def test_validar_inteiro_limites_customizados():
    assert validar_inteiro(50, min_val=10, max_val=100) == 50


def test_validar_inteiro_no_limite_inferior():
    assert validar_inteiro(1, min_val=1, max_val=10) == 1


def test_validar_inteiro_no_limite_superior():
    assert validar_inteiro(10, min_val=1, max_val=10) == 10


# ---------------------------------------------------------------------------
# validar_float
# ---------------------------------------------------------------------------

def test_validar_float_ok():
    assert validar_float(3.14) == pytest.approx(3.14)


def test_validar_float_de_string():
    assert validar_float("2.5") == pytest.approx(2.5)


def test_validar_float_abaixo_minimo_raise():
    with pytest.raises(ValidationError, match="pelo menos"):
        validar_float(-1.0, min_val=0.0)


def test_validar_float_acima_maximo_raise():
    with pytest.raises(ValidationError, match="no máximo"):
        validar_float(101.0, max_val=100.0)


def test_validar_float_nao_numerico_raise():
    with pytest.raises(ValidationError, match="número"):
        validar_float("abc")


def test_validar_float_zero_permitido():
    assert validar_float(0.0, min_val=0.0) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# validar_arquivo
# ---------------------------------------------------------------------------

def test_validar_arquivo_ok(tmp_path):
    arquivo = tmp_path / "teste.md"
    arquivo.write_text("conteúdo de teste")
    resultado = validar_arquivo(str(arquivo))
    assert os.path.isabs(resultado)
    assert resultado == str(arquivo.resolve())


def test_validar_arquivo_extensao_valida(tmp_path):
    arquivo = tmp_path / "teste.md"
    arquivo.write_text("conteúdo de teste")
    resultado = validar_arquivo(str(arquivo), extensoes=[".md"])
    assert resultado.endswith(".md")


def test_validar_arquivo_extensao_invalida_raise(tmp_path):
    arquivo = tmp_path / "teste.txt"
    arquivo.write_text("conteúdo de teste")
    with pytest.raises(ValidationError, match="Extensão inválida"):
        validar_arquivo(str(arquivo), extensoes=[".md"])


def test_validar_arquivo_nao_existe_raise():
    with pytest.raises(ValidationError, match="não encontrado"):
        validar_arquivo("/caminho/inexistente/arquivo.md")


def test_validar_arquivo_vazio_raise(tmp_path):
    arquivo = tmp_path / "vazio.md"
    arquivo.write_text("")
    with pytest.raises(ValidationError, match="vazio"):
        validar_arquivo(str(arquivo))


def test_validar_arquivo_caminho_vazio_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_arquivo("")


def test_validar_arquivo_diretorio_raise(tmp_path):
    with pytest.raises(ValidationError, match="não é um arquivo"):
        validar_arquivo(str(tmp_path))


def test_validar_arquivo_extensao_sem_ponto(tmp_path):
    arquivo = tmp_path / "teste.md"
    arquivo.write_text("conteúdo")
    # Deve aceitar extensão com ou sem ponto
    resultado = validar_arquivo(str(arquivo), extensoes=["md"])
    assert resultado.endswith(".md")


# ---------------------------------------------------------------------------
# validar_diretorio_saida
# ---------------------------------------------------------------------------

def test_validar_diretorio_saida_existente(tmp_path):
    resultado = validar_diretorio_saida(str(tmp_path))
    assert os.path.isabs(resultado)


def test_validar_diretorio_saida_cria_novo(tmp_path):
    novo_dir = str(tmp_path / "novo" / "subdir")
    resultado = validar_diretorio_saida(novo_dir)
    assert os.path.isdir(resultado)


def test_validar_diretorio_saida_vazio_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_diretorio_saida("")


def test_validar_diretorio_saida_arquivo_existente_raise(tmp_path):
    arquivo = tmp_path / "nao_diretorio.txt"
    arquivo.write_text("conteúdo")
    with pytest.raises(ValidationError, match="não é um diretório"):
        validar_diretorio_saida(str(arquivo))


# ---------------------------------------------------------------------------
# validar_plataforma
# ---------------------------------------------------------------------------

def test_validar_plataforma_instagram():
    assert validar_plataforma("instagram") == "instagram"


def test_validar_plataforma_case_insensitive():
    assert validar_plataforma("Instagram") == "instagram"
    assert validar_plataforma("TIKTOK") == "tiktok"


def test_validar_plataforma_invalida_raise():
    with pytest.raises(ValidationError, match="Plataforma inválida"):
        validar_plataforma("snapchat")


def test_validar_plataforma_vazia_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_plataforma("")


def test_validar_plataforma_todas_validas():
    for p in PLATAFORMAS_VALIDAS:
        assert validar_plataforma(p) == p


# ---------------------------------------------------------------------------
# validar_lista_plataformas
# ---------------------------------------------------------------------------

def test_validar_lista_plataformas_ok():
    resultado = validar_lista_plataformas(["instagram", "tiktok"])
    assert "instagram" in resultado
    assert "tiktok" in resultado


def test_validar_lista_plataformas_remove_duplicatas():
    resultado = validar_lista_plataformas(["instagram", "instagram", "tiktok"])
    assert resultado.count("instagram") == 1
    assert len(resultado) == 2


def test_validar_lista_plataformas_vazia_raise():
    with pytest.raises(ValidationError, match="não pode ser uma lista vazia"):
        validar_lista_plataformas([])


def test_validar_lista_plataformas_invalida_raise():
    with pytest.raises(ValidationError, match="Plataforma inválida"):
        validar_lista_plataformas(["instagram", "myspace"])


# ---------------------------------------------------------------------------
# validar_formato
# ---------------------------------------------------------------------------

def test_validar_formato_reels():
    assert validar_formato("reels") == "reels"


def test_validar_formato_case_insensitive():
    assert validar_formato("REELS") == "reels"


def test_validar_formato_invalido_raise():
    with pytest.raises(ValidationError, match="Formato inválido"):
        validar_formato("stories_animados")


def test_validar_formato_vazio_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_formato("")


def test_validar_formato_todos_validos():
    for f in FORMATOS_VALIDOS:
        assert validar_formato(f) == f


# ---------------------------------------------------------------------------
# validar_data
# ---------------------------------------------------------------------------

def test_validar_data_ok():
    from datetime import datetime
    resultado = validar_data("2026-02-17")
    assert isinstance(resultado, datetime)
    assert resultado.year == 2026
    assert resultado.month == 2
    assert resultado.day == 17


def test_validar_data_formato_invalido_raise():
    with pytest.raises(ValidationError, match="não é uma data válida"):
        validar_data("17/02/2026")


def test_validar_data_valor_invalido_raise():
    with pytest.raises(ValidationError, match="não é uma data válida"):
        validar_data("2026-13-01")


def test_validar_data_vazia_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_data("")


def test_validar_data_formato_customizado():
    from datetime import datetime
    resultado = validar_data("17/02/2026", formato="%d/%m/%Y")
    assert isinstance(resultado, datetime)
    assert resultado.year == 2026


# ---------------------------------------------------------------------------
# validar_semana_iso
# ---------------------------------------------------------------------------

def test_validar_semana_iso_ok():
    assert validar_semana_iso("2026-W07") == "2026-W07"


def test_validar_semana_iso_semana_01():
    assert validar_semana_iso("2026-W01") == "2026-W01"


def test_validar_semana_iso_semana_53():
    assert validar_semana_iso("2015-W53") == "2015-W53"


def test_validar_semana_iso_formato_invalido_raise():
    with pytest.raises(ValidationError, match="semana ISO válida"):
        validar_semana_iso("2026-7")


def test_validar_semana_iso_semana_54_raise():
    with pytest.raises(ValidationError, match="semana ISO válida"):
        validar_semana_iso("2026-W54")


def test_validar_semana_iso_semana_00_raise():
    with pytest.raises(ValidationError, match="semana ISO válida"):
        validar_semana_iso("2026-W00")


def test_validar_semana_iso_vazia_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_semana_iso("")


# ---------------------------------------------------------------------------
# validar_url
# ---------------------------------------------------------------------------

def test_validar_url_http():
    assert validar_url("http://example.com") == "http://example.com"


def test_validar_url_https():
    assert validar_url("https://example.com/path?q=1") == "https://example.com/path?q=1"


def test_validar_url_invalida_raise():
    with pytest.raises(ValidationError, match="não é uma URL válida"):
        validar_url("nao-e-url")


def test_validar_url_sem_protocolo_raise():
    with pytest.raises(ValidationError, match="não é uma URL válida"):
        validar_url("example.com")


def test_validar_url_vazia_raise():
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        validar_url("")


def test_validar_url_localhost():
    assert validar_url("http://localhost:8080") == "http://localhost:8080"


# ---------------------------------------------------------------------------
# handle_validation_error
# ---------------------------------------------------------------------------

def test_handle_validation_error_encerra_processo():
    with pytest.raises(SystemExit) as exc_info:
        handle_validation_error(ValidationError("erro de teste"))
    assert exc_info.value.code == 1


def test_handle_validation_error_com_uso():
    with pytest.raises(SystemExit) as exc_info:
        handle_validation_error(
            ValidationError("campo inválido"),
            mostrar_uso="Uso: script.py <argumento>"
        )
    assert exc_info.value.code == 1
