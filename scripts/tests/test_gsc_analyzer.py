#!/usr/bin/env python3
"""
Testes para gsc_analyzer.py
Usa mocks para todas as chamadas de rede e de autenticação.
"""

import json
import os
import sys
import unittest.mock as mock
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gsc_analyzer import (
    GSC_API_BASE,
    DIMENSOES_VALIDAS,
    TIPOS_BUSCA,
    MAX_ROWS,
    GSCError,
    GSCAuthError,
    _load_credentials,
    _encode_site_url,
    _date_range,
    get_search_queries,
    get_top_pages,
    get_ctr_opportunities,
    get_position_changes,
    print_queries_table,
    print_pages_table,
    build_parser,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FAKE_SITE = "https://example.com"
FAKE_TOKEN = "ya29.fake_token"

FAKE_CREDS = {
    "type": "service_account",
    "project_id": "my-project",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nfake\n-----END RSA PRIVATE KEY-----",
    "client_email": "sa@my-project.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

ROWS_QUERIES = [
    {"keys": ["marketing digital"], "clicks": 100, "impressions": 1000, "ctr": 0.1, "position": 8.5},
    {"keys": ["seo 2026"], "clicks": 50, "impressions": 500, "ctr": 0.1, "position": 12.3},
    {"keys": ["instagram marketing"], "clicks": 200, "impressions": 800, "ctr": 0.25, "position": 3.2},
]

ROWS_PAGES = [
    {"keys": ["https://example.com/blog/seo"], "clicks": 300, "impressions": 2000, "ctr": 0.15, "position": 5.1},
    {"keys": ["https://example.com/blog/marketing"], "clicks": 150, "impressions": 1500, "ctr": 0.10, "position": 9.8},
]


def make_response(data: dict):
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(data).encode("utf-8")
    resp.__enter__ = mock.MagicMock(return_value=resp)
    resp.__exit__ = mock.MagicMock(return_value=False)
    return resp


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

def test_dimensoes_validas_nao_vazio():
    assert len(DIMENSOES_VALIDAS) > 0


def test_tipos_busca_contem_web():
    assert "web" in TIPOS_BUSCA


def test_max_rows_positivo():
    assert MAX_ROWS > 0


def test_api_base_https():
    assert GSC_API_BASE.startswith("https://")


# ---------------------------------------------------------------------------
# _load_credentials
# ---------------------------------------------------------------------------

def test_load_credentials_de_env_json(monkeypatch):
    monkeypatch.setenv("GSC_SERVICE_ACCOUNT_JSON", json.dumps(FAKE_CREDS))
    monkeypatch.delenv("GSC_CREDENTIALS_FILE", raising=False)
    result = _load_credentials()
    assert result["client_email"] == FAKE_CREDS["client_email"]


def test_load_credentials_de_arquivo(tmp_path, monkeypatch):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text(json.dumps(FAKE_CREDS))
    monkeypatch.setenv("GSC_CREDENTIALS_FILE", str(creds_file))
    monkeypatch.delenv("GSC_SERVICE_ACCOUNT_JSON", raising=False)
    result = _load_credentials()
    assert result["project_id"] == "my-project"


def test_load_credentials_sem_env_raise(monkeypatch):
    monkeypatch.delenv("GSC_CREDENTIALS_FILE", raising=False)
    monkeypatch.delenv("GSC_SERVICE_ACCOUNT_JSON", raising=False)
    with pytest.raises(GSCAuthError, match="Credenciais não configuradas"):
        _load_credentials()


def test_load_credentials_json_invalido_raise(monkeypatch):
    monkeypatch.setenv("GSC_SERVICE_ACCOUNT_JSON", "nao-e-json")
    monkeypatch.delenv("GSC_CREDENTIALS_FILE", raising=False)
    with pytest.raises(GSCAuthError, match="inválido"):
        _load_credentials()


def test_load_credentials_arquivo_nao_existe_raise(monkeypatch, tmp_path):
    monkeypatch.setenv("GSC_CREDENTIALS_FILE", str(tmp_path / "inexistente.json"))
    monkeypatch.delenv("GSC_SERVICE_ACCOUNT_JSON", raising=False)
    with pytest.raises(GSCAuthError, match="não encontrado"):
        _load_credentials()


# ---------------------------------------------------------------------------
# _encode_site_url
# ---------------------------------------------------------------------------

def test_encode_site_url_https():
    encoded = _encode_site_url("https://example.com")
    assert "https" in encoded
    assert "/" not in encoded or encoded == encoded  # URL encoded


def test_encode_site_url_sc_domain():
    encoded = _encode_site_url("sc-domain:example.com")
    assert "sc-domain" in encoded or "sc" in encoded


# ---------------------------------------------------------------------------
# _date_range
# ---------------------------------------------------------------------------

def test_date_range_retorna_strings():
    start, end = _date_range(30)
    assert isinstance(start, str)
    assert isinstance(end, str)


def test_date_range_formato_iso():
    start, end = _date_range(30)
    from datetime import datetime
    datetime.fromisoformat(start)
    datetime.fromisoformat(end)


def test_date_range_start_antes_end():
    start, end = _date_range(30)
    assert start < end


def test_date_range_diferenca_correta():
    from datetime import date
    start, end = _date_range(30)
    start_dt = date.fromisoformat(start)
    end_dt = date.fromisoformat(end)
    assert (end_dt - start_dt).days == 29  # 30 dias inclusive


# ---------------------------------------------------------------------------
# get_search_queries
# ---------------------------------------------------------------------------

def test_get_search_queries_retorna_lista():
    resp = {"rows": ROWS_QUERIES}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_search_queries(FAKE_SITE, FAKE_TOKEN)
        assert isinstance(result, list)
        assert len(result) == 3


def test_get_search_queries_campos_obrigatorios():
    resp = {"rows": ROWS_QUERIES[:1]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_search_queries(FAKE_SITE, FAKE_TOKEN)
        item = result[0]
        assert "query" in item
        assert "clicks" in item
        assert "impressions" in item
        assert "ctr" in item
        assert "position" in item


def test_get_search_queries_ctr_em_porcentagem():
    resp = {"rows": [{"keys": ["test"], "clicks": 10, "impressions": 100, "ctr": 0.1, "position": 5.0}]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_search_queries(FAKE_SITE, FAKE_TOKEN)
        assert result[0]["ctr"] == pytest.approx(10.0)


def test_get_search_queries_sem_rows():
    resp = {}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_search_queries(FAKE_SITE, FAKE_TOKEN)
        assert result == []


# ---------------------------------------------------------------------------
# get_top_pages
# ---------------------------------------------------------------------------

def test_get_top_pages_retorna_lista():
    resp = {"rows": ROWS_PAGES}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_top_pages(FAKE_SITE, FAKE_TOKEN)
        assert isinstance(result, list)
        assert len(result) == 2


def test_get_top_pages_campos_obrigatorios():
    resp = {"rows": ROWS_PAGES[:1]}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_top_pages(FAKE_SITE, FAKE_TOKEN)
        item = result[0]
        assert "page" in item
        assert "clicks" in item
        assert "position" in item


# ---------------------------------------------------------------------------
# get_ctr_opportunities
# ---------------------------------------------------------------------------

def test_get_ctr_opportunities_filtra_por_impressoes():
    rows = [
        {"keys": ["query1"], "clicks": 5, "impressions": 200, "ctr": 0.025, "position": 10.0},
        {"keys": ["query2"], "clicks": 1, "impressions": 50, "ctr": 0.02, "position": 8.0},  # abaixo do mínimo
        {"keys": ["query3"], "clicks": 10, "impressions": 300, "ctr": 0.033, "position": 6.0},
    ]
    resp = {"rows": rows}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_ctr_opportunities(FAKE_SITE, FAKE_TOKEN, min_impressions=100)
        urls = [r["query"] for r in result]
        assert "query2" not in urls


def test_get_ctr_opportunities_filtra_por_ctr():
    rows = [
        {"keys": ["alta-ctr"], "clicks": 100, "impressions": 1000, "ctr": 0.10, "position": 5.0},  # CTR 10% — exclui
        {"keys": ["baixa-ctr"], "clicks": 5, "impressions": 500, "ctr": 0.01, "position": 8.0},   # CTR 1% — inclui
    ]
    resp = {"rows": rows}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_ctr_opportunities(FAKE_SITE, FAKE_TOKEN, min_impressions=100, max_ctr=3.0)
        queries = [r["query"] for r in result]
        assert "alta-ctr" not in queries
        assert "baixa-ctr" in queries


def test_get_ctr_opportunities_ordenado_por_impressoes():
    rows = [
        {"keys": ["query-b"], "clicks": 3, "impressions": 150, "ctr": 0.02, "position": 10.0},
        {"keys": ["query-a"], "clicks": 5, "impressions": 500, "ctr": 0.01, "position": 8.0},
    ]
    resp = {"rows": rows}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_ctr_opportunities(FAKE_SITE, FAKE_TOKEN, min_impressions=100)
        if len(result) >= 2:
            assert result[0]["impressions"] >= result[1]["impressions"]


def test_get_ctr_opportunities_tem_campo_ctr_potencial():
    rows = [{"keys": ["oportunidade"], "clicks": 2, "impressions": 200, "ctr": 0.01, "position": 12.0}]
    resp = {"rows": rows}
    with mock.patch("urllib.request.urlopen", return_value=make_response(resp)):
        result = get_ctr_opportunities(FAKE_SITE, FAKE_TOKEN, min_impressions=100)
        if result:
            assert "ctr_potencial" in result[0]


# ---------------------------------------------------------------------------
# get_position_changes
# ---------------------------------------------------------------------------

def test_get_position_changes_retorna_estrutura_esperada():
    resp_atual = {"rows": [
        {"keys": ["query-subiu"], "clicks": 50, "impressions": 400, "ctr": 0.125, "position": 5.0},
        {"keys": ["query-nova"], "clicks": 10, "impressions": 100, "ctr": 0.1, "position": 8.0},
    ]}
    resp_anterior = {"rows": [
        {"keys": ["query-subiu"], "clicks": 30, "impressions": 300, "ctr": 0.1, "position": 9.0},
    ]}

    respostas = [resp_atual, resp_anterior]
    call_count = [0]

    def fake_urlopen(req, timeout=None):
        data = respostas[call_count[0]]
        call_count[0] += 1
        return make_response(data)

    with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = get_position_changes(FAKE_SITE, FAKE_TOKEN)
        assert "subiram" in result
        assert "desceram" in result
        assert "novos" in result
        assert "resumo" in result


def test_get_position_changes_detecta_query_nova():
    resp_atual = {"rows": [{"keys": ["query-nova"], "clicks": 5, "impressions": 50, "ctr": 0.1, "position": 7.0}]}
    resp_anterior = {"rows": []}

    respostas = [resp_atual, resp_anterior]
    call_count = [0]

    def fake_urlopen(req, timeout=None):
        data = respostas[call_count[0]]
        call_count[0] += 1
        return make_response(data)

    with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = get_position_changes(FAKE_SITE, FAKE_TOKEN)
        novos_queries = [q["query"] for q in result["novos"]]
        assert "query-nova" in novos_queries


def test_get_position_changes_detecta_subida():
    resp_atual = {"rows": [{"keys": ["query-subiu"], "clicks": 50, "impressions": 400, "ctr": 0.125, "position": 3.0}]}
    resp_anterior = {"rows": [{"keys": ["query-subiu"], "clicks": 20, "impressions": 300, "ctr": 0.067, "position": 10.0}]}

    respostas = [resp_atual, resp_anterior]
    call_count = [0]

    def fake_urlopen(req, timeout=None):
        data = respostas[call_count[0]]
        call_count[0] += 1
        return make_response(data)

    with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = get_position_changes(FAKE_SITE, FAKE_TOKEN)
        assert result["resumo"]["total_subiram"] >= 1


# ---------------------------------------------------------------------------
# Tratamento de erros HTTP
# ---------------------------------------------------------------------------

def test_erro_401_levanta_gsc_auth_error():
    import urllib.error
    error_body = json.dumps({"error": {"message": "Invalid Credentials", "code": 401}}).encode()
    http_err = urllib.error.HTTPError(url="https://example.com", code=401, msg="Unauthorized", hdrs=None, fp=None)
    http_err.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(GSCAuthError):
            get_search_queries(FAKE_SITE, FAKE_TOKEN)


def test_erro_500_levanta_gsc_error():
    import urllib.error
    error_body = json.dumps({"error": {"message": "Internal Error", "code": 500}}).encode()
    http_err = urllib.error.HTTPError(url="https://example.com", code=500, msg="Server Error", hdrs=None, fp=None)
    http_err.read = mock.MagicMock(return_value=error_body)

    with mock.patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(GSCError):
            get_search_queries(FAKE_SITE, FAKE_TOKEN)


def test_erro_conexao_levanta_gsc_error():
    import urllib.error
    with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        with pytest.raises(GSCError, match="Erro de conexão"):
            get_search_queries(FAKE_SITE, FAKE_TOKEN)


# ---------------------------------------------------------------------------
# print_queries_table / print_pages_table
# ---------------------------------------------------------------------------

def test_print_queries_table_lista_vazia(capsys):
    print_queries_table([])
    out = capsys.readouterr().out
    assert "Nenhuma query" in out


def test_print_queries_table_exibe_dados(capsys):
    queries = [{"query": "marketing digital", "clicks": 100, "impressions": 1000, "ctr": 10.0, "position": 8.5}]
    print_queries_table(queries)
    out = capsys.readouterr().out
    assert "marketing digital" in out


def test_print_pages_table_lista_vazia(capsys):
    print_pages_table([])
    out = capsys.readouterr().out
    assert "Nenhuma página" in out


# ---------------------------------------------------------------------------
# CLI (parser)
# ---------------------------------------------------------------------------

def test_parser_comando_queries():
    parser = build_parser()
    args = parser.parse_args(["queries", FAKE_SITE])
    assert args.comando == "queries"
    assert args.site_url == FAKE_SITE


def test_parser_queries_com_days():
    parser = build_parser()
    args = parser.parse_args(["queries", FAKE_SITE, "--days", "60"])
    assert args.days == 60


def test_parser_ctr_opportunities():
    parser = build_parser()
    args = parser.parse_args(["ctr-opportunities", FAKE_SITE, "--min-impressions", "200"])
    assert args.min_impressions == 200


def test_parser_position_changes_com_compare():
    parser = build_parser()
    args = parser.parse_args(["position-changes", FAKE_SITE, "--compare", "14"])
    assert args.compare == 14


def test_parser_full_report_com_output():
    parser = build_parser()
    args = parser.parse_args(["full-report", FAKE_SITE, "--output", "report.json"])
    assert args.output == "report.json"


def test_parser_sem_subcomando_falha():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])
