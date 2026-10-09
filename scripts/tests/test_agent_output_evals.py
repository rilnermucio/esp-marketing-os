"""Guarda estrutural do eval de output de mos-social, mos-email e mos-ads.

O golden set (agent-output-cases.json) fixa briefs com todos os campos do
PRE-FLIGHT de cada agent, e cada caso tem o output de referência versionado em
baselines/<perfil>/. O julgamento par a par roda fora da suíte (custa modelo);
aqui a suíte garante que os briefs não param no pre-flight, que o perfil de
critérios existe e que a baseline está versionada.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
EVALS = REPO_ROOT / "docs" / "ai-engineering" / "evals"
CASES_PATH = EVALS / "agent-output-cases.json"
PROFILES_PATH = REPO_ROOT / "scripts" / "evals" / "output-profiles.json"

pytestmark = pytest.mark.skipif(
    not CASES_PATH.exists(),
    reason="docs/ai-engineering ausente (contexto de pacote Codex)",
)

# Campos do PRE-FLIGHT de cada agent (agents/mos-*.md). Se o pre-flight mudar,
# mude aqui: brief sem o campo faz o agent parar em perguntas e a baseline
# deixa de medir a peça.
PREFLIGHT = {
    "mos-social": ("Plataforma:", "Formato:", "Objetivo:", "Tema:", "Pilar:", "CTA:"),
    "mos-email": ("Produto:", "Lista:", "Público:", "Objetivo:", "Tom:", "Entregue:"),
    "mos-ads": (
        "Oferta:",
        "Orçamento:",
        "Plataforma:",
        "Objetivo:",
        "Público:",
        "consciência:",
        "Criativo:",
        "Conta:",
    ),
}
MIN_CASES_PER_AGENT = 3


def _cases() -> list[dict]:
    if not CASES_PATH.exists():
        return []
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]


def _profiles() -> dict:
    return json.loads(PROFILES_PATH.read_text(encoding="utf-8"))["profiles"]


def test_ids_unicos_no_padrao():
    ids = [case["id"] for case in _cases()]
    assert len(ids) == len(set(ids)), "IDs duplicados no golden set"
    for case_id in ids:
        assert re.fullmatch(r"AO-\d{3}", case_id), f"ID fora do padrão AO-NNN: {case_id}"


def test_cada_agent_tem_casos_suficientes():
    profiles = _profiles()
    por_agent = Counter(profiles[case["profile"]]["agent"] for case in _cases())
    for agent in PREFLIGHT:
        assert por_agent[agent] >= MIN_CASES_PER_AGENT, (
            f"{agent}: {por_agent[agent]} casos; o mínimo é {MIN_CASES_PER_AGENT}"
        )


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["id"])
def test_perfil_existe_e_aponta_para_agent_coberto(case):
    profiles = _profiles()
    assert case["profile"] in profiles, f"{case['id']}: perfil inexistente"
    assert profiles[case["profile"]]["agent"] in PREFLIGHT
    assert case["peca"].strip()


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["id"])
def test_briefing_preenche_o_preflight(case):
    agent = _profiles()[case["profile"]]["agent"]
    briefing = case["briefing"]
    assert len(briefing) > 400, f"{case['id']}: briefing curto demais"
    faltando = [campo for campo in PREFLIGHT[agent] if campo not in briefing]
    assert not faltando, f"{case['id']}: briefing sem {faltando} ({agent})"
    assert "—" not in briefing, f"{case['id']}: travessão no briefing"


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["id"])
def test_baseline_versionada(case):
    baseline = EVALS / "baselines" / case["profile"] / f"{case['id']}.md"
    assert baseline.exists(), f"{case['id']}: baseline ausente em {baseline}"
    assert (
        len(baseline.read_text(encoding="utf-8").strip()) > 300
    ), f"{case['id']}: baseline vazia ou truncada"
