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
]


@pytest.fixture(scope="module")
def baseline_dir(project_root: Path) -> Path:
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
