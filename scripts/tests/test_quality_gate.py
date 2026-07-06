"""Testes para quality_gate.py — validação de qualidade de conteúdo."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quality_gate import (
    check_accents,
    check_ai_tells,
    check_hook,
    check_cta,
    check_readability,
    check_format_compliance,
    check_hashtags,
    AI_TELL_PATTERNS,
    MUST_ACCENT_WORDS,
    PLATFORM_LIMITS,
    STRONG_CTA_WORDS,
    WEAK_CTA_WORDS,
)


class TestCheckAccents:
    """Testes para verificação de acentuação."""

    def test_text_with_correct_accents(self, sample_post):
        score, issues = check_accents(sample_post)
        assert score >= 8
        assert len(issues) == 0

    def test_text_without_accents(self, sample_unaccented_text):
        score, issues = check_accents(sample_unaccented_text)
        assert score < 8
        assert len(issues) > 0

    def test_detects_voce_without_accent(self):
        score, issues = check_accents("voce precisa ver isso agora mesmo")
        found = any("voce" in i and "você" in i for i in issues)
        assert found

    def test_detects_nao_without_accent(self):
        score, issues = check_accents("eu nao sei o que fazer com isso")
        found = any("nao" in i and "não" in i for i in issues)
        assert found

    def test_detects_estrategia_without_accent(self):
        score, issues = check_accents("minha estrategia de marketing digital")
        found = any("estrategia" in i and "estratégia" in i for i in issues)
        assert found

    def test_empty_text(self):
        score, issues = check_accents("")
        assert isinstance(score, int)
        assert isinstance(issues, list)

    def test_short_text_without_accents_no_warning(self):
        """Texto curto sem acentos não deve gerar aviso de texto longo."""
        score, issues = check_accents("hello world")
        long_warnings = [i for i in issues if "Texto longo sem nenhum acento" in i]
        assert len(long_warnings) == 0

    def test_long_text_without_any_accent_warns(self):
        """Texto longo (>100 chars) sem nenhum acento gera aviso."""
        text = "a " * 60  # >100 chars, sem acento
        score, issues = check_accents(text)
        long_warnings = [i for i in issues if "Texto longo sem nenhum acento" in i]
        assert len(long_warnings) == 1

    def test_score_range(self):
        """Score deve estar entre 0 e 10."""
        score, _ = check_accents("texto com acentuação correta: você não está")
        assert 0 <= score <= 10

    def test_all_must_accent_words_have_corrections(self):
        """Todas as palavras em MUST_ACCENT_WORDS devem ter correções."""
        for wrong, correct in MUST_ACCENT_WORDS.items():
            assert wrong != correct
            assert len(correct) > 0


class TestCheckHook:
    """Testes para avaliação de hook."""

    def test_strong_hook_with_number(self):
        content = "5 erros que você comete todo dia\n\nConteúdo do post..."
        score, hook, issues = check_hook(content)
        assert score >= 7
        assert "5 erros" in hook

    def test_strong_hook_with_question(self):
        content = "Você sabe por que sua estratégia não funciona?\n\nExplicação..."
        score, hook, issues = check_hook(content)
        assert score >= 7

    def test_weak_hook(self):
        content = "Texto simples sem padrão forte\n\nContinuação do texto"
        score, hook, issues = check_hook(content)
        assert score < 8

    def test_empty_content(self):
        score, hook, issues = check_hook("")
        assert score == 0
        assert len(issues) > 0

    def test_only_headers(self):
        content = "# Título do artigo\n## Subtítulo"
        score, hook, issues = check_hook(content)
        # Deve ignorar headers e não encontrar conteúdo
        assert isinstance(score, int)

    def test_very_short_hook(self):
        content = "Oi.\n\nConteúdo depois."
        score, hook, issues = check_hook(content)
        short_issues = [i for i in issues if "muito curto" in i]
        assert len(short_issues) > 0

    def test_very_long_hook(self):
        content = "a " * 150 + "\n\nConteúdo depois."
        score, hook, issues = check_hook(content)
        long_issues = [i for i in issues if "muito longo" in i]
        assert len(long_issues) > 0

    def test_hook_score_range(self):
        """Score deve estar entre 0 e 10."""
        score, _, _ = check_hook("5 segredos que você precisa saber\n\nConteúdo")
        assert 0 <= score <= 10

    def test_como_pattern(self):
        content = "Como criar conteúdo viral\n\nPasso 1..."
        score, hook, issues = check_hook(content)
        assert score >= 6  # "Como" pattern + tamanho ok


class TestCheckCTA:
    """Testes para verificação de CTA."""

    def test_strong_cta_at_end(self):
        content = "Conteúdo excelente aqui.\n\nGaranta sua vaga agora!"
        score, issues = check_cta(content)
        assert score >= 7

    def test_weak_cta(self):
        content = "Conteúdo aqui.\n\nClique aqui para saber mais."
        score, issues = check_cta(content)
        assert score < 7
        weak_issues = [i for i in issues if "CTA fraco" in i]
        assert len(weak_issues) > 0

    def test_no_cta(self):
        content = "Conteúdo sem chamada para ação nenhuma."
        score, issues = check_cta(content)
        assert score == 0
        no_cta = [i for i in issues if "Nenhum CTA" in i]
        assert len(no_cta) > 0

    def test_cta_not_at_end(self):
        content = "Garanta sua vaga.\n\n" + "Texto informativo.\n" * 10
        score, issues = check_cta(content)
        position_issues = [i for i in issues if "final" in i]
        assert len(position_issues) > 0

    def test_multiple_strong_ctas(self):
        content = "Comece agora.\n\n" * 5 + "\n\nGaranta sua vaga!"
        score, issues = check_cta(content)
        assert score >= 7

    def test_score_range(self):
        """Score deve estar entre 0 e 10."""
        score, _ = check_cta("Garanta sua vaga agora!")
        assert 0 <= score <= 10


class TestCheckReadability:
    """Testes para verificação de legibilidade."""

    def test_good_readability(self):
        content = "Frases curtas funcionam. Texto direto. Fácil de ler.\n\nNovo parágrafo aqui."
        score, issues = check_readability(content)
        assert score >= 8

    def test_poor_readability_long_sentences(self):
        long_sentence = " ".join(["palavra"] * 30) + ". "
        content = long_sentence * 5
        score, issues = check_readability(content)
        assert score < 7

    def test_long_paragraphs(self):
        long_para = " ".join(["palavra"] * 100)
        content = long_para
        score, issues = check_readability(content)
        para_issues = [i for i in issues if "parágrafo" in i]
        assert len(para_issues) > 0

    def test_empty_content(self):
        score, issues = check_readability("")
        assert isinstance(score, int)

    def test_markdown_stripped(self):
        """Headers e formatação markdown devem ser removidos para análise."""
        content = "# Título\n\n**Texto** com _formatação_. Frase curta."
        score, issues = check_readability(content)
        assert isinstance(score, int)

    def test_score_range(self):
        """Score deve estar entre 0 e 10."""
        score, _ = check_readability("Texto normal. Com frases curtas. Fácil de ler.")
        assert 0 <= score <= 10


class TestCheckFormatCompliance:
    """Testes para verificação de conformidade de formato."""

    def test_post_within_limit(self):
        content = "Post curto de teste" * 10  # Bem abaixo de 2200
        score, issues = check_format_compliance(content, "post")
        assert score == 10

    def test_post_exceeds_limit(self):
        content = "x" * 2300
        score, issues = check_format_compliance(content, "post")
        assert score < 10
        limit_issues = [i for i in issues if "excede" in i]
        assert len(limit_issues) > 0

    def test_article_too_short(self):
        content = "Artigo muito curto."
        score, issues = check_format_compliance(content, "artigo")
        assert score < 10

    def test_article_good_length(self, sample_article):
        score, issues = check_format_compliance(sample_article, "artigo")
        assert score >= 5

    def test_article_needs_headers(self):
        content = " ".join(["palavra"] * 900)  # Sem headers
        score, issues = check_format_compliance(content, "artigo")
        header_issues = [i for i in issues if "header" in i.lower()]
        assert len(header_issues) > 0

    def test_email_subject_too_long(self):
        content = "x" * 60 + "\n\nCorpo do email aqui."
        score, issues = check_format_compliance(content, "email")
        subject_issues = [i for i in issues if "Subject" in i]
        assert len(subject_issues) > 0

    def test_email_subject_ok(self, sample_email):
        score, issues = check_format_compliance(sample_email, "email")
        subject_issues = [i for i in issues if "Subject" in i]
        assert len(subject_issues) == 0

    def test_landing_page_missing_sections(self):
        content = "Apenas texto sem seções definidas."
        score, issues = check_format_compliance(content, "landing-page")
        assert score < 10

    def test_ad_too_long(self):
        content = " ".join(["palavra"] * 200)
        score, issues = check_format_compliance(content, "anuncio")
        assert score < 10

    def test_ad_good_length(self):
        content = " ".join(["palavra"] * 50)
        score, issues = check_format_compliance(content, "anuncio")
        assert score == 10

    def test_unknown_type_returns_full_score(self):
        """Tipo desconhecido não deve penalizar."""
        score, issues = check_format_compliance("Qualquer conteúdo", "desconhecido")
        assert score == 10


class TestCheckHashtags:
    """Testes para verificação de hashtags."""

    def test_no_hashtags(self):
        score, issues = check_hashtags("Texto sem hashtags")
        assert score == 5

    def test_good_hashtag_count(self):
        hashtags = " ".join(f"#tag{i}" for i in range(10))
        score, issues = check_hashtags(f"Conteúdo {hashtags}")
        assert score >= 8

    def test_too_many_hashtags(self):
        hashtags = " ".join(f"#tag{i}" for i in range(35))
        content = f"Conteúdo {hashtags}"
        score, issues = check_hashtags(content)
        assert score < 10
        many_issues = [i for i in issues if "Muitas hashtags" in i]
        assert len(many_issues) > 0

    def test_generic_hashtags_penalized(self):
        content = "Conteúdo #love #instagood #beautiful"
        score, issues = check_hashtags(content)
        generic_issues = [i for i in issues if "genéricas" in i]
        assert len(generic_issues) > 0

    def test_score_range(self):
        """Score deve estar entre 0 e 10."""
        score, _ = check_hashtags("#tag1 #tag2 #tag3")
        assert 0 <= score <= 10


class TestCheckAITells:
    """Testes para detecção de vícios de IA (travessão, 'brutal', antíteses)."""

    def test_clean_text_full_score(self):
        score, issues = check_ai_tells(
            "Texto direto, sem vícios. Você vai entender o método em 5 minutos."
        )
        assert score == 10
        assert issues == []

    def test_detects_em_dash(self):
        score, issues = check_ai_tells("Marketing digital — a arte de vender online")
        assert score == 0
        assert any("Travessão" in i for i in issues)

    def test_detects_brutal(self):
        score, issues = check_ai_tells("A verdade brutal sobre crescer no Instagram")
        assert score == 0
        assert any("brutal" in i for i in issues)

    def test_brutal_inside_word_not_flagged(self):
        score, issues = check_ai_tells("A brutalidade do algoritmo é conhecida")
        assert all("brutal" not in i for i in issues)

    def test_detects_antithesis_with_period(self):
        score, issues = check_ai_tells("Não é sobre dinheiro. É sobre tempo.")
        assert score == 0
        assert any("Antítese" in i for i in issues)

    def test_detects_antithesis_with_comma(self):
        score, issues = check_ai_tells("Não é magia, é método.")
        assert score == 0

    def test_detects_antithesis_repeated_verb(self):
        score, issues = check_ai_tells(
            "Não faça mais cursos aleatórios. Faça um plano de estudo."
        )
        assert score == 0
        assert any("verbo repetido" in i for i in issues)

    def test_detects_antithesis_foi(self):
        score, issues = check_ai_tells("Não foi sorte. Foi estratégia.")
        assert score == 0

    def test_plain_negation_not_flagged(self):
        score, issues = check_ai_tells(
            "Não é fácil crescer no Instagram. Esse caminho exige consistência."
        )
        assert score == 10

    def test_negation_across_clauses_not_flagged(self):
        """Verbo repetido em frase nova não relacionada não deve disparar."""
        score, issues = check_ai_tells(
            "Você não sabe por onde começar, comece pelo básico. Sabe qual é o maior erro?"
        )
        assert score == 10

    def test_patterns_have_messages(self):
        for pattern, message in AI_TELL_PATTERNS:
            assert len(pattern) > 0
            assert len(message) > 0


class TestConstants:
    """Testes para constantes e dados."""

    def test_platform_limits_structure(self):
        for platform, limits in PLATFORM_LIMITS.items():
            assert "hook" in limits
            assert "total" in limits
            assert isinstance(limits["hook"], int)
            assert isinstance(limits["total"], int)

    def test_strong_cta_words_not_empty(self):
        assert len(STRONG_CTA_WORDS) > 0

    def test_weak_cta_words_not_empty(self):
        assert len(WEAK_CTA_WORDS) > 0

    def test_no_overlap_cta_words(self):
        """Palavras fortes e fracas não devem se sobrepor."""
        overlap = set(STRONG_CTA_WORDS) & set(WEAK_CTA_WORDS)
        assert len(overlap) == 0


class TestIntegration:
    """Testes de integração usando generate_report com arquivo real."""

    def test_generate_report_post(self, tmp_file, sample_post, capsys):
        filepath = tmp_file(sample_post)
        from quality_gate import generate_report
        score = generate_report(filepath, "post")
        assert isinstance(score, int)
        assert 0 <= score <= 100
        captured = capsys.readouterr()
        assert "QUALITY GATE" in captured.out

    def test_generate_report_article(self, tmp_file, sample_article, capsys):
        filepath = tmp_file(sample_article)
        from quality_gate import generate_report
        score = generate_report(filepath, "artigo")
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_generate_report_email(self, tmp_file, sample_email, capsys):
        filepath = tmp_file(sample_email)
        from quality_gate import generate_report
        score = generate_report(filepath, "email")
        assert isinstance(score, int)
        assert 0 <= score <= 100
