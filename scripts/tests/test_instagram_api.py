#!/usr/bin/env python3
"""
Testes para instagram_api.py
Usa mocks para todas as chamadas de rede — não faz requests reais.
"""

import json
import os
import sys
import unittest.mock as mock
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instagram_api import (
    GRAPH_API_BASE,
    METRICAS_POST,
    METRICAS_CONTA,
    PERIODOS_VALIDOS,
    InstagramAPIError,
    InstagramAuthError,
    get_account_insights,
    get_insights,
    get_audience_demographics,
    get_recent_posts,
    publish_photo,
    publish_carousel,
    get_token,
    build_parser,
)
from validators import ValidationError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FAKE_TOKEN = "EAAtest1234"
FAKE_ACCOUNT = "17841400008460056"
FAKE_MEDIA_ID = "17854360229135492"
FAKE_IMAGE_URL = "https://example.com/imagem.jpg"


def make_response(data: dict) -> mock.MagicMock:
    """Cria um mock de resposta HTTP."""
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(data).encode("utf-8")
    resp.__enter__ = mock.MagicMock(return_value=resp)
    resp.__exit__ = mock.MagicMock(return_value=False)
    return resp


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

def test_metricas_post_nao_vazio():
    assert len(METRICAS_POST) > 0


def test_metricas_conta_nao_vazio():
    assert len(METRICAS_CONTA) > 0


def test_periodos_validos_contem_day():
    assert "day" in PERIODOS_VALIDOS


def test_grafo_api_base_https():
    assert GRAPH_API_BASE.startswith("https://")


# ---------------------------------------------------------------------------
# get_account_insights
# ---------------------------------------------------------------------------

def test_get_account_insights_chama_endpoint_correto():
    resposta = {"data": [{"name": "impressions", "values": [{"value": 100}]}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        resultado = get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN)
        assert resultado == resposta
        url_chamada = m.call_args[0][0]
        assert FAKE_ACCOUNT in url_chamada
        assert "insights" in url_chamada


def test_get_account_insights_metricas_padrao():
    resposta = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)):
        resultado = get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN)
        assert "data" in resultado


def test_get_account_insights_metricas_customizadas():
    resposta = {"data": [{"name": "reach"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN, metrics=["reach"])
        url_chamada = m.call_args[0][0]
        assert "reach" in url_chamada


def test_get_account_insights_periodo_customizado():
    resposta = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN, period="week")
        url_chamada = m.call_args[0][0]
        assert "week" in url_chamada


def test_get_account_insights_com_datas():
    resposta = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN, since="2026-01-01", until="2026-01-31")
        url_chamada = m.call_args[0][0]
        assert "since" in url_chamada
        assert "until" in url_chamada


# ---------------------------------------------------------------------------
# get_insights
# ---------------------------------------------------------------------------

