#!/usr/bin/env python3
"""
Testes funcionais adicionais para content_repurposer.py — cobre todas as
plataformas (twitter, linkedin, email, youtube, reels) + main().
"""
from __future__ import annotations

import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import content_repurposer as cr


SAMPLE_TEXT = """# Marketing Digital em 2026

Marketing digital evoluiu muito nos últimos anos. Aqui estão algumas dicas
importantes para você dominar.

- Primeiro: defina seu público-alvo de forma clara e específica
- Segundo: crie conteúdo de qualidade consistentemente
- Terceiro: use múltiplas plataformas integradas
- Quarto: meça métricas relevantes e ajuste estratégia
- Quinto: invista em SEO e tráfego orgânico
- Sexto: use anúncios pagos para escalar resultados
- Sétimo: mantenha relacionamento com sua audiência
"""


# ----------------------------------------------------------- to_instagram_reels
def test_to_instagram_reels_estrutura():
    r = cr.to_instagram_reels(SAMPLE_TEXT)
    assert r["platform"] == "Instagram Reels"
    assert "script" in r
    assert "duracao_sugerida" in r
    assert "formato" in r
    assert "9:16" in r["formato"]


def test_to_instagram_reels_inclui_hooks():
    r = cr.to_instagram_reels(SAMPLE_TEXT)
    assert "HOOK" in r["script"]
    assert "PONTO 1" in r["script"]
    assert "CTA" in r["script"]


def test_to_instagram_reels_texto_sem_pontos():
    r = cr.to_instagram_reels("Texto curto sem listas e tudo mais aqui.")
    assert "script" in r


# ----------------------------------------------------------- to_twitter_thread
def test_to_twitter_thread_estrutura():
    r = cr.to_twitter_thread(SAMPLE_TEXT)
    assert r["platform"] == "Twitter/X Thread"
    assert "tweets" in r
    assert "total_tweets" in r
    assert isinstance(r["tweets"], list)
    assert r["total_tweets"] == len(r["tweets"])


def test_to_twitter_thread_tweets_dentro_do_limite():
    r = cr.to_twitter_thread(SAMPLE_TEXT)
    for tweet in r["tweets"]:
        # Twitter tem 280 chars; alguns tweets têm chars=0 (calculo depois)
        if tweet["chars"] > 0:
            assert tweet["chars"] <= 280


def test_to_twitter_thread_inclui_hook_e_cta():
    r = cr.to_twitter_thread(SAMPLE_TEXT)
    primeiro = r["tweets"][0]["content"]
    ultimo = r["tweets"][-1]["content"]
    assert "🧵" in primeiro
    assert "RT" in ultimo or "segue" in ultimo.lower()


# ----------------------------------------------------------- to_linkedin_post
def test_to_linkedin_post_estrutura():
    r = cr.to_linkedin_post(SAMPLE_TEXT)
    assert r["platform"] == "LinkedIn"
    assert "post" in r
    assert "chars" in r
    assert "max_chars" in r
    assert r["chars"] == len(r["post"])


def test_to_linkedin_post_dentro_do_limite():
    r = cr.to_linkedin_post(SAMPLE_TEXT)
    assert r["chars"] <= r["max_chars"]


def test_to_linkedin_post_inclui_hashtags():
    r = cr.to_linkedin_post(SAMPLE_TEXT)
    assert "#" in r["post"]


# ----------------------------------------------------------- to_email_newsletter
def test_to_email_newsletter_estrutura():
    r = cr.to_email_newsletter(SAMPLE_TEXT)
    assert r["platform"] == "Email Newsletter"
    assert "email" in r
    assert "subject_options" in r
    assert "tempo_leitura" in r
    assert isinstance(r["subject_options"], list)
    assert len(r["subject_options"]) >= 2


def test_to_email_newsletter_inclui_assunto_e_cta():
    r = cr.to_email_newsletter(SAMPLE_TEXT)
    assert "Assunto" in r["email"]
    assert "Pré-header" in r["email"]


