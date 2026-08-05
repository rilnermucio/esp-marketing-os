"""Contrato público da criação de avatar completo."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "commands" / "criar-avatar.md"
RESEARCH_AGENT = ROOT / "agents" / "mos-research.md"
PERSONA_TEMPLATE = ROOT / "assets" / "personas" / "persona-template.md"
SKILL = ROOT / "skills" / "marketing-os" / "SKILL.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_criar_avatar_command_exists() -> None:
    assert COMMAND.is_file(), "a interface /criar-avatar precisa existir"


def test_criar_avatar_dispatches_only_mos_research() -> None:
    content = _read(COMMAND)
    dispatched = re.findall(
        r'subagent_type:\s*["\']?(mos-[a-z-]+)["\']?', content
    )

    assert dispatched == ["mos-research"]


def test_criar_avatar_exposes_the_complete_output_contract() -> None:
    content = _read(COMMAND).lower()
    required_contract = (
        "evidência confirmada",
        "inferência",
        "hipótese",
        "avatar principal",
        "segmentos secundários",
        "anti-avatar",
        "jobs to be done",
        "nível de consciência",
        "jornada de compra",
        "linguagem real",
        "handoff context",
        "mos-copy",
        "mos-ads",
        "mos-offer",
        "mos-funnel",
        "mos-social",
    )

    for marker in required_contract:
        assert marker in content, f"contrato de avatar sem {marker!r}"


def test_avatar_contract_is_reused_by_research_and_natural_routing() -> None:
    template = _read(PERSONA_TEMPLATE).lower()
    agent = _read(RESEARCH_AGENT).lower()
    skill = _read(SKILL).lower()

    for marker in (
        "protocolo de evidências",
        "segmentação e priorização",
        "anti-avatar",
        "handoff context",
    ):
        assert marker in template, f"template canônico sem {marker!r}"

    assert "dossiê de avatar" in agent
    assert "assets/personas/persona-template.md" in agent
    assert "/criar-avatar" in skill
