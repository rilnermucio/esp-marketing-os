#!/usr/bin/env python3
"""Lista fatos de plataforma vencidos em references/platform-facts.md.

Limites de formato e nomes de produto mudam sem aviso (Reels passou de 90 s
para 3 min, Advantage+ Shopping virou Advantage+ Sales). A auditoria de
2026-09-28 achou vários desatualizados porque nenhum trazia data de
verificação. Este script lê o registro e aponta as linhas com verificação mais
antiga que o limite.

Uso:
    python3 scripts/check_platform_facts.py
    python3 scripts/check_platform_facts.py --max-dias 90 --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

FACTS_FILE = Path(__file__).resolve().parent.parent / "references" / "platform-facts.md"
COMPLIANCE_FILE = (
    Path(__file__).resolve().parent.parent / "references" / "compliance-br.md"
)
# Norma de publicidade muda por resolução de conselho; a referência de
# compliance é revista a cada trimestre.
COMPLIANCE_MAX_DAYS = 90
COLUMNS = ["Plataforma", "Fato", "Valor", "Desde", "Fonte", "Verificado em"]


def parse_facts(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells == COLUMNS:
            continue
        if len(cells) != len(COLUMNS):
            rows.append({"erro": f"linha com {len(cells)} colunas: {line}"})
            continue
        rows.append(dict(zip(COLUMNS, cells)))
    return rows


def problems(
    rows: list[dict], today: date, max_days: int
) -> tuple[list[str], list[str]]:
    invalid, stale = [], []
    for row in rows:
        if "erro" in row:
            invalid.append(row["erro"])
            continue
        label = f"{row['Plataforma']}: {row['Fato']}"
        if not re.match(r"https?://", row["Fonte"]):
            invalid.append(f"{label}: fonte sem URL")
        try:
            checked = datetime.strptime(row["Verificado em"], "%Y-%m-%d").date()
        except ValueError:
            invalid.append(
                f"{label}: data de verificação inválida '{row['Verificado em']}'"
            )
            continue
        age = (today - checked).days
        if age > max_days:
            stale.append(f"{label}: verificado há {age} dias ({row['Verificado em']})")
    return invalid, stale


def compliance_age(text: str, today: date) -> int | None:
    """Idade, em dias, da verificação declarada no topo de compliance-br.md."""
    match = re.search(r"Verificado em (\d{4}-\d{2}-\d{2})", text)
    if not match:
        return None
    checked = datetime.strptime(match.group(1), "%Y-%m-%d").date()
    return (today - checked).days


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arquivo", default=str(FACTS_FILE), help="Registro de fatos")
    parser.add_argument(
        "--max-dias", type=int, default=180, help="Idade máxima da verificação"
    )
    parser.add_argument(
        "--hoje", default="", help="Data de referência YYYY-MM-DD (testes)"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Exit 1 se houver vencido ou inválido"
    )
    args = parser.parse_args(argv)

    today = (
        datetime.strptime(args.hoje, "%Y-%m-%d").date() if args.hoje else date.today()
    )
    rows = parse_facts(Path(args.arquivo).read_text(encoding="utf-8"))
    invalid, stale = problems(rows, today, args.max_dias)

    print(f"{len(rows)} fatos em {args.arquivo}")
    for item in invalid:
        print(f"INVÁLIDO: {item}")
    for item in stale:
        print(f"VENCIDO: {item}")
    if not (invalid or stale):
        print(f"Todos verificados nos últimos {args.max_dias} dias.")

    if COMPLIANCE_FILE.exists() and args.arquivo == str(FACTS_FILE):
        age = compliance_age(COMPLIANCE_FILE.read_text(encoding="utf-8"), today)
        if age is None:
            invalid.append("compliance-br.md sem data de verificação")
            print("INVÁLIDO: compliance-br.md sem data de verificação")
        elif age > COMPLIANCE_MAX_DAYS:
            stale.append("compliance-br.md")
            print(
                f"VENCIDO: references/compliance-br.md verificado há {age} dias "
                f"(revisão trimestral; limite {COMPLIANCE_MAX_DAYS})"
            )
        else:
            print(f"Compliance verificado há {age} dias.")
    return 1 if (args.strict and (invalid or stale)) else 0


if __name__ == "__main__":
    sys.exit(main())
