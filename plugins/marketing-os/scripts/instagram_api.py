#!/usr/bin/env python3
"""
Instagram Business API Integration
Integração com a Meta Graph API para gerenciar conta Instagram Business.

Autenticação: token de acesso de longa duração (Long-Lived Access Token).
Defina a variável de ambiente INSTAGRAM_ACCESS_TOKEN antes de usar.

Uso:
    python instagram_api.py insights <account_id>
    python instagram_api.py account <account_id>
    python instagram_api.py audience <account_id>
    python instagram_api.py posts <account_id> [--limit 10]
    python instagram_api.py publish-photo <account_id> <image_url> <caption>
    python instagram_api.py publish-carousel <account_id> <caption> <url1> [url2...]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from validators import (
    ValidationError,
    validar_inteiro,
    validar_texto,
    validar_url,
    handle_validation_error,
)

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

GRAPH_API_BASE = "https://graph.facebook.com/v18.0"
ENV_TOKEN = "INSTAGRAM_ACCESS_TOKEN"

# Métricas disponíveis para posts
METRICAS_POST = [
    "impressions",
    "reach",
    "engagement",
    "saved",
    "video_views",
    "likes",
    "comments",
    "shares",
]

# Métricas disponíveis para a conta
METRICAS_CONTA = [
    "impressions",
    "reach",
    "profile_views",
    "website_clicks",
    "follower_count",
]

# Granularidades de período
PERIODOS_VALIDOS = {"day", "week", "days_28", "month", "lifetime"}


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------


class InstagramAPIError(Exception):
    """Erro retornado pela API do Instagram/Meta."""

    def __init__(
        self, message: str, code: Optional[int] = None, subcode: Optional[int] = None
    ):
        super().__init__(message)
        self.code = code
        self.subcode = subcode

    def __str__(self):
        base = super().__str__()
        if self.code:
            return f"[{self.code}] {base}"
        return base


class InstagramAuthError(InstagramAPIError):
    """Erro de autenticação (token inválido ou expirado)."""


# ---------------------------------------------------------------------------
# Cliente HTTP mínimo (sem dependências externas)
# ---------------------------------------------------------------------------


def _get(url: str, params: Dict[str, Any]) -> Dict:
    """Faz uma requisição GET e retorna o JSON."""
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"

    try:
        with urllib.request.urlopen(full_url, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body)
            msg = err.get("error", {}).get("message", body)
            code = err.get("error", {}).get("code")
            subcode = err.get("error", {}).get("error_subcode")
            if code in (190, 102, 104):
                raise InstagramAuthError(msg, code=code, subcode=subcode)
            raise InstagramAPIError(msg, code=code, subcode=subcode)
        except (json.JSONDecodeError, KeyError):
            raise InstagramAPIError(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise InstagramAPIError(f"Erro de conexão: {e.reason}")

    if "error" in data:
        err = data["error"]
        msg = err.get("message", str(data))
        code = err.get("code")
        subcode = err.get("error_subcode")
        if code in (190, 102, 104):
            raise InstagramAuthError(msg, code=code, subcode=subcode)
        raise InstagramAPIError(msg, code=code, subcode=subcode)

    return data


def _post(url: str, params: Dict[str, Any]) -> Dict:
    """Faz uma requisição POST e retorna o JSON."""
    data = urllib.parse.urlencode(params).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body)
            msg = err.get("error", {}).get("message", body)
            code = err.get("error", {}).get("code")
            subcode = err.get("error", {}).get("error_subcode")
            if code in (190, 102, 104):
                raise InstagramAuthError(msg, code=code, subcode=subcode)
            raise InstagramAPIError(msg, code=code, subcode=subcode)
        except (json.JSONDecodeError, KeyError):
            raise InstagramAPIError(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise InstagramAPIError(f"Erro de conexão: {e.reason}")

    if "error" in result:
        err = result["error"]
        msg = err.get("message", str(result))
        code = err.get("code")
        subcode = err.get("error_subcode")
        if code in (190, 102, 104):
            raise InstagramAuthError(msg, code=code, subcode=subcode)
        raise InstagramAPIError(msg, code=code, subcode=subcode)

    return result


# ---------------------------------------------------------------------------
# Funções principais da API
# ---------------------------------------------------------------------------


def get_account_insights(
    account_id: str,
    token: str,
    metrics: Optional[List[str]] = None,
    period: str = "day",
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> Dict:
    """
    Retorna insights da conta Instagram Business.

    Args:
        account_id: ID da conta Instagram Business.
        token: Token de acesso de longa duração.
        metrics: Lista de métricas. Padrão: todas as métricas de conta.
        period: Granularidade ('day', 'week', 'days_28', 'month', 'lifetime').
        since: Data de início (Unix timestamp ou YYYY-MM-DD).
        until: Data de fim (Unix timestamp ou YYYY-MM-DD).

    Returns:
        Dicionário com dados de insights.
    """
    if metrics is None:
        metrics = METRICAS_CONTA

    params: Dict[str, Any] = {
        "metric": ",".join(metrics),
        "period": period,
        "access_token": token,
    }
    if since:
        params["since"] = since
    if until:
        params["until"] = until

    url = f"{GRAPH_API_BASE}/{account_id}/insights"
    return _get(url, params)


def get_insights(
    media_id: str,
    token: str,
    metrics: Optional[List[str]] = None,
) -> Dict:
    """
    Retorna insights de um post/mídia específico.

    Args:
        media_id: ID do post/mídia.
        token: Token de acesso de longa duração.
        metrics: Lista de métricas. Padrão: todas as métricas de post.

    Returns:
        Dicionário com dados de insights do post.
    """
    if metrics is None:
        metrics = METRICAS_POST

    params: Dict[str, Any] = {
        "metric": ",".join(metrics),
        "access_token": token,
    }

    url = f"{GRAPH_API_BASE}/{media_id}/insights"
    return _get(url, params)


def get_audience_demographics(account_id: str, token: str) -> Dict:
    """
    Retorna dados demográficos da audiência.

    Args:
        account_id: ID da conta Instagram Business.
        token: Token de acesso de longa duração.

    Returns:
        Dicionário com dados demográficos (faixa etária, gênero, localização).
    """
    metrics = [
        "audience_city",
        "audience_country",
        "audience_gender_age",
        "audience_locale",
    ]
    params: Dict[str, Any] = {
        "metric": ",".join(metrics),
        "period": "lifetime",
        "access_token": token,
    }

    url = f"{GRAPH_API_BASE}/{account_id}/insights"
    return _get(url, params)


def get_recent_posts(account_id: str, token: str, limit: int = 10) -> Dict:
    """
    Retorna posts recentes da conta.

    Args:
        account_id: ID da conta Instagram Business.
        token: Token de acesso de longa duração.
        limit: Número máximo de posts a retornar (1-100).

    Returns:
        Dicionário com lista de posts e metadados.
    """
    fields = "id,caption,media_type,media_url,thumbnail_url,timestamp,like_count,comments_count,permalink"
    params: Dict[str, Any] = {
        "fields": fields,
        "limit": max(1, min(limit, 100)),
        "access_token": token,
    }

    url = f"{GRAPH_API_BASE}/{account_id}/media"
    return _get(url, params)


def publish_photo(
    account_id: str,
    token: str,
    image_url: str,
    caption: str,
) -> Dict:
    """
    Publica uma foto no Instagram Business (fluxo de 2 etapas: criar container → publicar).

    Args:
        account_id: ID da conta Instagram Business.
        token: Token de acesso de longa duração.
        image_url: URL pública da imagem (JPEG/PNG acessível publicamente).
        caption: Legenda do post.

    Returns:
        Dicionário com {'creation_id': ..., 'id': ...} do post publicado.
    """
    # Etapa 1: criar container de mídia
    container_url = f"{GRAPH_API_BASE}/{account_id}/media"
    container_params: Dict[str, Any] = {
        "image_url": image_url,
        "caption": caption,
        "access_token": token,
    }
    container = _post(container_url, container_params)
    creation_id = container.get("id")
    if not creation_id:
        raise InstagramAPIError("Falha ao criar container de mídia: ID não retornado.")

    # Etapa 2: publicar o container
    publish_url = f"{GRAPH_API_BASE}/{account_id}/media_publish"
    publish_params: Dict[str, Any] = {
        "creation_id": creation_id,
        "access_token": token,
    }
    result = _post(publish_url, publish_params)
    result["creation_id"] = creation_id
    return result


def publish_carousel(
    account_id: str,
    token: str,
    caption: str,
    image_urls: List[str],
) -> Dict:
    """
    Publica um carrossel no Instagram Business.

    Args:
        account_id: ID da conta Instagram Business.
        token: Token de acesso de longa duração.
        caption: Legenda do carrossel.
        image_urls: Lista de URLs das imagens (2-10 imagens).

    Returns:
        Dicionário com o ID do carrossel publicado.
    """
    if not (2 <= len(image_urls) <= 10):
        raise ValidationError(
            f"Carrossel deve ter entre 2 e 10 imagens. Recebeu: {len(image_urls)}"
        )

    # Etapa 1: criar containers para cada imagem
    children_ids = []
    for idx, img_url in enumerate(image_urls):
        child_url = f"{GRAPH_API_BASE}/{account_id}/media"
        child_params: Dict[str, Any] = {
            "image_url": img_url,
            "is_carousel_item": "true",
            "access_token": token,
        }
        child = _post(child_url, child_params)
        child_id = child.get("id")
        if not child_id:
            raise InstagramAPIError(f"Falha ao criar container para imagem {idx + 1}.")
        children_ids.append(child_id)

    # Etapa 2: criar container do carrossel
    carousel_url = f"{GRAPH_API_BASE}/{account_id}/media"
    carousel_params: Dict[str, Any] = {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "caption": caption,
        "access_token": token,
    }
    carousel = _post(carousel_url, carousel_params)
    creation_id = carousel.get("id")
    if not creation_id:
        raise InstagramAPIError("Falha ao criar container do carrossel.")

    # Etapa 3: publicar o carrossel
    publish_url = f"{GRAPH_API_BASE}/{account_id}/media_publish"
    publish_params: Dict[str, Any] = {
        "creation_id": creation_id,
        "access_token": token,
    }
    result = _post(publish_url, publish_params)
    result["creation_id"] = creation_id
    result["children_ids"] = children_ids
    return result


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------


def get_token() -> str:
    """Lê o token da variável de ambiente INSTAGRAM_ACCESS_TOKEN."""
    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"\n❌ Token não encontrado. Defina a variável de ambiente:\n"
            f"   export {ENV_TOKEN}='seu_token_aqui'\n",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def print_json(data: Any) -> None:
    """Imprime dados formatados como JSON."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Instagram Business API — Marketing OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Variável de ambiente obrigatória:\n"
            f"  {ENV_TOKEN}   Token de acesso de longa duração\n\n"
            "Exemplos:\n"
            "  python instagram_api.py insights 17841400008460056\n"
            "  python instagram_api.py posts 17841400008460056 --limit 5\n"
            "  python instagram_api.py publish-photo 178414... https://... 'Minha legenda'\n"
        ),
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    # insights
    p_insights = sub.add_parser("insights", help="Retorna insights da conta")
    p_insights.add_argument("account_id", help="ID da conta Instagram Business")
    p_insights.add_argument(
        "--period",
        default="day",
        choices=list(PERIODOS_VALIDOS),
        help="Granularidade do período",
    )
    p_insights.add_argument("--since", help="Data de início (YYYY-MM-DD)")
    p_insights.add_argument("--until", help="Data de fim (YYYY-MM-DD)")

    # account
    p_account = sub.add_parser("account", help="Informações básicas da conta")
    p_account.add_argument("account_id", help="ID da conta Instagram Business")

    # audience
    p_audience = sub.add_parser("audience", help="Dados demográficos da audiência")
    p_audience.add_argument("account_id", help="ID da conta Instagram Business")

    # posts
    p_posts = sub.add_parser("posts", help="Posts recentes da conta")
    p_posts.add_argument("account_id", help="ID da conta Instagram Business")
    p_posts.add_argument(
        "--limit", type=int, default=10, help="Número de posts (1-100)"
    )

    # publish-photo
    p_photo = sub.add_parser("publish-photo", help="Publica uma foto")
    p_photo.add_argument("account_id", help="ID da conta Instagram Business")
    p_photo.add_argument("image_url", help="URL pública da imagem")
    p_photo.add_argument("caption", help="Legenda do post")

    # publish-carousel
    p_carousel = sub.add_parser(
        "publish-carousel", help="Publica um carrossel (2-10 imagens)"
    )
    p_carousel.add_argument("account_id", help="ID da conta Instagram Business")
    p_carousel.add_argument("caption", help="Legenda do carrossel")
    p_carousel.add_argument("image_urls", nargs="+", help="URLs das imagens (2-10)")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    token = get_token()

    try:
        if args.comando == "insights":
            validar_texto(args.account_id, campo="account_id", max_len=50)
            data = get_account_insights(
                args.account_id,
                token,
                period=args.period,
                since=getattr(args, "since", None),
                until=getattr(args, "until", None),
            )
            print_json(data)

        elif args.comando == "account":
            validar_texto(args.account_id, campo="account_id", max_len=50)
            params = {
                "fields": "id,name,biography,followers_count,follows_count,media_count,website,profile_picture_url",
                "access_token": token,
            }
            data = _get(f"{GRAPH_API_BASE}/{args.account_id}", params)
            print_json(data)

        elif args.comando == "audience":
            validar_texto(args.account_id, campo="account_id", max_len=50)
            data = get_audience_demographics(args.account_id, token)
            print_json(data)

        elif args.comando == "posts":
            validar_texto(args.account_id, campo="account_id", max_len=50)
            limit = validar_inteiro(args.limit, campo="limit", min_val=1, max_val=100)
            data = get_recent_posts(args.account_id, token, limit=limit)
            print_json(data)

        elif args.comando == "publish-photo":
            validar_texto(args.account_id, campo="account_id", max_len=50)
            validar_url(args.image_url, campo="image_url")
            validar_texto(args.caption, campo="caption", max_len=2200)
            result = publish_photo(args.account_id, token, args.image_url, args.caption)
            print(f"\n✅ Foto publicada com sucesso! ID: {result.get('id')}")
            print_json(result)

        elif args.comando == "publish-carousel":
            validar_texto(args.account_id, campo="account_id", max_len=50)
            validar_texto(args.caption, campo="caption", max_len=2200)
            for idx, url in enumerate(args.image_urls):
                validar_url(url, campo=f"image_url[{idx}]")
            result = publish_carousel(
                args.account_id, token, args.caption, args.image_urls
            )
            print(f"\n✅ Carrossel publicado com sucesso! ID: {result.get('id')}")
            print_json(result)

    except ValidationError as e:
        handle_validation_error(e)
    except InstagramAuthError as e:
        print(f"\n❌ Erro de autenticação: {e}", file=sys.stderr)
        print(
            f"Verifique se o token em {ENV_TOKEN} é válido e não expirou.",
            file=sys.stderr,
        )
        sys.exit(1)
    except InstagramAPIError as e:
        print(f"\n❌ Erro da API do Instagram: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
