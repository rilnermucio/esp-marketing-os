"""Descriptions de command servem à descoberta automática (auditoria 2026-09-28, #19).

Quando o orçamento de listagem estoura, a plataforma derruba descriptions das
skills menos usadas; as que sobram precisam dizer QUANDO usar, em PT-BR, sem
mecânica interna que envelhece (nomes de agents, "workflow #N", PARTEs de KB).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMMANDS = sorted((ROOT / "commands").glob("*.md"))
LISTING_CAP = 1536  # corte por entrada na listagem (doc oficial de skills)
INTERNAL = re.compile(r"\bmos-[a-z]|workflow #|\bPARTE\b|[Dd]ispatch", re.I)
ENGLISH = re.compile(
    r"\b(Create|Generate|Dispatches|Analyze|Turn|Publish|Capture|Design|Architect)\b"
)


def _description(path: Path) -> str:
    frontmatter = path.read_text(encoding="utf-8").split("---", 2)[1]
    match = re.search(r'^description:\s*"?(.*?)"?\s*$', frontmatter, re.M)
    assert match, f"{path.name} sem description"
    return match.group(1)


@pytest.mark.parametrize("path", COMMANDS, ids=lambda p: p.name)
def test_description_says_when_to_use(path: Path) -> None:
    desc = _description(path)
    assert re.search(r"Use (quando|para)", desc), f"{path.name}: diga quando usar"
    assert not INTERNAL.search(desc), f"{path.name}: mecânica interna na description"
    assert not ENGLISH.search(desc), f"{path.name}: description em inglês"
    assert len(desc) <= LISTING_CAP
