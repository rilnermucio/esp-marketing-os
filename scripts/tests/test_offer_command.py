"""Contrato público da arquitetura de ofertas baseada em evidências."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "commands" / "criar-oferta.md"
OFFER_AGENT = ROOT / "agents" / "mos-offer.md"
OFFER_KNOWLEDGE = ROOT / "subagents" / "offer-agent.md"
LEGACY_SOURCE_SKILL = (
    ROOT / ".agents" / "skills" / "source-command-marketing-os" / "SKILL.md"
)
CANONICAL_SKILL = ROOT / "skills" / "marketing-os" / "SKILL.md"
META_ROUTER = ROOT / "commands" / "mo.md"
ROUTING_CASES = ROOT / "docs" / "ai-engineering" / "evals" / "routing-cases.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _routing_case(case_id: str) -> dict:
    cases = json.loads(_read(ROUTING_CASES))["cases"]
    return next(case for case in cases if case["id"] == case_id)


def test_high_ticket_without_research_routes_research_before_offer() -> None:
    command = _read(COMMAND).lower()
    case = _routing_case("RT-017")

    assert "oferta core/high-ticket sem research" in command
    assert case["expected_agents"] == ["mos-research", "mos-offer"]
    assert case["dispatch"] == "sequencial"


def test_offer_consumes_an_approved_usp_handoff_without_rederiving_it() -> None:
    command = _read(COMMAND).lower()
    agent = _read(OFFER_AGENT).lower()
    knowledge = _read(OFFER_KNOWLEDGE).lower()

    for marker in (
        "dossiê de usp",
        "usp_version",
        "primary_usp",
        "reason_to_believe",
        "mechanism_or_differentiator",
        "evidence_ids",
        "claim_limits",
        "open_hypotheses",
    ):
        assert marker in command, f"/criar-oferta não preserva {marker!r}"

    assert "handoff de usp" in agent
    assert "entrada do dossiê de usp" in knowledge
    assert "redefinição silenciosa" in knowledge


def test_offer_exposes_evidence_claim_limits_and_validation_contract() -> None:
    command = _read(COMMAND).lower()
    agent = _read(OFFER_AGENT).lower()
    knowledge = _read(OFFER_KNOWLEDGE).lower()
    case = _routing_case("RT-017")

    for marker in (
        "protocolo de evidências",
        "evidência confirmada",
        "inferência",
        "hipótese",
        "fonte e data",
        "claims aprovados",
        "claims bloqueados",
        "plano de validação",
    ):
        assert marker in command, f"output de oferta sem {marker!r}"
        assert marker in agent, f"mos-offer sem {marker!r}"

    assert "protocolo de evidências da oferta" in knowledge
    assert "oe01" in knowledge
    assert "redefinição silenciosa" in knowledge
    assert "ledger de evidências, claims e hipóteses" in case["min_output_fields"]


def test_migrated_source_skill_delegates_to_the_canonical_orchestrator() -> None:
    skill = _read(LEGACY_SOURCE_SKILL).lower()

    assert "skills/marketing-os/skill.md" in skill
    assert "fonte canônica" in skill
    assert "/criar-oferta" in skill
    assert "/criar-avatar" in skill
    assert "/criar-usp" in skill
    assert "18 subagentes" not in skill
    assert "## arquitetura de subagentes" not in skill


def test_natural_offer_routing_matches_the_command_dependencies() -> None:
    skill = _read(CANONICAL_SKILL).lower()

    assert "### rota condicional: oferta" in skill
    assert "oferta core ou high-ticket sem research" in skill
    assert re.search(r"`mos-research`\s+seguido de `mos-offer`", skill)
    assert "dossiê de usp" in skill
    assert "preserv" in skill


def test_meta_router_exposes_the_offer_command() -> None:
    """O /mo roteia pela tabela canônica do SKILL.md (auditoria 2026-09-28, #13)."""
    router = _read(META_ROUTER).lower()
    skill = _read(CANONICAL_SKILL).lower()

    assert "slash commands: qual usar para cada necessidade" in router
    assert "| oferta (value stack, preço, garantia) | `/criar-oferta` |" in skill
    assert re.search(r"`mos-research`\s+seguido de `mos-offer`", skill)
