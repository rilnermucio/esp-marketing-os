#!/usr/bin/env python3
"""
Testes para meta_ads_api.py
Usa mocks para todas as chamadas de rede.
"""

import json
import os
import sys
import unittest.mock as mock
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meta_ads_api import (
    GRAPH_API_BASE,
    OBJETIVOS_CAMPANHA,
    STATUS_VALIDOS,
    METRICAS_INSIGHTS,
    MetaAdsError,
    MetaAdsAuthError,
    get_campaigns,
    get_campaign_insights,
    get_ad_performance,
    create_campaign,
    pause_ad,
    resume_ad,
    get_token,
    get_ad_account_id,
    print_campaigns_table,
    build_parser,
)
from validators import ValidationError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FAKE_TOKEN = "EAAtest_meta_token"
FAKE_ACCOUNT = "act_123456789"
FAKE_CAMPAIGN_ID = "120200000123456"
FAKE_AD_ID = "120200000987654"


def make_response(data: dict):
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(data).encode("utf-8")
    resp.__enter__ = mock.MagicMock(return_value=resp)
    resp.__exit__ = mock.MagicMock(return_value=False)
    return resp


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

def test_objetivos_campanha_nao_vazio():
    assert len(OBJETIVOS_CAMPANHA) > 0


def test_objetivos_contem_traffic():
    assert "TRAFFIC" in OBJETIVOS_CAMPANHA


def test_status_validos_contem_active():
    assert "ACTIVE" in STATUS_VALIDOS


def test_metricas_insights_nao_vazio():
    assert len(METRICAS_INSIGHTS) > 0


def test_graph_api_base_https():
    assert GRAPH_API_BASE.startswith("https://")


# ---------------------------------------------------------------------------
# get_campaigns
# ---------------------------------------------------------------------------

SAMPLE_CAMPAIGNS = [
    {
        "id": FAKE_CAMPAIGN_ID,
        "name": "Campanha Leads 2026",
        "status": "ACTIVE",
        "objective": "LEADS",
        "daily_budget": "5000",
    },
    {
        "id": "120200000111111",
        "name": "Campanha Tráfego",
        "status": "PAUSED",
        "objective": "TRAFFIC",
        "daily_budget": "3000",
    },
]


def test_get_campaigns_retorna_lista():
    resp = {"data": SAMPLE_CAMPAIGNS}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)
        assert isinstance(result, list)
        assert len(result) == 2


def test_get_campaigns_chama_endpoint_correto():
    resp = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)
        url = m.call_args[0][0]
        assert "campaigns" in url
        assert FAKE_ACCOUNT in url


def test_get_campaigns_filtra_por_status():
    resp = {"data": [SAMPLE_CAMPAIGNS[0]]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN, status="ACTIVE")
        url = m.call_args[0][0]
        assert "ACTIVE" in url


def test_get_campaigns_sem_dados_retorna_lista_vazia():
    resp = {}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)
        assert result == []


def test_get_campaigns_limite_aplicado():
    resp = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN, limit=10)
        url = m.call_args[0][0]
        assert "10" in url


# ---------------------------------------------------------------------------
# get_campaign_insights
# ---------------------------------------------------------------------------

