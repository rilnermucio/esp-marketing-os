"""A tabela de commands do SKILL.md é a fonte única de roteamento (auditoria 2026-09-28, #13).

O /mo mantinha um mapa próprio: citava "25 commands", deixava 21 dos 48 de
fora e mapeava gatilhos para rotas diferentes das do SKILL.md.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = (ROOT / "skills" / "marketing-os" / "SKILL.md").read_text(encoding="utf-8")
TABLE_HEADING = "## Slash commands: qual usar para cada necessidade"


def _command_table() -> str:
    start = SKILL.index(TABLE_HEADING)
    end = SKILL.find("\n## ", start + len(TABLE_HEADING))
    return SKILL[start : end if end != -1 else None]


def test_every_command_is_in_the_canonical_table():
    table = _command_table()
    listed = set(re.findall(r"`/([a-z0-9-]+)`", table))
    commands = {p.stem for p in (ROOT / "commands").glob("*.md")}
    missing = sorted(commands - listed)
    assert not missing, f"commands fora da tabela canônica do SKILL.md: {missing}"
    unknown = sorted(listed - commands)
    assert not unknown, f"a tabela cita commands inexistentes: {unknown}"


def test_mo_delegates_to_skill_instead_of_own_table():
    mo = (ROOT / "commands" / "mo.md").read_text(encoding="utf-8")
    assert TABLE_HEADING.removeprefix("## ") in mo
    assert "| Sinal no briefing |" not in mo, "o /mo voltou a ter tabela própria"


def test_skill_md_stays_under_recommended_size():
    """Doc oficial de skills: manter o SKILL.md abaixo de 500 linhas."""
    assert SKILL.count("\n") < 500
