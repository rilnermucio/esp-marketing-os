"""Valida o golden set de roteamento (docs/ai-engineering/evals/routing-cases.json).

Camada determinística dos routing evals: garante que o golden set está
bem-formado, aponta para commands/agents que existem no repo e referencia
IDs definidos na taxonomia de falhas. Renomear um command, agent ou ID de
falha sem atualizar o gabarito quebra aqui.

O acerto de roteamento em sessão real é medido pela camada viva (manual),
descrita em docs/ai-engineering/ROUTING-EVALS.md.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CASES_PATH = PROJECT_ROOT / "docs" / "ai-engineering" / "evals" / "routing-cases.json"
TAXONOMY_PATH = PROJECT_ROOT / "docs" / "ai-engineering" / "FAILURE-TAXONOMY.md"
COMMANDS_DIR = PROJECT_ROOT / "commands"
AGENTS_DIR = PROJECT_ROOT / "agents"

CASE_ID_RE = re.compile(r"^RT-\d{3}$")
FAILURE_ID_RE = re.compile(r"^F-[A-Z]+-\d{2}$")
VALID_DISPATCH = {"simples", "paralelo", "sequencial", "nenhum"}
REQUIRED_FIELDS = (
    "id",
    "prompt",
    "expected_command",
    "expected_agents",
    "dispatch",
    "min_output_fields",
    "detects",
)

# No pacote Codex distribuído docs/ai-engineering nao e copiada (build_codex_plugin
# COPY_DIRS); pular ali evita erro de coleta. No repo, a ausencia do JSON com o
# diretorio presente continua quebrando alto (guard segue estrito).
if not (PROJECT_ROOT / "docs" / "ai-engineering").exists():
    pytest.skip(
        "golden set não distribuído no pacote (docs/ai-engineering ausente)",
        allow_module_level=True,
    )

CASES: list[dict] = json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]
TAXONOMY_TEXT = TAXONOMY_PATH.read_text(encoding="utf-8")
CASE_IDS = [c.get("id", f"case-{i}") for i, c in enumerate(CASES)]


class TestGoldenSetStructure:
    """O arquivo de casos é bem-formado e auto-consistente."""

    def test_has_minimum_coverage(self) -> None:
        assert len(CASES) >= 10, "Golden set encolheu abaixo da cobertura mínima"

    def test_ids_unique_and_well_formed(self) -> None:
        ids = [c["id"] for c in CASES]
        assert len(ids) == len(set(ids)), f"IDs duplicados: {ids}"
        malformed = [i for i in ids if not CASE_ID_RE.match(i)]
        assert not malformed, f"IDs fora do padrão RT-NNN: {malformed}"

    @pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
    def test_required_fields_present(self, case: dict) -> None:
        missing = [f for f in REQUIRED_FIELDS if f not in case]
        assert not missing, f"{case.get('id')}: campos ausentes {missing}"
        assert case["prompt"].strip(), f"{case['id']}: prompt vazio"
        assert case["min_output_fields"], f"{case['id']}: min_output_fields vazio"
        assert case["detects"], f"{case['id']}: detects vazio"


class TestGoldenSetConsistency:
    """O gabarito aponta para artefatos que existem no repo."""

    @pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
    def test_expected_command_exists(self, case: dict) -> None:
        cmd = case["expected_command"]
        if cmd is None:
            return
        path = COMMANDS_DIR / f"{cmd}.md"
        assert path.exists(), (
            f"{case['id']}: command '{cmd}' não existe em commands/ "
            "(renomeou? atualize o golden set)"
        )

    @pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
    def test_expected_agents_exist(self, case: dict) -> None:
        for agent in case["expected_agents"]:
            path = AGENTS_DIR / f"{agent}.md"
            assert path.exists(), f"{case['id']}: agent '{agent}' não existe em agents/"

    @pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
    def test_dispatch_coherent_with_agents(self, case: dict) -> None:
        dispatch = case["dispatch"]
        agents = case["expected_agents"]
        assert (
            dispatch in VALID_DISPATCH
        ), f"{case['id']}: dispatch '{dispatch}' inválido"
        if dispatch == "nenhum":
            assert (
                agents == []
            ), f"{case['id']}: dispatch 'nenhum' exige lista de agents vazia"
        elif dispatch == "simples":
            assert (
                len(agents) == 1
            ), f"{case['id']}: dispatch 'simples' exige exatamente 1 agent"
        else:
            assert (
                len(agents) >= 2
            ), f"{case['id']}: dispatch '{dispatch}' exige 2+ agents"

    @pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
    def test_detects_ids_defined_in_taxonomy(self, case: dict) -> None:
        for fid in case["detects"]:
            assert FAILURE_ID_RE.match(
                fid
            ), f"{case['id']}: ID '{fid}' fora do padrão F-CATEGORIA-NN"
            assert fid in TAXONOMY_TEXT, (
                f"{case['id']}: '{fid}' não está definido em FAILURE-TAXONOMY.md "
                "(falha nova entra primeiro na taxonomia)"
            )