def test_get_insights_chama_endpoint_correto():
    resposta = {"data": [{"name": "impressions", "values": [{"value": 500}]}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        resultado = get_insights(FAKE_MEDIA_ID, FAKE_TOKEN)
        assert resultado == resposta
        url_chamada = m.call_args[0][0]
        assert FAKE_MEDIA_ID in url_chamada
        assert "insights" in url_chamada


def test_get_insights_metricas_customizadas():
    resposta = {"data": [{"name": "reach"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_insights(FAKE_MEDIA_ID, FAKE_TOKEN, metrics=["reach"])
        url_chamada = m.call_args[0][0]
        assert "reach" in url_chamada


# ---------------------------------------------------------------------------
# get_audience_demographics
# ---------------------------------------------------------------------------

def test_get_audience_demographics_chama_endpoint_correto():
    resposta = {"data": [{"name": "audience_gender_age", "values": []}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        resultado = get_audience_demographics(FAKE_ACCOUNT, FAKE_TOKEN)
        assert resultado == resposta
        url_chamada = m.call_args[0][0]
        assert FAKE_ACCOUNT in url_chamada
        assert "audience_gender_age" in url_chamada


def test_get_audience_demographics_periodo_lifetime():
    resposta = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_audience_demographics(FAKE_ACCOUNT, FAKE_TOKEN)
        url_chamada = m.call_args[0][0]
        assert "lifetime" in url_chamada


# ---------------------------------------------------------------------------
# get_recent_posts
# ---------------------------------------------------------------------------

def test_get_recent_posts_chama_endpoint_correto():
    resposta = {"data": [{"id": "123", "caption": "Post de teste"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        resultado = get_recent_posts(FAKE_ACCOUNT, FAKE_TOKEN)
        assert resultado == resposta
        url_chamada = m.call_args[0][0]
        assert FAKE_ACCOUNT in url_chamada
        assert "media" in url_chamada


def test_get_recent_posts_limite_customizado():
    resposta = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_recent_posts(FAKE_ACCOUNT, FAKE_TOKEN, limit=25)
        url_chamada = m.call_args[0][0]
        assert "25" in url_chamada


def test_get_recent_posts_limite_maximo_100():
    resposta = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resposta)) as m:
        get_recent_posts(FAKE_ACCOUNT, FAKE_TOKEN, limit=200)
        url_chamada = m.call_args[0][0]
        # Deve ser limitado a 100
        assert "100" in url_chamada


# ---------------------------------------------------------------------------
# publish_photo
# ---------------------------------------------------------------------------

def test_publish_photo_duas_etapas():
    """Verifica que publish_photo faz 2 chamadas POST (container + publish)."""
    container_resp = {"id": "container_123"}
    publish_resp = {"id": "post_456"}

    responses = [container_resp, publish_resp]
    call_count = [0]

    def fake_urlopen(req, timeout=None):
        data = responses[call_count[0]]
        call_count[0] += 1
        return make_response(data)

    with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = publish_photo(FAKE_ACCOUNT, FAKE_TOKEN, FAKE_IMAGE_URL, "Minha legenda")
        assert result["id"] == "post_456"
        assert result["creation_id"] == "container_123"
        assert call_count[0] == 2


def test_publish_photo_container_sem_id_raise():
    """Se o container não retorna ID, deve levantar InstagramAPIError."""
    with mock.patch("urllib.request.urlopen", return_value=make_response({})):
        with pytest.raises(InstagramAPIError, match="container"):
            publish_photo(FAKE_ACCOUNT, FAKE_TOKEN, FAKE_IMAGE_URL, "legenda")


# ---------------------------------------------------------------------------
# publish_carousel
# ---------------------------------------------------------------------------

def test_publish_carousel_tres_etapas():
    """Verifica que publish_carousel faz N+2 chamadas (N filhos + container + publish)."""
    image_urls = [
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg",
        "https://example.com/img3.jpg",
    ]
    responses = [
        {"id": "child_1"},
        {"id": "child_2"},
        {"id": "child_3"},
        {"id": "carousel_container"},
        {"id": "carousel_post"},
    ]
    call_count = [0]

    def fake_urlopen(req, timeout=None):
        data = responses[call_count[0]]
        call_count[0] += 1
        return make_response(data)

    with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = publish_carousel(FAKE_ACCOUNT, FAKE_TOKEN, "Legenda carrossel", image_urls)
        assert result["id"] == "carousel_post"
        assert len(result["children_ids"]) == 3
        assert call_count[0] == 5


def test_publish_carousel_menos_de_2_imagens_raise():
    with pytest.raises(ValidationError, match="2 e 10"):
        publish_carousel(FAKE_ACCOUNT, FAKE_TOKEN, "legenda", ["https://example.com/img1.jpg"])


def test_publish_carousel_mais_de_10_imagens_raise():
    urls = [f"https://example.com/img{i}.jpg" for i in range(11)]
    with pytest.raises(ValidationError, match="2 e 10"):
        publish_carousel(FAKE_ACCOUNT, FAKE_TOKEN, "legenda", urls)


def test_publish_carousel_sem_id_filho_raise():
    """Se um filho não retorna ID, deve levantar InstagramAPIError."""
    with mock.patch("urllib.request.urlopen", return_value=make_response({})):
        with pytest.raises(InstagramAPIError, match="container para imagem"):
            publish_carousel(
                FAKE_ACCOUNT, FAKE_TOKEN, "legenda",
                ["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
            )


# ---------------------------------------------------------------------------
# Tratamento de erros HTTP
# ---------------------------------------------------------------------------

def test_erro_autenticacao_levanta_instagram_auth_error():
    import urllib.error
    error_body = json.dumps({
        "error": {
            "message": "Invalid OAuth access token",
            "code": 190,
            "error_subcode": 463,
        }
    }).encode("utf-8")
    http_error = urllib.error.HTTPError(
        url="https://graph.facebook.com/v18.0/test/insights",
        code=400, msg="Bad Request", hdrs=None, fp=None
    )
    http_error.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_error):
        with pytest.raises(InstagramAuthError):
            get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN)


def test_erro_api_generico_levanta_instagram_api_error():
    import urllib.error
    error_body = json.dumps({
        "error": {
            "message": "Unsupported metric for this media type",
            "code": 100,
        }
    }).encode("utf-8")
    http_error = urllib.error.HTTPError(
        url="https://graph.facebook.com/v18.0/test/insights",
        code=400, msg="Bad Request", hdrs=None, fp=None
    )
    http_error.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_error):
        with pytest.raises(InstagramAPIError):
            get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN)


def test_erro_de_conexao_levanta_instagram_api_error():
    import urllib.error
    with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        with pytest.raises(InstagramAPIError, match="Erro de conexão"):
            get_account_insights(FAKE_ACCOUNT, FAKE_TOKEN)


# ---------------------------------------------------------------------------
# get_token
# ---------------------------------------------------------------------------

def test_get_token_retorna_valor_da_env(monkeypatch):
    monkeypatch.setenv("INSTAGRAM_ACCESS_TOKEN", "meu_token_123")
    token = get_token()
    assert token == "meu_token_123"


def test_get_token_sem_env_encerra_processo(monkeypatch):
    monkeypatch.delenv("INSTAGRAM_ACCESS_TOKEN", raising=False)
    with pytest.raises(SystemExit) as exc:
        get_token()
    assert exc.value.code == 1


def test_get_token_env_vazia_encerra_processo(monkeypatch):
    monkeypatch.setenv("INSTAGRAM_ACCESS_TOKEN", "   ")
    with pytest.raises(SystemExit) as exc:
        get_token()
    assert exc.value.code == 1


# ---------------------------------------------------------------------------
# CLI (parser)
# ---------------------------------------------------------------------------

def test_parser_comando_insights():
    parser = build_parser()
    args = parser.parse_args(["insights", FAKE_ACCOUNT])
    assert args.comando == "insights"
    assert args.account_id == FAKE_ACCOUNT


def test_parser_comando_posts_com_limit():
    parser = build_parser()
    args = parser.parse_args(["posts", FAKE_ACCOUNT, "--limit", "20"])
    assert args.comando == "posts"
    assert args.limit == 20


def test_parser_comando_publish_photo():
    parser = build_parser()
    args = parser.parse_args(["publish-photo", FAKE_ACCOUNT, FAKE_IMAGE_URL, "Minha legenda"])
    assert args.comando == "publish-photo"
    assert args.image_url == FAKE_IMAGE_URL
    assert args.caption == "Minha legenda"


def test_parser_comando_publish_carousel():
    parser = build_parser()
    args = parser.parse_args([
        "publish-carousel", FAKE_ACCOUNT, "Legenda",
        "https://example.com/img1.jpg", "https://example.com/img2.jpg"
    ])
    assert args.comando == "publish-carousel"
    assert len(args.image_urls) == 2


def test_parser_sem_subcomando_falha():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])
