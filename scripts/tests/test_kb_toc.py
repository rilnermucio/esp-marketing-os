"""O índice de cada KB lista todas as PARTES do arquivo.

Auditoria 2026-08-21 (itens 2 e 3) e 2026-09-28 (#15): KBs ganharam PARTES
novas sem entrada no índice (II-C e XV-B no copy-agent, XIV a XX no
infoproduct) e o seo-agent não tinha índice. O agent navega pelo índice, então
a parte que não está nele some na leitura guiada.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PART_HEADING = re.compile(r"^#{1,3}\s+PARTE\s+([IVXLC]+(?:-[A-Z0-9]+)?)\b", re.M)
KBS = [
    p
    for p in sorted((ROOT / "subagents").glob("*-agent.md"))
    if PART_HEADING.search(p.read_text(encoding="utf-8"))
]


@pytest.mark.parametrize("kb", KBS, ids=lambda p: p.name)
def test_toc_lists_every_part(kb: Path) -> None:
    text = kb.read_text(encoding="utf-8")
    first = PART_HEADING.search(text)
    toc_region = text[: first.start()]
    assert re.search(
        r"(?i)##\s+(índice|sumário)", toc_region
    ), f"{kb.name} sem índice antes da PARTE I"
    parts = list(dict.fromkeys(m.group(1) for m in PART_HEADING.finditer(text)))
    missing = [
        p for p in parts if not re.search(rf"PARTE\s+{re.escape(p)}\b", toc_region)
    ]
    assert not missing, f"{kb.name}: índice sem as PARTES {', '.join(missing)}"
