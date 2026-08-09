"""Tier 2 smoke tests: invoke marketing-os agents via `claude -p` (uses subscription)."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.smoke


CLAUDE_BIN = shutil.which("claude")
TIMEOUT_SECONDS = 180


REPRESENTATIVE_AGENTS = [
    (
        "mos-copy",
        "Use o agente mos-copy para escrever apenas UMA headline curta para um curso online de marketing digital. Responda apenas a headline, sem explicacao.",
        ["headline", "marketing", "curso", "venda", "domine", "aprenda", "transforme"],
    ),
    (
        "mos-seo",
        "Use o agente mos-seo para sugerir 3 keywords longtail e UMA meta description para um artigo sobre 'funil de vendas para infoprodutos'. Formato: lista numerada de keywords, depois meta description em UMA linha.",
        ["keyword", "meta", "funil", "infoproduto"],
    ),
    (
        "mos-social",
        "Use o agente mos-social para escrever UM post curto de Instagram (max 5 linhas) sobre 'produtividade para criadores'. Inclua 3-5 hashtags no final.",
        ["#", "produtividade"],
    ),
    (
        "mos-email",
        "Use o agente mos-email para escrever UM email muito curto (subject + 2 paragrafos + CTA) sobre o lancamento de um workshop online de copywriting. Formato: subject em UMA linha, depois corpo, depois CTA.",
        ["subject", "workshop", "copy"],
    ),
    (
        "mos-ads",
        "Use o agente mos-ads para escrever copy de UM anuncio do Facebook para um curso de copywriting. Formato: headline em UMA linha + 1-2 paragrafos de texto principal + CTA. Responda apenas o anuncio, sem explicacao.",
        ["headline", "copy", "curso"],
    ),
    (
        "mos-ab-testing",
        "Use o agente mos-ab-testing para propor UMA hipotese de teste A/B para a headline de uma landing page de curso. Formato: hipotese em 1-2 linhas + metrica primaria.",
        ["teste", "headline", "curso", "metrica", "hipotese"],
    ),
    (
        "mos-ai-tools",
        "Use o agente mos-ai-tools para criar UM prompt de imagem (Midjourney) de um mockup de produto digital. Responda apenas o prompt.",
        ["prompt", "mockup", "produto", "midjourney"],
    ),
    (
        "mos-analytics",
        "Use o agente mos-analytics para listar 3 KPIs essenciais para um perfil de Instagram em crescimento. Lista numerada.",
        ["kpi", "instagram", "engajamento", "alcance"],
    ),
    (
        "mos-audio",
        "Use o agente mos-audio para escrever a estrutura (3 blocos) de UM episodio de podcast sobre produtividade. Formato: lista.",
        ["podcast", "produtividade", "bloco", "intro"],
    ),
    (
        "mos-brand",
        "Use o agente mos-brand para definir o arquetipo de marca e UMA frase de posicionamento para uma consultoria de marketing. Formato curto.",
        ["marca", "posicionamento", "arquetipo", "consultoria"],
    ),
    (
        "mos-community",
        "Use o agente mos-community para classificar e redigir um rascunho de resposta para UM comentario que pergunta o preco de uma mentoria. Formato: classificacao + resposta + acao recomendada.",
        ["resposta", "comentario", "classificacao", "lead"],
    ),
    (
        "mos-design",
        "Use o agente mos-design para sugerir uma paleta de 3 cores (hex) e UMA fonte para um app de financas. Formato: lista.",
        ["#", "cor", "fonte", "paleta"],
    ),
    (
        "mos-funnel",
        "Use o agente mos-funnel para descrever as 3 etapas (TOFU/MOFU/BOFU) de um funil para um curso online. Lista.",
        ["funil", "tofu", "bofu", "etapa"],
    ),
    (
        "mos-growth",
        "Use o agente mos-growth para propor UM experimento de aquisicao para um SaaS B2B. Formato: hipotese + canal + metrica.",
        ["experimento", "aquisicao", "canal", "metrica"],
    ),
    (
        "mos-infoproduct",
        "Use o agente mos-infoproduct para esbocar os 3 modulos de um curso online de copywriting. Lista numerada.",
        ["modulo", "curso", "copywriting", "aula"],
    ),
    (
        "mos-launch",
        "Use o agente mos-launch para listar as 3 fases de um lancamento (pre, carrinho, pos). Lista.",
        ["lancamento", "fase", "carrinho", "email"],
    ),
    (
        "mos-offer",
        "Use o agente mos-offer para esbocar uma oferta curta para uma mentoria de copywriting. Formato: promessa + preco + bonus + garantia.",
        ["oferta", "preco", "garantia", "bonus"],
    ),
    (
        "mos-partnerships",
        "Use o agente mos-partnerships para avaliar UM creator para uma parceria de curso online. Formato: fit score + modelo de parceria + rascunho de outreach.",
        ["creator", "parceria", "fit", "outreach"],
    ),
    (
        "mos-research",
        "Use o agente mos-research para listar 3 angulos de pesquisa de concorrencia para um nicho de financas pessoais. Lista.",
        ["pesquisa", "concorrente", "nicho", "financas"],
    ),
    (
        "mos-storytelling",
        "Use o agente mos-storytelling para escrever a estrutura (3 atos) de uma historia de marca de origem. Lista.",
        ["historia", "ato", "marca", "jornada"],
    ),
    (
        "mos-video",
        "Use o agente mos-video para escrever UM hook (3 segundos) e a estrutura de retencao de um Reels sobre produtividade. Formato curto.",
        ["hook", "reels", "produtividade", "retencao"],
    ),
]


@pytest.fixture(scope="module")
def baseline_dir(project_root: Path) -> Path:
    # NOTA: as baselines em tests/snapshots/baseline/ são artefatos INFORMATIVOS
    # pra inspeção manual (salvas só com MARKETING_OS_SAVE_BASELINE=1). NÃO são
    # golden files: a asserção é por marcadores, porque a saída do LLM não é
    # determinística e um diff exato seria flaky por natureza.
    d = project_root / "tests" / "snapshots" / "baseline"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.mark.skipif(CLAUDE_BIN is None, reason="claude CLI not in PATH")
@pytest.mark.parametrize(
    "agent_name,prompt,expected_markers",
    REPRESENTATIVE_AGENTS,
    ids=[a[0] for a in REPRESENTATIVE_AGENTS],
)
def test_agent_responds_structurally(
    agent_name: str,
    prompt: str,
    expected_markers: list[str],
    project_root: Path,
    baseline_dir: Path,
) -> None:
    """Invokes agent via claude -p, validates response is non-empty and has expected markers."""
    result = subprocess.run(
        [CLAUDE_BIN, "-p", prompt],
        capture_output=True,
        text=True,
        cwd=str(project_root),
        timeout=TIMEOUT_SECONDS,
    )
    output = result.stdout.strip()
    assert result.returncode == 0, (
        f"{agent_name} invocation failed (exit {result.returncode}):\n"
        f"STDERR:\n{result.stderr[:500]}"
    )
    assert len(output) > 50, f"{agent_name} output too short ({len(output)} chars):\n{output[:500]}"

    output_lower = output.lower()
    found = [m for m in expected_markers if m.lower() in output_lower]
    assert found, (
        f"{agent_name} output missing all expected markers {expected_markers}.\n"
        f"Output:\n{output[:1000]}"
    )

    if os.environ.get("MARKETING_OS_SAVE_BASELINE") == "1":
        baseline_path = baseline_dir / f"{agent_name}.txt"
        baseline_path.write_text(output, encoding="utf-8")
