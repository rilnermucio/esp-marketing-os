"""Testes para quality_gate_hook.py — regexes de HARD BLOCK, WARN e skip de paths."""

import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks"),
)

from quality_gate_hook import (
    find_hard_violations,
    find_warnings,
    should_skip,
)


class TestHardViolations:
    """HARD BLOCK: em-dash, 'brutal' e antíteses negação/afirmação."""

    def test_clean_copy_passes(self):
        content = (
            "Você quer crescer no Instagram com consistência. "
            "O método tem 3 passos práticos e funciona pra qualquer nicho."
        )
        assert find_hard_violations(content) == []

    def test_em_dash_blocks(self):
        violations = find_hard_violations("O segredo — que ninguém conta — é simples")
        assert any("Em-dash" in v for v in violations)

    def test_brutal_blocks(self):
        violations = find_hard_violations("A verdade brutal sobre vendas")
        assert any("brutal" in v for v in violations)

    def test_brutal_case_insensitive(self):
        violations = find_hard_violations("Verdade BRUTAL sobre vendas")
        assert any("brutal" in v for v in violations)

    def test_brutalidade_not_blocked(self):
        violations = find_hard_violations("A brutalidade do mercado exige preparo")
        assert all("brutal" not in v for v in violations)

    def test_antithesis_e_period_blocks(self):
        violations = find_hard_violations("Não é motivação. É arquitetura.")
        assert any("Antítese" in v for v in violations)

    def test_antithesis_e_comma_blocks(self):
        violations = find_hard_violations("Não é sobre vender mais, é sobre vender melhor")
        assert any("Antítese" in v for v in violations)

    def test_antithesis_e_newline_blocks(self):
        violations = find_hard_violations("Não é talento.\nÉ repetição.")
        assert any("Antítese" in v for v in violations)

    def test_antithesis_repeated_verb_blocks(self):
        violations = find_hard_violations("Não faça mais posts genéricos. Faça posts que vendem.")
        assert any("verbo repetido" in v for v in violations)

    def test_antithesis_foi_blocks(self):
        violations = find_hard_violations("Não foi sorte. Foi estratégia.")
        assert any("verbo repetido" in v for v in violations)

    def test_antithesis_tem_blocks(self):
        violations = find_hard_violations("Não tem segredo. Tem método.")
        assert any("verbo repetido" in v for v in violations)

    def test_plain_negation_passes(self):
        content = "Não é fácil crescer um perfil do zero. Esse processo leva meses."
        assert find_hard_violations(content) == []

    def test_unrelated_repeated_verb_across_clauses_passes(self):
        """Verbo repetido em frase nova não relacionada não pode disparar."""
        content = (
            "Você não sabe por onde começar, comece pelo básico. "
            "Sabe qual é o maior erro de quem trava?"
        )
        assert find_hard_violations(content) == []

    def test_short_antithesis_adianta_blocks(self):
        violations = find_hard_violations("Não adianta postar mais. Adianta postar melhor.")
        assert any("verbo repetido" in v for v in violations)

    def test_negation_with_long_distance_passes(self):
        content = (
            "Não adianta postar todo santo dia se o seu conteúdo continua raso "
            "demais para gerar qualquer conexão real com as pessoas. "
            "Adianta muito mais entender o que a audiência procura."
        )
        # Span entre as cláusulas passa de 60 chars: fora do shape do AI-tell
        assert find_hard_violations(content) == []


class TestWarnings:
    """WARN: clichês e variantes suaves que não bloqueiam."""

    def test_antithesis_soft_variant_warns(self):
        warnings = find_warnings("Não se trata de talento, mas de consistência.")
        assert any("Antítese suave" in w for w in warnings)

    def test_questao_de_variant_warns(self):
        warnings = find_warnings("Não é uma questão de sorte, e sim de método.")
        assert any("Antítese suave" in w for w in warnings)

    def test_clean_text_no_antithesis_warning(self):
        warnings = find_warnings("Consistência vence talento quando o talento não treina.")
        assert all("Antítese suave" not in w for w in warnings)


class TestShouldSkip:
    """Paths de tooling/docs são ignorados; conteúdo de marketing não."""

    def test_skips_commands(self):
        assert should_skip("commands/otimizar-copy.md") is True

    def test_skips_scripts(self):
        assert should_skip("scripts/quality_gate.py") is True

    def test_skips_subagents(self):
        assert should_skip("subagents/copy-agent.md") is True

    def test_does_not_skip_workspace_content(self):
        assert should_skip("workspace/outputs/post-instagram.md") is False
