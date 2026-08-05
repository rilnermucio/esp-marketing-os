"""Contrato público da criação de USP baseada em evidências."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "commands" / "criar-usp.md"
BRAND_AGENT = ROOT / "agents" / "mos-brand.md"
BRAND_KNOWLEDGE = ROOT / "subagents" / "brand-agent.md"
SKILL = ROOT / "skills" / "marketing-os" / "SKILL.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_criar_usp_command_exists() -> None:
    assert COMMAND.is_file(), "a interface /criar-usp precisa existir"


def test_criar_usp_exposes_simple_and_research_first_routes() -> None:
    content = _read(COMMAND)
    dispatched = re.findall(
        r'subagent_type:\s*["\']?(mos-[a-z-]+)["\']?', content
    )

    assert "## Dispatch Simples" in content
    assert "## Dispatch Sequencial" in content
    assert set(dispatched) == {"mos-research", "mos-brand"}


def test_criar_usp_exposes_the_complete_output_contract() -> None:
    content = _read(COMMAND).lower()
    required_contract = (
        "evidência confirmada",
        "inferência",
        "hipótese",
        "categoria e contexto competitivo",
        "job to be done",
        "matriz de candidatos",
        "usp principal",
        "reason to believe",
        "mecanismo ou diferencial",
        "limites da promessa",
        "clareza",
        "relevância",
        "diferenciação",
        "credibilidade",
        "defensabilidade",
        "plano de validação",
        "handoff context",
        "mos-offer",
        "mos-copy",
        "mos-ads",
        "mos-funnel",
    )

    for marker in required_contract:
        assert marker in content, f"contrato de USP sem {marker!r}"


def test_usp_contract_is_reused_by_brand_and_natural_routing() -> None:
    knowledge = _read(BRAND_KNOWLEDGE).lower()
    agent = _read(BRAND_AGENT).lower()
    skill = _read(SKILL).lower()

    for marker in (
        "contrato canônico do dossiê de usp",
        "protocolo de evidências",
        "score de usp",
        "handoff context",
    ):
        assert marker in knowledge, f"knowledge canônico sem {marker!r}"

    assert "dossiê de usp" in agent
    assert "subagents/brand-agent.md" in agent
    assert "/criar-usp" in skill