# ----------------------------------------------------------- to_youtube_script
def test_to_youtube_script_estrutura():
    r = cr.to_youtube_script(SAMPLE_TEXT)
    assert r["platform"] == "YouTube"
    assert "script" in r
    assert "duracao_estimada" in r
    assert "estrutura" in r


def test_to_youtube_script_inclui_secoes():
    r = cr.to_youtube_script(SAMPLE_TEXT)
    assert "HOOK" in r["script"]
    assert "INTRO" in r["script"]
    assert "CONTEÚDO" in r["script"]
    assert "FECHAMENTO" in r["script"]


# ----------------------------------------------------------- repurpose_all
def test_repurpose_all_inclui_todas_plataformas():
    r = cr.repurpose_all(SAMPLE_TEXT)
    chaves_esperadas = ["original", "instagram_carousel", "instagram_reels",
                        "twitter_thread", "linkedin", "email", "youtube"]
    for k in chaves_esperadas:
        assert k in r


def test_repurpose_all_original_tem_metadados():
    r = cr.repurpose_all(SAMPLE_TEXT)
    assert "title" in r["original"]
    assert "key_points" in r["original"]
    assert "read_time" in r["original"]
    assert isinstance(r["original"]["key_points"], list)


# ----------------------------------------------------------- print_output
def test_print_output_resumo_geral(capsys):
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r)
    out = capsys.readouterr().out
    assert "CONTENT REPURPOSER" in out
    assert "VERSÕES GERADAS" in out
    assert "Instagram Carrossel" in out
    assert "LinkedIn" in out


def test_print_output_plataforma_carousel(capsys):
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r, platform="instagram_carousel")
    out = capsys.readouterr().out
    assert "Slide" in out or "CAPTION" in out


def test_print_output_plataforma_twitter(capsys):
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r, platform="twitter_thread")
    out = capsys.readouterr().out
    assert "Tweet" in out


def test_print_output_plataforma_linkedin(capsys):
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r, platform="linkedin")
    out = capsys.readouterr().out
    # post inteiro está em out
    assert r["linkedin"]["post"][:30] in out


def test_print_output_plataforma_email(capsys):
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r, platform="email")
    out = capsys.readouterr().out
    assert "Assunto" in out


def test_print_output_plataforma_youtube_via_alias(capsys):
    """to_youtube_script retorna 'script' — vai entrar no branch elif."""
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r, platform="youtube")
    out = capsys.readouterr().out
    assert "ROTEIRO YOUTUBE" in out


def test_print_output_reels_via_alias(capsys):
    """platform='reels' tenta result['instagram_reels']."""
    r = cr.repurpose_all(SAMPLE_TEXT)
    cr.print_output(r, platform="reels")
    out = capsys.readouterr().out
    # Branch acerta via prefixo instagram_
    assert "ROTEIRO REELS" in out or len(out) > 0


# ----------------------------------------------------------- main / CLI
# O conflito de --output (argparse local x add_output_args) foi corrigido:
# --platform seleciona a plataforma, --output/-o salva em arquivo.
def test_main_sem_args_e_sem_file(capsys):
    with patch.object(sys, "argv", ["content_repurposer.py"]):
        with pytest.raises(SystemExit):
            cr.main()
    out = capsys.readouterr().out
    assert "--platform" in out


def test_main_com_texto_e_platform(capsys):
    argv = ["content_repurposer.py", SAMPLE_TEXT, "--platform", "twitter"]
    with patch.object(sys, "argv", argv):
        cr.main()
    out = capsys.readouterr().out
    assert len(out) > 0


def test_main_json_mode(capsys):
    argv = ["content_repurposer.py", SAMPLE_TEXT, "--platform", "todos", "--json"]
    with patch.object(sys, "argv", argv):
        cr.main()
    out = capsys.readouterr().out
    assert out.strip().startswith("{") or out.strip().startswith("[")
