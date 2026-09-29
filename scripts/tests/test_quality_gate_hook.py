"""Testes para quality_gate_hook.py — regexes de HARD BLOCK, WARN e skip de paths."""

import json

import pytest
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks"),
)

from quality_gate_hook import (
    evaluate_event,
    compliance_findings,
    find_compliance_warnings,
    find_hard_violations,
    find_warnings,
    marketing_agent,
    render,
    should_skip,
)

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "scripts" / "hooks" / "quality_gate_hook.py"
PAYLOADS = Path(__file__).resolve().parent / "fixtures" / "hook_payloads"


def load_payload(name: str, **overrides) -> dict:
    """Payload real capturado do runtime (Claude Code 2.1.283), anonimizado."""
    payload = json.loads((PAYLOADS / name).read_text(encoding="utf-8"))
    payload.update(overrides)
    return payload


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
        assert any("Travessão '—'" in v for v in violations)

    def test_spaced_en_dash_as_punctuation_blocks(self):
        violations = find_hard_violations("O segredo – que ninguém conta – é simples")
        assert any("Travessão curto" in v for v in violations)

    def test_en_dash_in_range_passes(self):
        assert find_hard_violations("Reels de 15–90s e ciclos de 2024–2026.") == []

    def test_brutalmente_blocks(self):
        violations = find_hard_violations("Seja brutalmente honesto com o seu funil")
        assert any("brutal" in v for v in violations)

    def test_brutais_blocks(self):
        violations = find_hard_violations("Resultados brutais em 30 dias")
        assert any("brutal" in v for v in violations)

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
        violations = find_hard_violations(
            "Não é sobre vender mais, é sobre vender melhor"
        )
        assert any("Antítese" in v for v in violations)

    def test_antithesis_e_newline_blocks(self):
        violations = find_hard_violations("Não é talento.\nÉ repetição.")
        assert any("Antítese" in v for v in violations)

    def test_antithesis_repeated_verb_blocks(self):
        violations = find_hard_violations(
            "Não faça mais posts genéricos. Faça posts que vendem."
        )
        assert any("verbo repetido" in v for v in violations)

    def test_antithesis_foi_blocks(self):
        violations = find_hard_violations("Não foi sorte. Foi estratégia.")
        assert any("verbo repetido" in v for v in violations)

    def test_antithesis_tem_blocks(self):
        violations = find_hard_violations("Não tem segredo. Tem método.")
        assert any("verbo repetido" in v for v in violations)

    def test_antithesis_mixed_copula_blocks(self):
        """Baseline AO-001 (2026-09-28): 'Não é X. São Y.' escapava do gate."""
        violations = find_hard_violations(
            "Não é falta de equipamento caro. São cinco ajustes simples."
        )
        assert any("Antítese" in v for v in violations)

    def test_antithesis_plural_copula_blocks(self):
        violations = find_hard_violations("Não são dicas soltas. É um método.")
        assert any("Antítese" in v for v in violations)

    def test_antithesis_past_copula_blocks(self):
        violations = find_hard_violations("Não era sorte. Foi método.")
        assert any("Antítese" in v for v in violations)

    def test_sao_as_proper_noun_passes(self):
        content = (
            "Não é à toa que tantos negócios nascem aqui. "
            "São Paulo concentra metade do mercado."
        )
        assert find_hard_violations(content) == []

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
        violations = find_hard_violations(
            "Não adianta postar mais. Adianta postar melhor."
        )
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

    def test_e_sim_variant_warns(self):
        warnings = find_warnings("Não é dinheiro, e sim tempo.")
        assert any("Antítese suave" in w for w in warnings)

    def test_clean_text_no_antithesis_warning(self):
        warnings = find_warnings(
            "Consistência vence talento quando o talento não treina."
        )
        assert all("Antítese suave" not in w for w in warnings)

    def test_caps_word_warns(self):
        warnings = find_warnings("COMPRE AGORA e garanta sua vaga")
        assert any("CAPS" in w and "COMPRE" in w for w in warnings)

    def test_known_acronyms_do_not_warn(self):
        warnings = find_warnings(
            "Siga as regras da ANVISA e do CONAR. SEO e CTA também."
        )
        assert all("CAPS" not in w for w in warnings)

    def test_cfm_required_caps_do_not_warn(self):
        """A CFM 2.336/2023 exige MÉDICO e NÃO ESPECIALISTA em caixa alta."""
        warnings = find_warnings(
            "Dra. Ana Souza, CRM/SP 12345, MÉDICA com pós-graduação em nutrologia, "
            "NÃO ESPECIALISTA."
        )
        assert all("CAPS" not in w for w in warnings)

    def test_other_caps_still_warn_next_to_cfm_identification(self):
        warnings = find_warnings("Dr. Leo, CRM/RJ 999, MÉDICO. COMPRE AGORA.")
        assert any("CAPS" in w and "COMPRE" in w for w in warnings)

    def test_more_than_two_emojis_warn(self):
        warnings = find_warnings("Bora 🚀🔥💰 vender mais")
        assert any("emojis" in w for w in warnings)

    def test_two_emojis_pass(self):
        warnings = find_warnings("Bora 🚀 vender mais 🔥")
        assert all("emojis" not in w for w in warnings)


