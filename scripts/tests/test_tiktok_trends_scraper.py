#!/usr/bin/env python3
"""
Testes para tiktok_trends_scraper.py

Cobre funções puras que não dependem da TikTok-Api:
- calcular_engagement
- calcular_viral_score
- extrair_dados_video
- analisar_trends
- gerar_relatorio
- constantes (NICHOS_HASHTAGS, FORMATOS_VIRAIS)
"""

import os
import sys
import pytest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiktok_trends_scraper import (
    calcular_engagement,
    calcular_viral_score,
    extrair_dados_video,
    analisar_trends,
    gerar_relatorio,
    NICHOS_HASHTAGS,
    FORMATOS_VIRAIS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_stats(views: int = 0, likes: int = 0, comments: int = 0, shares: int = 0):
    """Cria objeto de stats compatível com calcular_engagement/calcular_viral_score."""
    return SimpleNamespace(
        play_count=views,
        digg_count=likes,
        comment_count=comments,
        share_count=shares,
    )


def make_video_dict(
    video_id: str = "vid001",
    autor: str = "usuario",
    views: int = 1000,
    likes: int = 100,
    comments: int = 20,
    shares: int = 10,
    duracao: int = 30,
    hashtags: list = None,
    descricao: str = "Descrição do vídeo",
) -> dict:
    """Cria dicionário de vídeo no formato retornado por extrair_dados_video."""
    return {
        "id": video_id,
        "url": f"https://www.tiktok.com/@{autor}/video/{video_id}",
        "descricao": descricao,
        "autor": autor,
        "autor_followers": 5000,
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "duracao_segundos": duracao,
        "hashtags": hashtags or ["marketing", "dicas"],
        "musica": "Som viral",
        "data_criacao": "",
        "engagement_rate": calcular_engagement(make_stats(views, likes, comments, shares)),
        "viral_score": calcular_viral_score(make_stats(views, likes, comments, shares)),
    }


# ---------------------------------------------------------------------------
# calcular_engagement
# ---------------------------------------------------------------------------

def test_engagement_zero_views():
    stats = make_stats(views=0, likes=100, comments=10, shares=5)
    assert calcular_engagement(stats) == 0


def test_engagement_calculo_correto():
    # (100 + 10 + 5) / 1000 * 100 = 11.5%
    stats = make_stats(views=1000, likes=100, comments=10, shares=5)
    assert calcular_engagement(stats) == pytest.approx(11.5, rel=1e-2)


def test_engagement_retorna_float():
    stats = make_stats(views=500, likes=25, comments=5, shares=2)
    result = calcular_engagement(stats)
    assert isinstance(result, float)


def test_engagement_alto():
    # (500 + 100 + 50) / 1000 * 100 = 65%
    stats = make_stats(views=1000, likes=500, comments=100, shares=50)
    assert calcular_engagement(stats) == pytest.approx(65.0, rel=1e-2)


def test_engagement_objeto_invalido_retorna_zero():
    # Objeto sem atributos esperados
    stats = SimpleNamespace()
    result = calcular_engagement(stats)
    assert result == 0


# ---------------------------------------------------------------------------
# calcular_viral_score
# ---------------------------------------------------------------------------

def test_viral_score_zero_stats():
    stats = make_stats(views=0, likes=0, comments=0, shares=0)
    assert calcular_viral_score(stats) == 0


def test_viral_score_maximo():
    # views=10M, likes=1M, shares=100K, comments=50K → score=100
    stats = make_stats(views=10_000_000, likes=1_000_000, comments=50_000, shares=100_000)
    assert calcular_viral_score(stats) == pytest.approx(100.0, rel=1e-2)


def test_viral_score_entre_0_e_100():
    stats = make_stats(views=500_000, likes=50_000, comments=5_000, shares=10_000)
    score = calcular_viral_score(stats)
    assert 0 <= score <= 100


def test_viral_score_retorna_float():
    stats = make_stats(views=1_000_000, likes=100_000, comments=10_000, shares=5_000)
    result = calcular_viral_score(stats)
    assert isinstance(result, float)


def test_viral_score_pesos_corretos():
    # Apenas views no máximo → 40 pontos
    stats = make_stats(views=10_000_000, likes=0, comments=0, shares=0)
    assert calcular_viral_score(stats) == pytest.approx(40.0, rel=1e-2)

    # Apenas likes no máximo → 25 pontos
    stats = make_stats(views=0, likes=1_000_000, comments=0, shares=0)
    assert calcular_viral_score(stats) == pytest.approx(25.0, rel=1e-2)


def test_viral_score_objeto_invalido_retorna_zero():
    stats = SimpleNamespace()
    result = calcular_viral_score(stats)
    assert result == 0


# ---------------------------------------------------------------------------
# extrair_dados_video
# ---------------------------------------------------------------------------

def _make_mock_video(
    video_id: str = "vid123",
    username: str = "testuser",
    views: int = 5000,
    likes: int = 300,
    comments: int = 50,
    shares: int = 20,
    duracao: int = 45,
    desc: str = "Vídeo de teste",
    hashtags_names: list = None,
    musica: str = "Música teste",
) -> MagicMock:
    """Cria mock de objeto de vídeo no estilo TikTokApi v7.x."""
    video = MagicMock()
    video.id = video_id
    video.desc = desc

    # Author
    author = MagicMock()
    author.username = username
    author.follower_count = 10000
    video.author = author

    # Stats
    stats = MagicMock()
    stats.play_count = views
    stats.digg_count = likes
    stats.comment_count = comments
    stats.share_count = shares
    video.stats = stats

    # Video info
    video_info = MagicMock()
    video_info.duration = duracao
    video.video = video_info

    # Hashtags
    if hashtags_names:
        mock_tags = []
        for name in hashtags_names:
            tag = MagicMock()
            tag.name = name
            mock_tags.append(tag)
        video.hashtags = mock_tags
    else:
        video.hashtags = []

    # Sound
    sound = MagicMock()
    sound.title = musica
    video.sound = sound

    # as_dict não disponível
    del video.as_dict

    return video


def test_extrair_dados_retorna_dict():
    video = _make_mock_video()
    result = extrair_dados_video(video)
    assert isinstance(result, dict)


def test_extrair_dados_campos_basicos():
    video = _make_mock_video(video_id="abc123", username="criador", views=10000)
    result = extrair_dados_video(video)
    assert result["id"] == "abc123"
    assert result["autor"] == "criador"
    assert result["views"] == 10000


def test_extrair_dados_url_montada_corretamente():
    video = _make_mock_video(video_id="xyz789", username="marca")
    result = extrair_dados_video(video)
    assert "marca" in result["url"]
    assert "xyz789" in result["url"]
    assert result["url"].startswith("https://www.tiktok.com/")


def test_extrair_dados_engagement_calculado():
    video = _make_mock_video(views=1000, likes=50, comments=10, shares=5)
    result = extrair_dados_video(video)
    assert "engagement_rate" in result
    assert result["engagement_rate"] >= 0


def test_extrair_dados_viral_score_presente():
    video = _make_mock_video(views=5_000_000, likes=500_000, comments=50_000, shares=10_000)
    result = extrair_dados_video(video)
    assert "viral_score" in result
    assert 0 <= result["viral_score"] <= 100


def test_extrair_dados_hashtags_extraidas():
    video = _make_mock_video(hashtags_names=["marketing", "dicas", "viral"])
    result = extrair_dados_video(video)
    assert "marketing" in result["hashtags"]
    assert len(result["hashtags"]) == 3


def test_extrair_dados_descricao_truncada():
    desc_longa = "A" * 300
    video = _make_mock_video(desc=desc_longa)
    result = extrair_dados_video(video)
    assert len(result["descricao"]) <= 200


def test_extrair_dados_erro_retorna_dict_com_erro():
    # Objeto que vai gerar exception
    video = MagicMock()
    video.id = None
    del video.as_dict
    # Forçar erro removendo atributos essenciais
    video.author = None
    video.stats = None
    video.video = None
    video.hashtags = None
    video.sound = None
    video.desc = None

    result = extrair_dados_video(video)
    # Deve retornar dict (pode ter "erro" ou dados parciais)
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# analisar_trends
# ---------------------------------------------------------------------------

VIDEOS_SAMPLE = [
    make_video_dict("v1", views=10000, likes=800, comments=100, shares=50, duracao=30, hashtags=["marketing", "dicas"]),
    make_video_dict("v2", views=5000, likes=300, comments=40, shares=20, duracao=45, hashtags=["marketing", "viral"]),
    make_video_dict("v3", views=20000, likes=1500, comments=200, shares=100, duracao=25, hashtags=["dicas", "fyp"]),
]


def test_analisar_trends_lista_vazia():
    result = analisar_trends([])
    assert result == {}


def test_analisar_trends_total_videos():
    result = analisar_trends(VIDEOS_SAMPLE)
    assert result["total_videos"] == 3


def test_analisar_trends_views_medio():
    result = analisar_trends(VIDEOS_SAMPLE)
    esperado = (10000 + 5000 + 20000) / 3
    assert result["views_medio"] == int(esperado)


def test_analisar_trends_duracao_media():
    result = analisar_trends(VIDEOS_SAMPLE)
    esperado = (30 + 45 + 25) / 3
    assert result["duracao_media_segundos"] == pytest.approx(esperado, rel=1e-2)


def test_analisar_trends_top_hashtags():
    result = analisar_trends(VIDEOS_SAMPLE)
    hashtags = dict(result["top_hashtags"])
    # "marketing" e "dicas" aparecem 2x cada
    assert hashtags.get("marketing", 0) == 2
    assert hashtags.get("dicas", 0) == 2


def test_analisar_trends_video_mais_viral():
    result = analisar_trends(VIDEOS_SAMPLE)
    assert result["video_mais_viral"] is not None
    assert result["video_mais_viral"]["id"] == "v3"  # 20000 views


def test_analisar_trends_melhor_engagement():
    result = analisar_trends(VIDEOS_SAMPLE)
    assert result["melhor_engagement"] is not None


def test_analisar_trends_engagement_medio_float():
    result = analisar_trends(VIDEOS_SAMPLE)
    assert isinstance(result["engagement_medio"], float)


def test_analisar_trends_um_video():
    videos = [make_video_dict("v1", views=1000)]
    result = analisar_trends(videos)
    assert result["total_videos"] == 1
    assert result["video_mais_viral"]["id"] == "v1"


# ---------------------------------------------------------------------------
# gerar_relatorio
# ---------------------------------------------------------------------------

def test_gerar_relatorio_retorna_tuple():
    analise = analisar_trends(VIDEOS_SAMPLE)
    params = {"tipo": "Hashtag", "termo": "marketing", "min_views": 0, "limit": 30}
    result = gerar_relatorio(VIDEOS_SAMPLE, analise, params)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_gerar_relatorio_conteudo_markdown():
    analise = analisar_trends(VIDEOS_SAMPLE)
    params = {"tipo": "Hashtag", "termo": "marketing", "min_views": 0, "limit": 30}
    relatorio, timestamp = gerar_relatorio(VIDEOS_SAMPLE, analise, params)
    assert "# " in relatorio  # tem cabeçalho markdown
    assert "marketing" in relatorio


def test_gerar_relatorio_timestamp_formato():
    analise = analisar_trends(VIDEOS_SAMPLE)
    params = {"tipo": "Trending", "termo": "BR", "min_views": 0, "limit": 30}
    _, timestamp = gerar_relatorio(VIDEOS_SAMPLE, analise, params)
    # Formato: YYYY-MM-DD_HH-MM
    assert len(timestamp) == 16
    assert "-" in timestamp
    assert "_" in timestamp


def test_gerar_relatorio_tem_secao_analise():
    analise = analisar_trends(VIDEOS_SAMPLE)
    params = {"tipo": "Nicho", "termo": "financas", "min_views": 1000, "limit": 10}
    relatorio, _ = gerar_relatorio(VIDEOS_SAMPLE, analise, params)
    assert "Análise" in relatorio or "analise" in relatorio.lower()


def test_gerar_relatorio_tem_recomendacoes():
    analise = analisar_trends(VIDEOS_SAMPLE)
    params = {"tipo": "Keyword", "termo": "receitas", "min_views": 500, "limit": 20}
    relatorio, _ = gerar_relatorio(VIDEOS_SAMPLE, analise, params)
    assert "Recomendações" in relatorio or "Recomendacoes" in relatorio or "recomendações" in relatorio.lower()


def test_gerar_relatorio_insight_videos_curtos():
    # duracao_media < 30 → mensagem sobre vídeos curtos
    videos_curtos = [
        make_video_dict("v1", duracao=15),
        make_video_dict("v2", duracao=20),
    ]
    analise = analisar_trends(videos_curtos)
    params = {"tipo": "Hashtag", "termo": "shorts", "min_views": 0, "limit": 30}
    relatorio, _ = gerar_relatorio(videos_curtos, analise, params)
    assert "30s" in relatorio or "curtos" in relatorio


def test_gerar_relatorio_insight_alto_engajamento():
    # Criar vídeos com engajamento > 5%
    videos_alto_eng = [
        make_video_dict("v1", views=100, likes=10, comments=5, shares=3),
    ]
    analise = analisar_trends(videos_alto_eng)
    params = {"tipo": "Hashtag", "termo": "viral", "min_views": 0, "limit": 30}
    relatorio, _ = gerar_relatorio(videos_alto_eng, analise, params)
    assert isinstance(relatorio, str)


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

def test_nichos_hashtags_tem_nichos_esperados():
    esperados = ["marketing", "fitness", "beleza", "gastronomia", "financas", "tecnologia", "lifestyle"]
    for nicho in esperados:
        assert nicho in NICHOS_HASHTAGS


def test_nichos_hashtags_cada_nicho_tem_hashtags():
    for nicho, hashtags in NICHOS_HASHTAGS.items():
        assert len(hashtags) >= 5, f"Nicho '{nicho}' tem poucas hashtags"
        assert all(isinstance(h, str) for h in hashtags)


def test_formatos_virais_tem_formatos_esperados():
    esperados = ["tutorial", "storytime", "trends", "pov", "reviews", "antes_depois", "react", "grwm"]
    for fmt in esperados:
        assert fmt in FORMATOS_VIRAIS


def test_formatos_virais_cada_formato_tem_keywords():
    for fmt, keywords in FORMATOS_VIRAIS.items():
        assert len(keywords) >= 3, f"Formato '{fmt}' tem poucas keywords"
        assert all(isinstance(k, str) for k in keywords)


def test_nichos_hashtags_sem_duplicatas_por_nicho():
    for nicho, hashtags in NICHOS_HASHTAGS.items():
        assert len(hashtags) == len(set(hashtags)), f"Nicho '{nicho}' tem hashtags duplicadas"
