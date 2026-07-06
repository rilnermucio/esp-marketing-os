#!/usr/bin/env python3
"""
Apify API Integration — wrapper do Run-Sync API.

Autenticação: token via APIFY_TOKEN. Sem token, scripts dependentes
(apify_serp.py, apify_instagram.py) degradam graciosamente.

Não tem CLI próprio. É importado pelos scripts apify_*.py.

Uso programático:
    from apify_client import run_actor_sync, _get_token, save_result
    token = _get_token()
    items = run_actor_sync(
        "apify/google-search-scraper",
        {"queries": ["x"], "resultsPerPage": 10},
        token=token,
    )

Documentação Apify: https://docs.apify.com/api/v2
"""

import json
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

APIFY_API_BASE = "https://api.apify.com/v2"
ENV_TOKEN = "APIFY_TOKEN"

# Estimativas de custo (USD por unidade). Heurísticas conservadoras
# baseadas em pricing público dos Actors em maio/2026.
# Formato: actor_id -> (campo do input, custo por unidade, campo opcional de multiplicador)
_COST_RATES = {
    "apify/google-search-scraper": {
        "list_field": "queries",
        "multiplier_field": "resultsPerPage",
        "rate_per_result": 0.005,
        "default_multiplier": 10,
    },
    "apify/instagram-scraper": {
        "list_field": "directUrls",
        "multiplier_field": "resultsLimit",
        "rate_per_result": 0.0023,
        "default_multiplier": 30,
    },
    "curious_coder/facebook-ads-library-scraper": {
        "list_field": "urls",
        "multiplier_field": "count",
        "rate_per_result": 0.0015,
        "default_multiplier": 30,
    },
    "clockworks/free-tiktok-scraper": {
        "list_field": "profiles",
        "multiplier_field": "resultsPerPage",
        "rate_per_result": 0.0,  # Free Actor — sem custo de API
        "default_multiplier": 30,
    },
    "streamers/youtube-scraper": {
        "list_field": "startUrls",
        "multiplier_field": "maxResults",
        "rate_per_result": 0.005,
        "default_multiplier": 20,
    },
}


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------


class ApifyAPIError(Exception):
    """Erro genérico da Apify API."""

    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status

    def __str__(self) -> str:
        base = super().__str__()
        prefix = f"[HTTP {self.status}] " if self.status else ""
        return f"{prefix}{base}"


class ApifyAuthError(ApifyAPIError):
    """Token inválido ou ausente."""


class ApifyRateLimitError(ApifyAPIError):
    """Rate limit ou quota excedida."""


class ApifyTimeoutError(ApifyAPIError):
    """Execução demorou mais que o timeout."""


# ---------------------------------------------------------------------------
# Funções internas
# ---------------------------------------------------------------------------


def _get_token() -> str:
    """Carrega APIFY_TOKEN do ambiente. Raise ApifyAuthError se ausente."""
    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        raise ApifyAuthError(
            f"{ENV_TOKEN} não configurado. Defina a variável de ambiente "
            f"para usar scraping via Apify."
        )
    return token


def _actor_url(actor_id: str) -> str:
    """
    Converte actor ID 'apify/google-search-scraper' em URL completa.

    Apify usa '~' como separador no path em vez de '/' (URL-friendly).
    """
    safe_id = actor_id.replace("/", "~")
    return f"{APIFY_API_BASE}/acts/{safe_id}/run-sync-get-dataset-items"


def _http_post_json(
    url: str, data: bytes, headers: Dict[str, str], timeout: int
) -> List[Dict[str, Any]]:
    """
    POST JSON, parseia resposta como lista de items.

    Mapeia erros HTTP/rede para Apify*Error apropriado.
    """
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            if not body.strip():
                return []
            parsed = json.loads(body)
            if isinstance(parsed, list):
                return parsed
            return [parsed]  # Caso retorne dict único
    except urllib.error.HTTPError as e:
        msg = ""
        try:
            msg = e.read().decode("utf-8")[:500]
        except Exception:
            pass
        if e.code == 401:
            raise ApifyAuthError(f"Token inválido. {msg}", status=401) from e
        if e.code == 429:
            raise ApifyRateLimitError(f"Rate limit excedido. {msg}", status=429) from e
        raise ApifyAPIError(f"HTTP {e.code}: {msg}", status=e.code) from e
    except socket.timeout as e:
        raise ApifyTimeoutError(f"Timeout após {timeout}s") from e
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            raise ApifyTimeoutError(f"Timeout após {timeout}s") from e
        raise ApifyAPIError(f"Erro de rede: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise ApifyAPIError(f"Resposta JSON inválida: {e}") from e


# ---------------------------------------------------------------------------
# Funções públicas
# ---------------------------------------------------------------------------


def run_actor_sync(
    actor_id: str,
    input_data: Dict[str, Any],
    token: str,
    timeout: int = 60,
) -> List[Dict[str, Any]]:
    """
    Executa um Actor do Apify de forma síncrona e retorna o dataset.

    Args:
        actor_id: ID no formato 'username/name' (ex: 'apify/google-search-scraper').
        input_data: Input do Actor (varia por Actor; ver docs do Actor no Apify).
        token: APIFY_TOKEN.
        timeout: Timeout em segundos (default 60).

    Returns:
        Lista de items do dataset. Estrutura varia por Actor.

    Raises:
        ApifyAuthError: 401.
        ApifyRateLimitError: 429.
        ApifyTimeoutError: timeout de rede.
        ApifyAPIError: outros erros HTTP/rede/parsing.
    """
    url = _actor_url(actor_id)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = json.dumps(input_data).encode("utf-8")
    return _http_post_json(url, data, headers, timeout)


def estimate_cost(actor_id: str, input_data: Dict[str, Any]) -> float:
    """
    Estima custo em USD da execução. Heurística — preço real pode variar.

    Returns:
        Estimativa em USD arredondada a 4 casas. 0.0 se Actor desconhecido.
    """
    config = _COST_RATES.get(actor_id)
    if not config:
        return 0.0

    list_field = config["list_field"]
    multiplier_field = config["multiplier_field"]
    rate = config["rate_per_result"]
    default_multiplier = config["default_multiplier"]

    raw_list = input_data.get(list_field, [])
    n_items = len(raw_list) if isinstance(raw_list, list) and raw_list else 1

    raw_mult = input_data.get(multiplier_field, default_multiplier)
    if isinstance(raw_mult, int) and raw_mult > 0:
        multiplier = raw_mult
    else:
        multiplier = default_multiplier

    return round(n_items * multiplier * rate, 4)


def _slugify(text: str, max_length: int = 50) -> str:
    """Converte texto em slug seguro para filename."""
    if not text:
        return "result"
    slug = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return slug[:max_length] or "result"


def save_result(data: Dict[str, Any], slug: str, output_dir: str) -> str:
    """
    Salva resultado em <output_dir>/<timestamp>-<slug>.json.

    Args:
        data: Dicionário JSON-serializável.
        slug: Identificador legível (será slugificado).
        output_dir: Diretório de saída (criado se não existir).

    Returns:
        Caminho absoluto do arquivo criado.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    safe_slug = _slugify(slug)
    filename = f"{timestamp}-{safe_slug}.json"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return os.path.abspath(path)