class TestCompliance:
    """Sinais de disclaimer são comparados com o texto em minúsculas."""

    def test_cvm_mention_counts_as_disclaimer(self):
        text = "Investimento em fundo regulado pela CVM."
        assert find_compliance_warnings(text) == []

    def test_financial_claim_without_disclaimer_warns(self):
        warnings = find_compliance_warnings(
            "Investimento com retorno garantido todo mês."
        )
        assert any("CVM" in w for w in warnings)


class TestComplianceRiskPhrases:
    """Frases de risco regulatório: avisam com a norma, sem aviso que resolva."""

    @pytest.mark.parametrize(
        "text, rule",
        [
            ("Resultado garantido em 30 dias.", "Promessa de resultado"),
            ("Garantimos o resultado do seu tratamento.", "Promessa de resultado"),
            ("Fature R$ 10 mil por mês com o método.", "Promessa de ganho"),
            ("Ganhe dinheiro dormindo com afiliados.", "Promessa de ganho"),
            (
                "Agende sua avaliação gratuita pelo WhatsApp.",
                "Gratuidade em serviço profissional",
            ),
            ("Veja o antes e depois da paciente.", "Antes e depois (saúde)"),
            ("Sou o melhor dentista de Curitiba.", "Título de melhor profissional"),
            (
                "Atendimento com preço social às quintas.",
                "Preço como chamariz (psicologia e advocacia)",
            ),
            (
                "Compre PETR4 agora, isso não é recomendação.",
                "Recomendação de investimento",
            ),
            ("O sérum que elimina melasma.", "Alegação terapêutica em produto"),
        ],
    )
    def test_risk_phrase_warns_with_rule(self, text, rule):
        findings = compliance_findings(text)
        assert any(f["regra"] == rule for f in findings), findings

    @pytest.mark.parametrize(
        "text",
        [
            "Garantia de 7 dias: se não gostar, devolvemos o valor.",
            "Faturamento da empresa cresceu no trimestre.",
            "Teste grátis por 14 dias, sem cartão.",
            "Os melhores cafés especiais da cidade.",
            "Entrega em todo o Brasil com preço justo.",
        ],
    )
    def test_similar_phrases_do_not_warn(self, text):
        assert compliance_findings(text) == []

    def test_finding_keeps_original_excerpt(self):
        findings = compliance_findings("Fature R$ 10 mil por mês.")
        assert findings[0]["trecho"] == "Fature R$ 1"

    def test_warning_strings_cite_rule_name(self):
        warnings = find_compliance_warnings("Resultado garantido.")
        assert any(w.startswith("[Promessa de resultado]") for w in warnings)


