#!/usr/bin/env python3
"""
Módulo de validação de entrada para scripts do Marketing OS.
Fornece funções reutilizáveis para validar argumentos de linha de comando.
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Optional


# Plataformas suportadas no Marketing OS
PLATAFORMAS_VALIDAS = {
    "instagram", "tiktok", "youtube", "shorts", "linkedin",
    "twitter", "reels", "x", "facebook", "pinterest",
}

# Formatos de conteúdo válidos
FORMATOS_VALIDOS = {
    "reels", "carrossel", "post", "stories", "tutorial",
    "shorts", "video", "artigo", "newsletter", "thread",
}

# Limites de tamanho de arquivo (bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class ValidationError(ValueError):
    """Erro de validação de entrada."""
    pass


# ---------------------------------------------------------------------------
# Validação de texto
# ---------------------------------------------------------------------------

def validar_texto(valor: str, campo: str = "texto", min_len: int = 1, max_len: int = 500) -> str:
    """
    Valida uma string de texto.

    Args:
        valor: Valor a validar.
        campo: Nome do campo (para mensagens de erro).
        min_len: Comprimento mínimo permitido.
        max_len: Comprimento máximo permitido.

    Returns:
        Texto validado (sem espaços extras nas bordas).

    Raises:
        ValidationError: Se a validação falhar.
    """
    if not isinstance(valor, str):
        raise ValidationError(f"'{campo}' deve ser uma string, recebeu: {type(valor).__name__}")

    valor = valor.strip()

    if len(valor) < min_len:
        raise ValidationError(
            f"'{campo}' deve ter pelo menos {min_len} caractere(s). Recebeu: '{valor}'"
        )

    if len(valor) > max_len:
        raise ValidationError(
            f"'{campo}' deve ter no máximo {max_len} caracteres. Recebeu {len(valor)} caracteres."
        )

    return valor


# ---------------------------------------------------------------------------
# Validação numérica
# ---------------------------------------------------------------------------

def validar_inteiro(valor, campo: str = "número", min_val: int = 1, max_val: int = 1000) -> int:
    """
    Valida e converte um valor para inteiro dentro de um intervalo.

    Args:
        valor: Valor a validar (string ou int).
        campo: Nome do campo (para mensagens de erro).
        min_val: Valor mínimo permitido (inclusive).
        max_val: Valor máximo permitido (inclusive).

    Returns:
        Inteiro validado.

    Raises:
        ValidationError: Se a validação falhar.
    """
    try:
        inteiro = int(valor)
    except (TypeError, ValueError):
        raise ValidationError(
            f"'{campo}' deve ser um número inteiro. Recebeu: '{valor}'"
        )

    if inteiro < min_val:
        raise ValidationError(
            f"'{campo}' deve ser pelo menos {min_val}. Recebeu: {inteiro}"
        )

    if inteiro > max_val:
        raise ValidationError(
            f"'{campo}' deve ser no máximo {max_val}. Recebeu: {inteiro}"
        )

    return inteiro


def validar_float(valor, campo: str = "número", min_val: float = 0.0, max_val: float = 100.0) -> float:
    """
    Valida e converte um valor para float dentro de um intervalo.

    Args:
        valor: Valor a validar (string ou float).
        campo: Nome do campo (para mensagens de erro).
        min_val: Valor mínimo permitido (inclusive).
        max_val: Valor máximo permitido (inclusive).

    Returns:
        Float validado.

    Raises:
        ValidationError: Se a validação falhar.
    """
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ValidationError(
            f"'{campo}' deve ser um número. Recebeu: '{valor}'"
        )

    if numero < min_val:
        raise ValidationError(
            f"'{campo}' deve ser pelo menos {min_val}. Recebeu: {numero}"
        )

    if numero > max_val:
        raise ValidationError(
            f"'{campo}' deve ser no máximo {max_val}. Recebeu: {numero}"
        )

    return numero


# ---------------------------------------------------------------------------
# Validação de arquivo
# ---------------------------------------------------------------------------

def validar_arquivo(caminho: str, extensoes: Optional[List[str]] = None, campo: str = "arquivo") -> str:
    """
    Valida que um caminho de arquivo existe, é legível e tem extensão permitida.

    Args:
        caminho: Caminho do arquivo a validar.
        extensoes: Lista de extensões permitidas (ex: ['.md', '.txt']). None = qualquer extensão.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        Caminho absoluto validado.

    Raises:
        ValidationError: Se a validação falhar.
    """
    if not caminho or not caminho.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    caminho = caminho.strip()

    if not os.path.exists(caminho):
        raise ValidationError(f"Arquivo não encontrado: '{caminho}'")

    if not os.path.isfile(caminho):
        raise ValidationError(f"'{caminho}' não é um arquivo (pode ser um diretório).")

    if not os.access(caminho, os.R_OK):
        raise ValidationError(f"Sem permissão de leitura para: '{caminho}'")

    tamanho = os.path.getsize(caminho)
    if tamanho == 0:
        raise ValidationError(f"O arquivo está vazio: '{caminho}'")

    if tamanho > MAX_FILE_SIZE:
        raise ValidationError(
            f"Arquivo muito grande: '{caminho}' ({tamanho / 1024 / 1024:.1f} MB). "
            f"Máximo permitido: {MAX_FILE_SIZE / 1024 / 1024:.0f} MB."
        )

    if extensoes:
        _, ext = os.path.splitext(caminho)
        extensoes_norm = [e.lower() if e.startswith('.') else f'.{e.lower()}' for e in extensoes]
        if ext.lower() not in extensoes_norm:
            raise ValidationError(
                f"Extensão inválida para '{campo}': '{ext}'. "
                f"Extensões permitidas: {', '.join(extensoes_norm)}"
            )

    return os.path.abspath(caminho)


# ---------------------------------------------------------------------------
# Validação de diretório de saída
# ---------------------------------------------------------------------------

def validar_diretorio_saida(caminho: str, campo: str = "diretório de saída") -> str:
    """
    Valida um diretório de saída, criando-o se necessário.

    Args:
        caminho: Caminho do diretório.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        Caminho absoluto do diretório.

    Raises:
        ValidationError: Se a validação falhar.
    """
    if not caminho or not caminho.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    caminho = caminho.strip()

    if os.path.exists(caminho) and not os.path.isdir(caminho):
        raise ValidationError(f"'{caminho}' existe mas não é um diretório.")

    if not os.path.exists(caminho):
        try:
            os.makedirs(caminho, exist_ok=True)
        except OSError as e:
            raise ValidationError(f"Não foi possível criar o diretório '{caminho}': {e}")

    if not os.access(caminho, os.W_OK):
        raise ValidationError(f"Sem permissão de escrita no diretório: '{caminho}'")

    return os.path.abspath(caminho)


# ---------------------------------------------------------------------------
# Validação de plataforma
# ---------------------------------------------------------------------------

def validar_plataforma(plataforma: str, campo: str = "plataforma") -> str:
    """
    Valida que a plataforma é suportada pelo Marketing OS.

    Args:
        plataforma: Nome da plataforma.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        Plataforma em letras minúsculas validada.

    Raises:
        ValidationError: Se a plataforma não for suportada.
    """
    if not plataforma or not plataforma.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    plataforma = plataforma.strip().lower()

    if plataforma not in PLATAFORMAS_VALIDAS:
        raise ValidationError(
            f"Plataforma inválida: '{plataforma}'. "
            f"Plataformas suportadas: {', '.join(sorted(PLATAFORMAS_VALIDAS))}"
        )

    return plataforma


def validar_lista_plataformas(plataformas: List[str], campo: str = "plataformas") -> List[str]:
    """
    Valida uma lista de plataformas, removendo duplicatas.

    Args:
        plataformas: Lista de plataformas a validar.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        Lista de plataformas validadas (sem duplicatas, em minúsculas).

    Raises:
        ValidationError: Se alguma plataforma for inválida.
    """
    if not plataformas:
        raise ValidationError(f"'{campo}' não pode ser uma lista vazia.")

    resultado = []
    vistas = set()
    for p in plataformas:
        p_validada = validar_plataforma(p, campo=campo)
        if p_validada not in vistas:
            resultado.append(p_validada)
            vistas.add(p_validada)

    return resultado


# ---------------------------------------------------------------------------
# Validação de formato de conteúdo
# ---------------------------------------------------------------------------

def validar_formato(formato: str, campo: str = "formato") -> str:
    """
    Valida um formato de conteúdo.

    Args:
        formato: Formato de conteúdo.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        Formato em letras minúsculas validado.

    Raises:
        ValidationError: Se o formato não for reconhecido.
    """
    if not formato or not formato.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    formato = formato.strip().lower()

    if formato not in FORMATOS_VALIDOS:
        raise ValidationError(
            f"Formato inválido: '{formato}'. "
            f"Formatos suportados: {', '.join(sorted(FORMATOS_VALIDOS))}"
        )

    return formato


# ---------------------------------------------------------------------------
# Validação de data
# ---------------------------------------------------------------------------

def validar_data(data_str: str, campo: str = "data", formato: str = "%Y-%m-%d") -> datetime:
    """
    Valida e converte uma string de data.

    Args:
        data_str: String de data a validar.
        campo: Nome do campo (para mensagens de erro).
        formato: Formato esperado da data (padrão: YYYY-MM-DD).

    Returns:
        Objeto datetime validado.

    Raises:
        ValidationError: Se a data for inválida.
    """
    if not data_str or not data_str.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    data_str = data_str.strip()

    try:
        return datetime.strptime(data_str, formato)
    except ValueError:
        raise ValidationError(
            f"'{campo}' com valor '{data_str}' não é uma data válida. "
            f"Formato esperado: {formato} (ex: {datetime.now().strftime(formato)})"
        )


def validar_semana_iso(semana_str: str, campo: str = "semana") -> str:
    """
    Valida o formato de semana ISO (YYYY-Www).

    Args:
        semana_str: String no formato YYYY-Www.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        String da semana validada.

    Raises:
        ValidationError: Se o formato for inválido.
    """
    if not semana_str or not semana_str.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    semana_str = semana_str.strip()

    padrao = re.compile(r'^\d{4}-W(0[1-9]|[1-4]\d|5[0-3])$')
    if not padrao.match(semana_str):
        raise ValidationError(
            f"'{campo}' com valor '{semana_str}' não é uma semana ISO válida. "
            f"Formato esperado: YYYY-Www (ex: 2026-W07)"
        )

    return semana_str


# ---------------------------------------------------------------------------
# Validação de URL
# ---------------------------------------------------------------------------

def validar_url(url: str, campo: str = "URL") -> str:
    """
    Valida o formato básico de uma URL.

    Args:
        url: URL a validar.
        campo: Nome do campo (para mensagens de erro).

    Returns:
        URL validada.

    Raises:
        ValidationError: Se a URL for inválida.
    """
    if not url or not url.strip():
        raise ValidationError(f"'{campo}' não pode ser vazio.")

    url = url.strip()

    padrao = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )

    if not padrao.match(url):
        raise ValidationError(
            f"'{campo}' com valor '{url}' não é uma URL válida. "
            f"Exemplo: https://example.com"
        )

    return url


# ---------------------------------------------------------------------------
# Handler de erro para CLI
# ---------------------------------------------------------------------------

def handle_validation_error(error: ValidationError, mostrar_uso: Optional[str] = None) -> None:
    """
    Imprime uma mensagem de erro formatada e encerra o processo.

    Args:
        error: Erro de validação.
        mostrar_uso: String de uso a exibir após o erro (opcional).
    """
    print(f"\n❌ Erro de validação: {error}", file=sys.stderr)
    if mostrar_uso:
        print(f"\n{mostrar_uso}", file=sys.stderr)
    sys.exit(1)