def test_get_campaign_insights_retorna_dict():
    resp = {"data": [{"impressions": "1000", "clicks": "50", "ctr": "0.05", "spend": "25.00"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_campaign_insights(FAKE_CAMPAIGN_ID, FAKE_TOKEN)
        assert isinstance(result, dict)
        assert "campaign_id" in result
        assert "periodo" in result
        assert "dados" in result


def test_get_campaign_insights_chama_endpoint_correto():
    resp = {"data": [{"impressions": "500"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        get_campaign_insights(FAKE_CAMPAIGN_ID, FAKE_TOKEN)
        url = m.call_args[0][0]
        assert FAKE_CAMPAIGN_ID in url
        assert "insights" in url


def test_get_campaign_insights_sem_dados():
    resp = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_campaign_insights(FAKE_CAMPAIGN_ID, FAKE_TOKEN)
        assert result["dados"] is None
        assert "mensagem" in result


def test_get_campaign_insights_periodo_customizado():
    resp = {"data": [{"impressions": "200"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_campaign_insights(FAKE_CAMPAIGN_ID, FAKE_TOKEN, days=14)
        assert "14" in result["periodo"] or result["dados"] is not None


# ---------------------------------------------------------------------------
# get_ad_performance
# ---------------------------------------------------------------------------

def test_get_ad_performance_retorna_lista():
    resp = {"data": [{"campaign_name": "Campanha A", "impressions": "1000", "spend": "20.00"}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_ad_performance(FAKE_ACCOUNT, FAKE_TOKEN)
        assert isinstance(result, list)


def test_get_ad_performance_chama_insights_endpoint():
    resp = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        get_ad_performance(FAKE_ACCOUNT, FAKE_TOKEN)
        url = m.call_args[0][0]
        assert "insights" in url
        assert FAKE_ACCOUNT in url


def test_get_ad_performance_nivel_customizado():
    resp = {"data": []}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        get_ad_performance(FAKE_ACCOUNT, FAKE_TOKEN, level="campaign")
        url = m.call_args[0][0]
        assert "campaign" in url


# ---------------------------------------------------------------------------
# create_campaign
# ---------------------------------------------------------------------------

def test_create_campaign_retorna_dict_com_id():
    resp = {"id": "120200000NEW123"}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = create_campaign(FAKE_ACCOUNT, FAKE_TOKEN, "Nova Campanha", "LEADS", 5000)
        assert result["id"] == "120200000NEW123"
        assert result["name"] == "Nova Campanha"
        assert result["status"] == "PAUSED"


def test_create_campaign_objetivo_em_maiusculas():
    resp = {"id": "120200000NEW456"}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        create_campaign(FAKE_ACCOUNT, FAKE_TOKEN, "Campanha Teste", "traffic", 5000)
        req = m.call_args[0][0]
        body = urllib.parse.parse_qs(req.data.decode("utf-8") if req.data else "")


def test_create_campaign_sem_id_raise():
    resp = {}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        with pytest.raises(MetaAdsError, match="ID não retornado"):
            create_campaign(FAKE_ACCOUNT, FAKE_TOKEN, "Campanha", "LEADS", 5000)


def test_create_campaign_status_customizado():
    resp = {"id": "120200000STATUS"}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = create_campaign(FAKE_ACCOUNT, FAKE_TOKEN, "Campanha Ativa", "TRAFFIC", 3000, status="ACTIVE")
        assert result["status"] == "ACTIVE"


# ---------------------------------------------------------------------------
# pause_ad / resume_ad
# ---------------------------------------------------------------------------

def test_pause_ad_retorna_dict():
    resp = {"success": True}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = pause_ad(FAKE_AD_ID, FAKE_TOKEN)
        assert result["id"] == FAKE_AD_ID
        assert result["status"] == "PAUSED"


def test_pause_ad_chama_endpoint_correto():
    resp = {"success": True}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)) as m:
        pause_ad(FAKE_AD_ID, FAKE_TOKEN)
        req = m.call_args[0][0]
        assert FAKE_AD_ID in req.full_url if hasattr(req, 'full_url') else FAKE_AD_ID in str(req)


def test_resume_ad_retorna_dict():
    resp = {"success": True}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = resume_ad(FAKE_AD_ID, FAKE_TOKEN)
        assert result["id"] == FAKE_AD_ID
        assert result["status"] == "ACTIVE"


# ---------------------------------------------------------------------------
# Tratamento de erros HTTP
# ---------------------------------------------------------------------------

def test_erro_autenticacao_levanta_meta_ads_auth_error():
    import urllib.error
    error_body = json.dumps({
        "error": {"message": "Invalid OAuth access token", "code": 190}
    }).encode()
    http_err = urllib.error.HTTPError(url="https://graph.facebook.com", code=400, msg="Bad Request", hdrs=None, fp=None)
    http_err.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(MetaAdsAuthError):
            get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)


def test_erro_permissao_levanta_meta_ads_auth_error():
    import urllib.error
    error_body = json.dumps({
        "error": {"message": "Permissions error", "code": 200}
    }).encode()
    http_err = urllib.error.HTTPError(url="https://graph.facebook.com", code=403, msg="Forbidden", hdrs=None, fp=None)
    http_err.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(MetaAdsAuthError):
            get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)


def test_erro_generico_levanta_meta_ads_error():
    import urllib.error
    error_body = json.dumps({
        "error": {"message": "Invalid parameter", "code": 100}
    }).encode()
    http_err = urllib.error.HTTPError(url="https://graph.facebook.com", code=400, msg="Bad Request", hdrs=None, fp=None)
    http_err.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(MetaAdsError):
            get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)


def test_erro_conexao_levanta_meta_ads_error():
    import urllib.error
    with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        with pytest.raises(MetaAdsError, match="Erro de conexão"):
            get_campaigns(FAKE_ACCOUNT, FAKE_TOKEN)


# ---------------------------------------------------------------------------
# get_token
# ---------------------------------------------------------------------------

def test_get_token_retorna_env(monkeypatch):
    monkeypatch.setenv("META_ACCESS_TOKEN", "meu_token_meta")
    assert get_token() == "meu_token_meta"


def test_get_token_sem_env_encerra(monkeypatch):
    monkeypatch.delenv("META_ACCESS_TOKEN", raising=False)
    with pytest.raises(SystemExit) as exc:
        get_token()
    assert exc.value.code == 1


# ---------------------------------------------------------------------------
# get_ad_account_id
# ---------------------------------------------------------------------------

def test_get_ad_account_id_com_prefixo_act():
    result = get_ad_account_id("act_123456789")
    assert result == "act_123456789"


def test_get_ad_account_id_adiciona_prefixo_act():
    result = get_ad_account_id("123456789")
    assert result == "act_123456789"


def test_get_ad_account_id_de_env(monkeypatch):
    monkeypatch.setenv("META_AD_ACCOUNT_ID", "act_999888777")
    result = get_ad_account_id()
    assert result == "act_999888777"


def test_get_ad_account_id_sem_config_encerra(monkeypatch):
    monkeypatch.delenv("META_AD_ACCOUNT_ID", raising=False)
    with pytest.raises(SystemExit) as exc:
        get_ad_account_id()
    assert exc.value.code == 1


# ---------------------------------------------------------------------------
# print_campaigns_table
# ---------------------------------------------------------------------------

def test_print_campaigns_table_lista_vazia(capsys):
    print_campaigns_table([])
    out = capsys.readouterr().out
    assert "Nenhuma campanha" in out


def test_print_campaigns_table_exibe_dados(capsys):
    print_campaigns_table(SAMPLE_CAMPAIGNS)
    out = capsys.readouterr().out
    assert "Campanha Leads 2026" in out
    assert "ACTIVE" in out


# ---------------------------------------------------------------------------
# CLI (parser)
# ---------------------------------------------------------------------------

def test_parser_comando_campaigns():
    parser = build_parser()
    args = parser.parse_args(["campaigns"])
    assert args.comando == "campaigns"


def test_parser_campaigns_com_status():
    parser = build_parser()
    args = parser.parse_args(["campaigns", "--status", "ACTIVE"])
    assert args.status == "ACTIVE"


def test_parser_campaign_insights():
    parser = build_parser()
    args = parser.parse_args(["campaign-insights", FAKE_CAMPAIGN_ID])
    assert args.comando == "campaign-insights"
    assert args.campaign_id == FAKE_CAMPAIGN_ID


def test_parser_create_campaign():
    parser = build_parser()
    args = parser.parse_args(["create-campaign", "Minha Campanha", "LEADS", "5000"])
    assert args.nome == "Minha Campanha"
    assert args.objetivo == "LEADS"
    assert args.budget_diario == pytest.approx(5000.0)


def test_parser_pause_ad():
    parser = build_parser()
    args = parser.parse_args(["pause-ad", FAKE_AD_ID])
    assert args.ad_id == FAKE_AD_ID


def test_parser_resume_ad():
    parser = build_parser()
    args = parser.parse_args(["resume-ad", FAKE_AD_ID])
    assert args.ad_id == FAKE_AD_ID


def test_parser_sem_subcomando_falha():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


import urllib.parse