class TestShouldSkip:
    """Código, config e arquivos do próprio plugin são ignorados; peças do usuário não."""

    def test_skips_plugin_commands(self):
        assert should_skip(str(ROOT / "commands" / "otimizar-copy.md")) is True

    def test_skips_scripts_by_suffix(self):
        assert should_skip("/home/usuario/projeto/scripts/gerar.py") is True

    def test_skips_plugin_kbs(self):
        assert should_skip(str(ROOT / "subagents" / "copy-agent.md")) is True

    def test_gates_plugin_workspace_content(self):
        assert should_skip(str(ROOT / "workspace" / "drafts" / "post.md")) is False

    def test_gates_user_docs_folder(self):
        """Uma pasta docs/ no projeto do usuário pode conter copy (achado #16)."""
        assert should_skip("/home/usuario/projeto/docs/lancamento/emails.md") is False

    def test_gates_plain_text_scripts(self):
        assert should_skip("/home/usuario/projeto/workspace/media/roteiro.txt") is False

    def test_skips_claude_state(self):
        path = (
            "/home/usuario/projeto/.claude/agent-memory/marketing-os-mos-copy/MEMORY.md"
        )
        assert should_skip(path) is True

    def test_does_not_skip_workspace_content(self):
        assert should_skip("workspace/outputs/post-instagram.md") is False


class TestFinalResponseGate:
    """SubagentStop valida a mensagem que realmente volta ao usuário."""

    def test_blocks_marketing_agent_with_hard_violation(self):
        result = evaluate_event(
            {
                "hook_event_name": "SubagentStop",
                "agent_type": "mos-copy",
                "stop_hook_active": False,
                "last_assistant_message": "O segredo — que ninguém conta",
            }
        )

        assert result.blocked is True
        assert any("Travessão" in item for item in result.hard)

    def test_allows_clean_marketing_agent_response(self):
        result = evaluate_event(
            {
                "hook_event_name": "SubagentStop",
                "agent_type": "mos-email",
                "stop_hook_active": False,
                "last_assistant_message": "Assunto: três passos para vender com clareza.",
            }
        )

        assert result.blocked is False
        assert result.hard == []

    def test_second_failed_stop_does_not_create_infinite_loop(self):
        result = evaluate_event(
            {
                "hook_event_name": "SubagentStop",
                "agent_type": "mos-copy",
                "stop_hook_active": True,
                "last_assistant_message": "A verdade brutal sobre vendas",
            }
        )

        assert result.blocked is False
        assert result.retry_exhausted is True
        assert result.hard

    def test_ignores_non_marketing_subagent(self):
        result = evaluate_event(
            {
                "hook_event_name": "SubagentStop",
                "agent_type": "Explore",
                "stop_hook_active": False,
                "last_assistant_message": "O segredo — que ninguém conta",
            }
        )

        assert result.blocked is False
        assert result.hard == []

    def test_cli_blocks_bad_final_response(self):
        payload = {
            "hook_event_name": "SubagentStop",
            "agent_type": "mos-copy",
            "stop_hook_active": False,
            "last_assistant_message": "Não foi sorte. Foi estratégia.",
        }

        completed = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=False,
        )

        assert completed.returncode == 2
        assert "resposta final" in completed.stderr


class TestMarketingAgent:
    """O runtime qualifica agents de plugin com o nome do plugin (auditoria 2026-09-28)."""

    def test_plugin_qualified_name(self):
        assert marketing_agent("marketing-os:mos-copy") == "mos-copy"

    def test_local_install_short_name(self):
        assert marketing_agent("mos-email") == "mos-email"

    def test_other_plugin_with_similar_agent_is_ignored(self):
        assert marketing_agent("outro-plugin:mos-copy") == ""

    def test_builtin_and_foreign_agents_are_ignored(self):
        for name in (
            "Explore",
            "general-purpose",
            "marketing-os:helper",
            "",
            "cosmos-agent",
        ):
            assert marketing_agent(name) == ""


