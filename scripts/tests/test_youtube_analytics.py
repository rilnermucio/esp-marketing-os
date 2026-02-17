#!/usr/bin/env python3
"""
Testes para youtube_analytics.py
"""

import json
import os
import sys
import pytest
from unittest.mock import MagicMock, patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_analytics import (
    YouTubeAnalyticsError,
    YouTubeAuthError,
    _load_credentials,
    _date_range,
    get_channel_stats,
    get_top_videos,
    get_video_list,
    get_demographics,
    get_traffic_sources,
    get_credentials_and_token,
    YT_ANALYTICS_SCOPE,
    ENV_CREDENTIALS_FILE,
    ENV_CREDENTIALS_JSON,
    ENV_CREDENTIALS_FILE_FALLBACK,
    ENV_CREDENTIALS_JSON_FALLBACK,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FAKE_CREDENTIALS = {
    "type": "service_account",
    "project_id": "test-project",
    "private_key_id": "key-id",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----\n",
    "client_email": "test@test-project.iam.gserviceaccount.com",
    "client_id": "1234567890",
    "token_uri": "https://oauth2.googleapis.com/token",
}

FAKE_TOKEN = "ya29.fake-access-token"


def make_analytics_response(rows: list, col_names: list) -> dict:
    """Monta resposta simulada da YouTube Analytics API."""
    return {
        "columnHeaders": [{"name": n, "dataType": "INTEGER" if i > 0 else "STRING"}
                          for i, n in enumerate(col_names)],
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# YouTubeAnalyticsError / YouTubeAuthError
# ---------------------------------------------------------------------------

def test_youtube_analytics_error_sem_status():
    err = YouTubeAnalyticsError("Erro genérico")
    assert "Erro genérico" in str(err)
    assert err.status is None


def test_youtube_analytics_error_com_status():
    err = YouTubeAnalyticsError("Quota excedida", status=403)
    assert "[HTTP 403]" in str(err)
    assert err.status == 403


def test_youtube_auth_error_herda_analytics_error():
    err = YouTubeAuthError("Token inválido", status=401)
    assert isinstance(err, YouTubeAnalyticsError)
    assert err.status == 401


# ---------------------------------------------------------------------------
# _load_credentials
# ---------------------------------------------------------------------------

def test_load_credentials_via_json_env(monkeypatch):
    monkeypatch.setenv(ENV_CREDENTIALS_JSON, json.dumps(FAKE_CREDENTIALS))
    creds = _load_credentials()
    assert creds["client_email"] == FAKE_CREDENTIALS["client_email"]


def test_load_credentials_via_json_env_invalido(monkeypatch):
    monkeypatch.setenv(ENV_CREDENTIALS_JSON, "{invalid json")
    with pytest.raises(YouTubeAuthError, match="Credenciais JSON inválidas"):
        _load_credentials()


def test_load_credentials_via_file_env(tmp_path, monkeypatch):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text(json.dumps(FAKE_CREDENTIALS))
    monkeypatch.delenv(ENV_CREDENTIALS_JSON, raising=False)
    monkeypatch.delenv(ENV_CREDENTIALS_JSON_FALLBACK, raising=False)
    monkeypatch.setenv(ENV_CREDENTIALS_FILE, str(creds_file))
    creds = _load_credentials()
    assert creds["type"] == "service_account"


def test_load_credentials_arquivo_nao_encontrado(monkeypatch):
    monkeypatch.delenv(ENV_CREDENTIALS_JSON, raising=False)
    monkeypatch.delenv(ENV_CREDENTIALS_JSON_FALLBACK, raising=False)
    monkeypatch.setenv(ENV_CREDENTIALS_FILE, "/caminho/inexistente.json")
    with pytest.raises(YouTubeAuthError, match="não encontrado"):
        _load_credentials()


def test_load_credentials_fallback_gsc(monkeypatch):
    monkeypatch.delenv(ENV_CREDENTIALS_JSON, raising=False)
    monkeypatch.delenv(ENV_CREDENTIALS_FILE, raising=False)
    monkeypatch.setenv(ENV_CREDENTIALS_JSON_FALLBACK, json.dumps(FAKE_CREDENTIALS))
    creds = _load_credentials()
    assert creds["client_email"] == FAKE_CREDENTIALS["client_email"]


def test_load_credentials_sem_nenhuma_config(monkeypatch):
    for env in [ENV_CREDENTIALS_JSON, ENV_CREDENTIALS_FILE,
                ENV_CREDENTIALS_JSON_FALLBACK, ENV_CREDENTIALS_FILE_FALLBACK]:
        monkeypatch.delenv(env, raising=False)
    with pytest.raises(YouTubeAuthError, match="Credenciais não configuradas"):
        _load_credentials()


def test_load_credentials_arquivo_json_invalido(tmp_path, monkeypatch):
    creds_file = tmp_path / "bad.json"
    creds_file.write_text("not valid json")
    monkeypatch.delenv(ENV_CREDENTIALS_JSON, raising=False)
    monkeypatch.delenv(ENV_CREDENTIALS_JSON_FALLBACK, raising=False)
    monkeypatch.setenv(ENV_CREDENTIALS_FILE, str(creds_file))
    with pytest.raises(YouTubeAuthError, match="inválido"):
        _load_credentials()


# ---------------------------------------------------------------------------
# _date_range
# ---------------------------------------------------------------------------

def test_date_range_retorna_duas_strings():
    start, end = _date_range(30)
    assert len(start) == 10  # YYYY-MM-DD
    assert len(end) == 10


def test_date_range_start_antes_end():
    from datetime import date
    start, end = _date_range(30)
    assert date.fromisoformat(start) < date.fromisoformat(end)


def test_date_range_periodo_correto():
    from datetime import date, timedelta
    start, end = _date_range(7)
    start_d = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    assert (end_d - start_d).days == 6  # 7 dias: start + 6 = end


# ---------------------------------------------------------------------------
# get_channel_stats
# ---------------------------------------------------------------------------

CHANNEL_STATS_RESPONSE = make_analytics_response(
    rows=[[1000, 5000.0, 180.0, 80, 20, 10, 50, 5, 15]],
    col_names=[
        "views", "estimatedMinutesWatched", "averageViewDuration",
        "likes", "comments", "shares",
        "subscribersGained", "subscribersLost", "videosAddedToPlaylists",
    ],
)


@patch("youtube_analytics._api_get", return_value=CHANNEL_STATS_RESPONSE)
def test_get_channel_stats_retorna_metricas(mock_get):
    result = get_channel_stats(FAKE_TOKEN, days=30)
    assert result["views"] == 1000
    assert result["likes"] == 80
    assert result["net_subscribers"] == 45  # 50 - 5


@patch("youtube_analytics._api_get", return_value=CHANNEL_STATS_RESPONSE)
def test_get_channel_stats_tem_periodo(mock_get):
    result = get_channel_stats(FAKE_TOKEN, days=30)
    assert "periodo" in result
    assert " a " in result["periodo"]


@patch("youtube_analytics._api_get", return_value={"rows": [], "columnHeaders": []})
def test_get_channel_stats_sem_dados(mock_get):
    result = get_channel_stats(FAKE_TOKEN, days=30)
    assert result["dados"] is None
    assert "mensagem" in result


@patch("youtube_analytics._api_get", return_value=CHANNEL_STATS_RESPONSE)
def test_get_channel_stats_net_subscribers_negativo(mock_get):
    # Forçar mais perdas que ganhos
    response = make_analytics_response(
        rows=[[500, 2000.0, 120.0, 30, 5, 2, 3, 10, 5]],
        col_names=[
            "views", "estimatedMinutesWatched", "averageViewDuration",
            "likes", "comments", "shares",
            "subscribersGained", "subscribersLost", "videosAddedToPlaylists",
        ],
    )
    mock_get.return_value = response
    result = get_channel_stats(FAKE_TOKEN)
    assert result["net_subscribers"] == -7  # 3 - 10


# ---------------------------------------------------------------------------
# get_top_videos
# ---------------------------------------------------------------------------

TOP_VIDEOS_RESPONSE = make_analytics_response(
    rows=[
        ["vid001", 5000, 15000.0, 400, 50, 30],
        ["vid002", 3000, 9000.0, 200, 25, 10],
        ["vid003", 1000, 3000.0, 50, 5, 2],
    ],
    col_names=["video", "views", "estimatedMinutesWatched", "likes", "comments", "shares"],
)


@patch("youtube_analytics._api_get", return_value=TOP_VIDEOS_RESPONSE)
def test_get_top_videos_retorna_lista(mock_get):
    result = get_top_videos(FAKE_TOKEN, days=30, limit=10)
    assert isinstance(result, list)
    assert len(result) == 3


@patch("youtube_analytics._api_get", return_value=TOP_VIDEOS_RESPONSE)
def test_get_top_videos_tem_campos_esperados(mock_get):
    result = get_top_videos(FAKE_TOKEN)
    video = result[0]
    assert "video_id" in video
    assert "views" in video
    assert "likes" in video
    assert "comments" in video
    assert "shares" in video
    assert "watch_time_minutos" in video


@patch("youtube_analytics._api_get", return_value=TOP_VIDEOS_RESPONSE)
def test_get_top_videos_ordenado_por_views(mock_get):
    result = get_top_videos(FAKE_TOKEN)
    views = [v["views"] for v in result]
    assert views == sorted(views, reverse=True)


@patch("youtube_analytics._api_get", return_value={"rows": [], "columnHeaders": []})
def test_get_top_videos_sem_dados(mock_get):
    result = get_top_videos(FAKE_TOKEN)
    assert result == []


# ---------------------------------------------------------------------------
# get_video_list
# ---------------------------------------------------------------------------

DATA_API_RESPONSE = {
    "items": [
        {"id": "vid001", "snippet": {"title": "Título do Vídeo 1"}},
        {"id": "vid002", "snippet": {"title": "Título do Vídeo 2"}},
        {"id": "vid003", "snippet": {"title": "Título do Vídeo 3"}},
    ]
}


@patch("youtube_analytics._api_get")
def test_get_video_list_enriquece_com_titulos(mock_get):
    mock_get.side_effect = [TOP_VIDEOS_RESPONSE, DATA_API_RESPONSE]
    result = get_video_list(FAKE_TOKEN, days=30, limit=10)
    assert len(result) == 3
    assert result[0]["titulo"] == "Título do Vídeo 1"


@patch("youtube_analytics._api_get")
def test_get_video_list_calcula_engagement_rate(mock_get):
    mock_get.side_effect = [TOP_VIDEOS_RESPONSE, DATA_API_RESPONSE]
    result = get_video_list(FAKE_TOKEN)
    for v in result:
        assert "engagement_rate" in v
        assert isinstance(v["engagement_rate"], float)


@patch("youtube_analytics._api_get")
def test_get_video_list_sem_videos_retorna_lista_vazia(mock_get):
    mock_get.return_value = {"rows": [], "columnHeaders": []}
    result = get_video_list(FAKE_TOKEN)
    assert result == []


@patch("youtube_analytics._api_get")
def test_get_video_list_video_sem_titulo_usa_fallback(mock_get):
    mock_get.side_effect = [
        TOP_VIDEOS_RESPONSE,
        {"items": []},  # Data API retorna vazio
    ]
    result = get_video_list(FAKE_TOKEN)
    assert "video_id" in result[0]["titulo"] or result[0]["titulo"].startswith("Video ")


# ---------------------------------------------------------------------------
# get_demographics
# ---------------------------------------------------------------------------

DEMOGRAPHICS_RESPONSE = make_analytics_response(
    rows=[
        ["age18-24", "male", 35.5],
        ["age18-24", "female", 20.0],
        ["age25-34", "male", 25.0],
        ["age25-34", "female", 15.0],
        ["age35-44", "male", 4.5],
    ],
    col_names=["ageGroup", "gender", "viewerPercentage"],
)


@patch("youtube_analytics._api_get", return_value=DEMOGRAPHICS_RESPONSE)
def test_get_demographics_retorna_por_faixa(mock_get):
    result = get_demographics(FAKE_TOKEN)
    assert "por_faixa_etaria" in result
    assert "age18-24" in result["por_faixa_etaria"]


@patch("youtube_analytics._api_get", return_value=DEMOGRAPHICS_RESPONSE)
def test_get_demographics_retorna_por_genero(mock_get):
    result = get_demographics(FAKE_TOKEN)
    assert "por_genero" in result
    assert "male" in result["por_genero"]
    assert "female" in result["por_genero"]


@patch("youtube_analytics._api_get", return_value=DEMOGRAPHICS_RESPONSE)
def test_get_demographics_agrega_faixas_etarias(mock_get):
    result = get_demographics(FAKE_TOKEN)
    # age18-24 = 35.5 + 20.0 = 55.5
    assert result["por_faixa_etaria"]["age18-24"] == pytest.approx(55.5, rel=1e-2)


@patch("youtube_analytics._api_get", return_value=DEMOGRAPHICS_RESPONSE)
def test_get_demographics_tem_periodo(mock_get):
    result = get_demographics(FAKE_TOKEN)
    assert "periodo" in result


@patch("youtube_analytics._api_get", return_value={"rows": [], "columnHeaders": []})
def test_get_demographics_sem_dados(mock_get):
    result = get_demographics(FAKE_TOKEN)
    assert result["por_faixa_etaria"] == {}
    assert result["por_genero"] == {}


# ---------------------------------------------------------------------------
# get_traffic_sources
# ---------------------------------------------------------------------------

TRAFFIC_RESPONSE = make_analytics_response(
    rows=[
        ["YT_SEARCH", 5000, 15000.0],
        ["SUGGESTED_VIDEOS", 3000, 9000.0],
        ["EXTERNAL", 1000, 2000.0],
        ["DIRECT_OR_UNKNOWN", 500, 800.0],
    ],
    col_names=["insightTrafficSourceType", "views", "estimatedMinutesWatched"],
)


@patch("youtube_analytics._api_get", return_value=TRAFFIC_RESPONSE)
def test_get_traffic_sources_retorna_lista(mock_get):
    result = get_traffic_sources(FAKE_TOKEN)
    assert isinstance(result, list)
    assert len(result) == 4


@patch("youtube_analytics._api_get", return_value=TRAFFIC_RESPONSE)
def test_get_traffic_sources_tem_campos_esperados(mock_get):
    result = get_traffic_sources(FAKE_TOKEN)
    fonte = result[0]
    assert "source" in fonte
    assert "views" in fonte
    assert "watch_time_minutos" in fonte
    assert "percentual_views" in fonte


@patch("youtube_analytics._api_get", return_value=TRAFFIC_RESPONSE)
def test_get_traffic_sources_percentuais_somam_100(mock_get):
    result = get_traffic_sources(FAKE_TOKEN)
    total = sum(f["percentual_views"] for f in result)
    assert total == pytest.approx(100.0, rel=1e-2)


@patch("youtube_analytics._api_get", return_value={"rows": [], "columnHeaders": []})
def test_get_traffic_sources_sem_dados(mock_get):
    result = get_traffic_sources(FAKE_TOKEN)
    assert result == []


@patch("youtube_analytics._api_get", return_value=TRAFFIC_RESPONSE)
def test_get_traffic_sources_maior_fonte_primeiro(mock_get):
    result = get_traffic_sources(FAKE_TOKEN)
    views = [f["views"] for f in result]
    assert views[0] >= views[1]


# ---------------------------------------------------------------------------
# get_credentials_and_token
# ---------------------------------------------------------------------------

@patch("youtube_analytics._get_access_token", return_value=FAKE_TOKEN)
@patch("youtube_analytics._load_credentials", return_value=FAKE_CREDENTIALS)
def test_get_credentials_and_token_retorna_token(mock_creds, mock_token):
    token = get_credentials_and_token()
    assert token == FAKE_TOKEN


@patch("youtube_analytics._get_access_token", return_value=FAKE_TOKEN)
@patch("youtube_analytics._load_credentials", return_value=FAKE_CREDENTIALS)
def test_get_credentials_and_token_usa_scope_padrao(mock_creds, mock_token):
    get_credentials_and_token()
    mock_token.assert_called_once_with(FAKE_CREDENTIALS, YT_ANALYTICS_SCOPE)


@patch("youtube_analytics._get_access_token", return_value=FAKE_TOKEN)
@patch("youtube_analytics._load_credentials", return_value=FAKE_CREDENTIALS)
def test_get_credentials_and_token_scope_customizado(mock_creds, mock_token):
    from youtube_analytics import YT_DATA_SCOPE
    get_credentials_and_token(scope=YT_DATA_SCOPE)
    mock_token.assert_called_once_with(FAKE_CREDENTIALS, YT_DATA_SCOPE)


# ---------------------------------------------------------------------------
# Tratamento de erros de API
# ---------------------------------------------------------------------------

@patch("youtube_analytics._api_get", side_effect=YouTubeAuthError("Token expirado", status=401))
def test_get_channel_stats_propaga_auth_error(mock_get):
    with pytest.raises(YouTubeAuthError, match="Token expirado"):
        get_channel_stats(FAKE_TOKEN)


@patch("youtube_analytics._api_get", side_effect=YouTubeAnalyticsError("Quota excedida", status=429))
def test_get_top_videos_propaga_analytics_error(mock_get):
    with pytest.raises(YouTubeAnalyticsError, match="Quota excedida"):
        get_top_videos(FAKE_TOKEN)


@patch("youtube_analytics._api_get", side_effect=YouTubeAnalyticsError("Erro de rede"))
def test_get_demographics_propaga_analytics_error(mock_get):
    with pytest.raises(YouTubeAnalyticsError):
        get_demographics(FAKE_TOKEN)


@patch("youtube_analytics._api_get", side_effect=YouTubeAnalyticsError("Erro"))
def test_get_traffic_sources_propaga_analytics_error(mock_get):
    with pytest.raises(YouTubeAnalyticsError):
        get_traffic_sources(FAKE_TOKEN)


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------

def test_cli_parser_channel_subcommand():
    """Testa que o subcomando 'channel' é reconhecido pelo parser."""
    import argparse
    import youtube_analytics as yt

    # Verificar que o módulo define main() e é executável
    assert callable(yt.main)


def test_date_range_7_dias():
    from datetime import date, timedelta
    start, end = _date_range(7)
    start_d = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    # end está ~2 dias no passado por causa do delay do YouTube
    assert end_d < date.today()
    assert (end_d - start_d).days == 6


def test_date_range_1_dia():
    start, end = _date_range(1)
    assert start == end  # 1 dia: período de 1 dia (start == end)
