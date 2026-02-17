#!/usr/bin/env python3
"""
Testes para weekly_report.py
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from weekly_report import (
    get_current_week,
    get_week_dates,
    parse_week_number,
    collect_content_metrics,
    collect_seo_metrics,
    generate_next_week_recommendations,
    generate_suggested_calendar,
    generate_weekly_report,
    export_report,
    load_week_data,
    BENCHMARKS,
    CONTENT_THEMES_BY_DAY,
)


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def sample_content_list():
    return [
        {
            "titulo": "7 estratégias de marketing",
            "plataforma": "instagram",
            "formato": "carrossel",
            "alcance": 5000,
            "engajamentos": 300,
            "saves": 80,
            "shares": 40,
            "data": "2026-02-10",
        },
        {
            "titulo": "Como usar IA no marketing",
            "plataforma": "instagram",
            "formato": "reels",
            "alcance": 8000,
            "engajamentos": 600,
            "data": "2026-02-11",
        },
        {
            "titulo": "Dica de produtividade",
            "plataforma": "linkedin",
            "formato": "post",
            "alcance": 2000,
            "engajamentos": 100,
            "data": "2026-02-12",
        },
    ]


@pytest.fixture
def sample_seo_list():
    return [
        {
            "url": "https://exemplo.com/artigo-1",
            "titulo": "Artigo sobre marketing digital",
            "posicao_media": 8.5,
            "impressoes": 1200,
            "cliques": 48,
            "ctr": 4.0,
        },
        {
            "url": "https://exemplo.com/artigo-2",
            "titulo": "Como criar funil de vendas",
            "posicao_media": 3.2,
            "impressoes": 3000,
            "cliques": 270,
            "ctr": 9.0,
        },
        {
            "url": "https://exemplo.com/artigo-3",
            "titulo": "Tendências de SEO",
            "posicao_media": 12.0,
            "impressoes": 500,
            "cliques": 10,
            "ctr": 2.0,
        },
    ]


@pytest.fixture
def sample_email_metrics():
    return {
        "enviados": 2500,
        "taxa_abertura": 32.5,
        "taxa_clique": 4.8,
        "taxa_conversao": 1.2,
        "taxa_descadastro": 0.1,
    }


@pytest.fixture
def sample_week_data(sample_content_list, sample_seo_list, sample_email_metrics):
    return {
        "week": "2026-W07",
        "content": sample_content_list,
        "seo": sample_seo_list,
        "email": sample_email_metrics,
    }


# ──────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────

def test_benchmarks_tem_plataformas():
    assert "instagram" in BENCHMARKS
    assert "email" in BENCHMARKS
    assert "linkedin" in BENCHMARKS


def test_benchmarks_email_tem_campos():
    email = BENCHMARKS["email"]
    assert "taxa_abertura" in email
    assert "taxa_clique" in email


def test_content_themes_tem_7_dias():
    assert len(CONTENT_THEMES_BY_DAY) == 7


def test_content_themes_tem_campos():
    for dia, info in CONTENT_THEMES_BY_DAY.items():
        assert "tema" in info
        assert "formatos" in info
        assert len(info["formatos"]) >= 1


# ──────────────────────────────────────────────
# Utilitários de data
# ──────────────────────────────────────────────

def test_get_current_week_formato():
    week = get_current_week()
    import re
    assert re.match(r'^\d{4}-W\d{2}$', week), f"Formato inválido: {week}"


def test_get_week_dates_retorna_tuple():
    start, end = get_week_dates("2026-W07")
    assert start is not None
    assert end is not None


def test_get_week_dates_diferenca_6_dias():
    start, end = get_week_dates("2026-W07")
    delta = end - start
    assert delta.days == 6


def test_get_week_dates_formato_invalido():
    with pytest.raises(ValueError):
        get_week_dates("semana-invalida")


def test_get_week_dates_inicio_e_fim_corretos():
    start, end = get_week_dates("2026-W07")
    # Segunda-feira = 0, Domingo = 6
    assert start.weekday() == 0  # Segunda-feira
    assert end.weekday() == 6    # Domingo


def test_parse_week_number():
    assert parse_week_number("2026-W07") == 7
    assert parse_week_number("2026-W52") == 52
    assert parse_week_number("2026-W01") == 1


def test_parse_week_number_invalido():
    with pytest.raises(ValueError):
        parse_week_number("formato-invalido")


# ──────────────────────────────────────────────
# collect_content_metrics
# ──────────────────────────────────────────────

def test_collect_content_metrics_lista_vazia():
    result = collect_content_metrics([])
    assert result["total_pecas"] == 0
    assert result["alcance_total"] == 0
    assert result["engajamento_total"] == 0
    assert result["taxa_engajamento_media"] == 0.0


def test_collect_content_metrics_total_pecas(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    assert result["total_pecas"] == 3


def test_collect_content_metrics_alcance_total(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    assert result["alcance_total"] == 15000  # 5000 + 8000 + 2000


def test_collect_content_metrics_engajamento_total(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    assert result["engajamento_total"] == 1000  # 300 + 600 + 100


def test_collect_content_metrics_taxa_engajamento(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    assert result["taxa_engajamento_media"] > 0


def test_collect_content_metrics_top_conteudos(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    assert len(result["top_conteudos"]) <= 3
    assert len(result["top_conteudos"]) >= 1


def test_collect_content_metrics_por_plataforma(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    por_plat = result["por_plataforma"]
    assert "instagram" in por_plat
    assert "linkedin" in por_plat
    assert por_plat["instagram"]["pecas"] == 2
    assert por_plat["linkedin"]["pecas"] == 1


def test_collect_content_metrics_por_formato(sample_content_list):
    result = collect_content_metrics(sample_content_list)
    por_fmt = result["por_formato"]
    assert "carrossel" in por_fmt
    assert "reels" in por_fmt
    assert "post" in por_fmt


# ──────────────────────────────────────────────
# collect_seo_metrics
# ──────────────────────────────────────────────

def test_collect_seo_metrics_lista_vazia():
    result = collect_seo_metrics([])
    assert result["total_urls"] == 0
    assert result["impressoes_total"] == 0
    assert result["cliques_total"] == 0


def test_collect_seo_metrics_total_urls(sample_seo_list):
    result = collect_seo_metrics(sample_seo_list)
    assert result["total_urls"] == 3


def test_collect_seo_metrics_impressoes(sample_seo_list):
    result = collect_seo_metrics(sample_seo_list)
    assert result["impressoes_total"] == 4700  # 1200 + 3000 + 500


def test_collect_seo_metrics_cliques(sample_seo_list):
    result = collect_seo_metrics(sample_seo_list)
    assert result["cliques_total"] == 328  # 48 + 270 + 10


def test_collect_seo_metrics_ctr_medio(sample_seo_list):
    result = collect_seo_metrics(sample_seo_list)
    assert result["ctr_medio"] > 0


def test_collect_seo_metrics_quick_wins(sample_seo_list):
    result = collect_seo_metrics(sample_seo_list)
    # artigo-3 está na posição 12 com CTR 2% — é um quick win
    quick_wins = result["quick_wins"]
    assert len(quick_wins) >= 1


def test_collect_seo_metrics_top_paginas(sample_seo_list):
    result = collect_seo_metrics(sample_seo_list)
    top = result["top_paginas"]
    assert len(top) >= 1
    # Deve estar ordenado por cliques (artigo-2 tem mais cliques)
    assert top[0].get("cliques", 0) >= top[-1].get("cliques", 0)


# ──────────────────────────────────────────────
# generate_next_week_recommendations
# ──────────────────────────────────────────────

def test_recommendations_retorna_lista(sample_content_list, sample_seo_list):
    content_metrics = collect_content_metrics(sample_content_list)
    seo_metrics = collect_seo_metrics(sample_seo_list)
    recs = generate_next_week_recommendations(content_metrics, seo_metrics)
    assert isinstance(recs, list)
    assert len(recs) >= 1


def test_recommendations_texto_nao_vazio(sample_content_list, sample_seo_list):
    content_metrics = collect_content_metrics(sample_content_list)
    seo_metrics = collect_seo_metrics(sample_seo_list)
    recs = generate_next_week_recommendations(content_metrics, seo_metrics)
    for rec in recs:
        assert isinstance(rec, str)
        assert len(rec) > 10


def test_recommendations_sem_dados():
    content_metrics = collect_content_metrics([])
    seo_metrics = collect_seo_metrics([])
    recs = generate_next_week_recommendations(content_metrics, seo_metrics)
    assert len(recs) >= 1


def test_recommendations_email_baixo_taxa_abertura():
    content_metrics = collect_content_metrics([])
    seo_metrics = collect_seo_metrics([])
    email_metrics = {"taxa_abertura": 10.0}  # Baixo
    recs = generate_next_week_recommendations(content_metrics, seo_metrics, email_metrics)
    assert any("abertura" in rec.lower() or "email" in rec.lower() for rec in recs)


# ──────────────────────────────────────────────
# generate_suggested_calendar
# ──────────────────────────────────────────────

def test_generate_calendar_retorna_lista():
    calendario = generate_suggested_calendar("2026-W07", ["instagram"])
    assert isinstance(calendario, list)


def test_generate_calendar_7_dias():
    calendario = generate_suggested_calendar("2026-W07", ["instagram"])
    datas = set(item["data"] for item in calendario)
    assert len(datas) == 7


def test_generate_calendar_multiplas_plataformas():
    calendario = generate_suggested_calendar("2026-W07", ["instagram", "linkedin"])
    plataformas = set(item["plataforma"] for item in calendario)
    assert "instagram" in plataformas
    assert "linkedin" in plataformas


def test_generate_calendar_tem_campos():
    calendario = generate_suggested_calendar("2026-W07", ["instagram"])
    for item in calendario:
        assert "data" in item
        assert "dia_semana" in item
        assert "plataforma" in item
        assert "tema" in item
        assert "formato_sugerido" in item


def test_generate_calendar_semana_invalida():
    calendario = generate_suggested_calendar("formato-invalido", ["instagram"])
    assert isinstance(calendario, list)


# ──────────────────────────────────────────────
# generate_weekly_report
# ──────────────────────────────────────────────

def test_generate_weekly_report_retorna_string(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert isinstance(report, str)
    assert len(report) > 100


def test_generate_weekly_report_tem_titulo(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert "Relatório Semanal" in report


def test_generate_weekly_report_tem_resumo(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert "Resumo Executivo" in report


def test_generate_weekly_report_tem_recomendacoes(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert "Recomendações" in report


def test_generate_weekly_report_tem_email(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert "Email Marketing" in report


def test_generate_weekly_report_tem_seo(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert "SEO" in report


def test_generate_weekly_report_sem_dados():
    report = generate_weekly_report({"week": "2026-W07"})
    assert isinstance(report, str)
    assert "Relatório Semanal" in report


def test_generate_weekly_report_semana_no_titulo(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    assert "2026" in report


def test_generate_weekly_report_formato_markdown(sample_week_data):
    report = generate_weekly_report(sample_week_data)
    # Deve conter elementos de Markdown
    assert "#" in report
    assert "|" in report  # Tabelas


# ──────────────────────────────────────────────
# export_report
# ──────────────────────────────────────────────

def test_export_report_cria_arquivo(tmp_path, sample_week_data):
    report = generate_weekly_report(sample_week_data)
    output_path = str(tmp_path / "relatorio.md")
    resultado = export_report(report, output_path)
    assert os.path.exists(resultado)


def test_export_report_conteudo_correto(tmp_path, sample_week_data):
    report = generate_weekly_report(sample_week_data)
    output_path = str(tmp_path / "relatorio.md")
    export_report(report, output_path)
    with open(output_path, encoding='utf-8') as f:
        conteudo = f.read()
    assert conteudo == report


def test_export_report_retorna_caminho(tmp_path, sample_week_data):
    report = generate_weekly_report(sample_week_data)
    output_path = str(tmp_path / "relatorio.md")
    resultado = export_report(report, output_path)
    assert isinstance(resultado, str)
    assert resultado == output_path


# ──────────────────────────────────────────────
# load_week_data
# ──────────────────────────────────────────────

def test_load_week_data_arquivo_valido(tmp_path):
    dados = {"week": "2026-W07", "content": []}
    arquivo = tmp_path / "dados.json"
    arquivo.write_text(json.dumps(dados), encoding='utf-8')
    resultado = load_week_data(str(arquivo))
    assert resultado["week"] == "2026-W07"
    assert "content" in resultado


def test_load_week_data_arquivo_nao_existente():
    with pytest.raises(FileNotFoundError):
        load_week_data("/caminho/que/nao/existe.json")