class TestRealPayloads:
    """Payloads com o formato exato que o Claude Code envia para agent de plugin."""

    def test_namespaced_final_answer_with_violation_blocks(self):
        payload = load_payload(
            "subagent_stop_plugin_agent.json",
            last_assistant_message="A verdade brutal: o segredo — que ninguém conta.",
        )
        result = evaluate_event(payload)
        assert result.skip_reason == ""
        assert result.blocked is True

    def test_namespaced_clean_final_answer_is_evaluated_and_allowed(self):
        result = evaluate_event(load_payload("subagent_stop_plugin_agent.json"))
        assert result.skip_reason == ""
        assert result.blocked is False

    def test_namespaced_agent_write_with_violation_blocks(self):
        payload = load_payload("pre_tool_use_write_plugin_agent.json")
        payload["tool_input"]["content"] = "Legenda — com travessão."
        result = evaluate_event(payload)
        assert result.blocked is True
        assert "post-teste.md" in result.context

    def test_main_session_write_is_never_gated(self):
        result = evaluate_event(load_payload("pre_tool_use_write_main_session.json"))
        assert result.blocked is False
        assert result.skip_reason == "escrita fora de agent Marketing OS"

    def test_foreign_plugin_agent_write_is_not_gated(self):
        payload = load_payload(
            "pre_tool_use_write_plugin_agent.json", agent_type="outro:mos-social"
        )
        payload["tool_input"]["content"] = "Texto — de outro plugin."
        assert evaluate_event(payload).blocked is False


class TestRender:
    """Canal de saída: bloqueio em stderr (exit 2), aviso em JSON additionalContext."""

    def test_block_goes_to_stderr_with_exit_2(self):
        payload = load_payload(
            "subagent_stop_plugin_agent.json", last_assistant_message="Isso é brutal."
        )
        code, out, err = render("SubagentStop", evaluate_event(payload))
        assert code == 2
        assert out == ""
        assert "resposta final de mos-copy" in err

    def test_warnings_use_additional_context_json(self):
        payload = load_payload("pre_tool_use_write_plugin_agent.json")
        payload["tool_input"]["content"] = "Vamos mergulhar no tema, basicamente, hoje."
        code, out, err = render("PreToolUse", evaluate_event(payload))
        assert code == 0
        assert err == ""
        data = json.loads(out)
        assert data["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
        assert "vamos mergulhar" in data["hookSpecificOutput"]["additionalContext"]

    def test_retry_exhausted_informs_user_and_parent(self):
        payload = load_payload(
            "subagent_stop_plugin_agent.json",
            stop_hook_active=True,
            last_assistant_message="Isso é brutal.",
        )
        code, out, _ = render("SubagentStop", evaluate_event(payload))
        data = json.loads(out)
        assert code == 0
        assert "systemMessage" in data
        assert "brutal" in data["hookSpecificOutput"]["additionalContext"]

    def test_clean_event_is_silent(self):
        code, out, err = render(
            "SubagentStop",
            evaluate_event(load_payload("subagent_stop_plugin_agent.json")),
        )
        assert (code, out, err) == (0, "", "")


def _hook_entries(event: str) -> list:
    config = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    return config["hooks"][event]


def test_plugin_registers_subagent_stop_gate():
    gate = next(
        entry
        for entry in _hook_entries("SubagentStop")
        if entry.get("matcher") == "mos-.*"
    )
    command = gate["hooks"][0]["command"]

    assert "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/quality_gate_hook.py" in command


def test_plugin_registers_write_gate():
    """Hooks no frontmatter de agent de plugin são ignorados; o gate de escrita vive no plugin."""
    gate = next(
        entry
        for entry in _hook_entries("PreToolUse")
        if entry.get("matcher") == "Write|Edit|MultiEdit"
    )
    command = gate["hooks"][0]["command"]

    assert '"${CLAUDE_PLUGIN_ROOT}/scripts/hooks/quality_gate_hook.py"' in command


def test_agents_do_not_declare_frontmatter_hooks():
    """Campo ignorado para agent de plugin e perigoso em instalação local (ADR-0005)."""
    offenders = []
    for path in sorted((ROOT / "agents").glob("mos-*.md")):
        frontmatter = path.read_text(encoding="utf-8").split("---", 2)[1]
        if "\nhooks:" in "\n" + frontmatter:
            offenders.append(path.name)
    assert not offenders, offenders
