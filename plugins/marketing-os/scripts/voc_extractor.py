#!/usr/bin/env python3
"""Extrai a voz do cliente de reviews, comentários e respostas de pesquisa.

Separa frases literais por sinal (dor, desejo, objeção, resultado) e conta as
expressões mais repetidas. É a base determinística do /minerar-voc: o agent
interpreta em cima de frases que existem de verdade no material, em vez de
parafrasear o público.

Entrada: arquivo .txt (um item por linha ou separados por linha em branco),
.csv (use --coluna) ou .json (lista de textos ou de objetos com --campo), ou
stdin com "-".

Uso:
    python3 scripts/voc_extractor.py --input reviews.csv --coluna comentario
    python3 scripts/voc_extractor.py --input respostas.txt --json
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# Marcadores por categoria, comparados sem acento e em minúsculas.
SIGNALS = {
    "dor": (
        "nao consigo",
        "nao aguento",
        "dificil",
        "problema",
        "frustr",
        "cansad",
        "odeio",
        "medo",
        "preocup",
        "demora",
        "perdi",
        "sofr",
        "trava",
    ),
    "desejo": (
        "queria",
        "gostaria",
        "sonho",
        "seria otimo",
        "meu objetivo",
        "preciso de",
        "quero ",
    ),
    "objecao": (
        "nao sei se",
        "sera que",
        "muito caro",
        "caro demais",
        "nao tenho tempo",
        "ja tentei",
        "nao funciona",
        "golpe",
        "desconfi",
        "nao confio",
    ),
    "resultado": (
        "consegui",
        "finalmente",
        "mudou",
        "recomendo",
        "funcionou",
        "resultado",
        "valeu a pena",
    ),
}
STOPWORDS = set(
    """a o as os um uma uns umas de do da dos das em no na nos nas por para pra
    com sem e ou que se mas mais muito muita ja nao sim eu voce ele ela nos eles
    elas meu minha seu sua isso isto esse essa este esta foi ser ter tem tinha
    estou esta estava ao aos como quando onde porque pois entao tambem so ate
    me te lhe lo la""".split()
)


def fold(text: str) -> str:
    """Minúsculas e sem acento, para comparar marcadores."""
    return (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    )


def load_items(raw: str, suffix: str, column: str = "", field: str = "") -> list[str]:
    if suffix == ".json":
        data = json.loads(raw)
        items = []
        for entry in data if isinstance(data, list) else []:
            if isinstance(entry, str):
                items.append(entry)
            elif (
                isinstance(entry, dict) and field and isinstance(entry.get(field), str)
            ):
                items.append(entry[field])
        return [i.strip() for i in items if i.strip()]
    if suffix == ".csv":
        reader = csv.DictReader(io.StringIO(raw))
        if not column:
            raise ValueError("CSV exige --coluna com o nome da coluna de texto")
        return [
            row[column].strip() for row in reader if (row.get(column) or "").strip()
        ]
    blocks = re.split(r"\n\s*\n", raw) if "\n\n" in raw else raw.splitlines()
    return [b.strip().replace("\n", " ") for b in blocks if b.strip()]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 8]


def classify(items: list[str], per_category: int = 8) -> dict:
    found: dict[str, Counter] = {cat: Counter() for cat in SIGNALS}
    for item in items:
        for sentence in sentences(item):
            folded = fold(sentence)
            for category, markers in SIGNALS.items():
                if any(marker in folded for marker in markers):
                    found[category][sentence] += 1
    return {
        category: [
            {"frase": s, "vezes": n} for s, n in counter.most_common(per_category)
        ]
        for category, counter in found.items()
    }


def top_expressions(items: list[str], size: int = 2, top: int = 15) -> list[dict]:
    counter: Counter = Counter()
    for item in items:
        words = [w for w in re.findall(r"[a-z0-9]+", fold(item)) if w not in STOPWORDS]
        for i in range(len(words) - size + 1):
            counter[" ".join(words[i : i + size])] += 1
    return [{"expressao": e, "vezes": n} for e, n in counter.most_common(top) if n > 1]


def analyze(items: list[str]) -> dict:
    return {
        "itens": len(items),
        "sinais": classify(items),
        "expressoes": top_expressions(items),
    }


def render_markdown(result: dict) -> str:
    lines = [f"# Voz do cliente: {result['itens']} itens analisados", ""]
    titles = {
        "dor": "Dores",
        "desejo": "Desejos",
        "objecao": "Objeções",
        "resultado": "Resultados e elogios",
    }
    for category, title in titles.items():
        lines.append(f"## {title}")
        rows = result["sinais"][category]
        lines += [f"- ({r['vezes']}x) {r['frase']}" for r in rows] or [
            "- (nenhuma frase com esse sinal)"
        ]
        lines.append("")
    lines.append("## Expressões que se repetem")
    lines += [f"- {e['expressao']} ({e['vezes']}x)" for e in result["expressoes"]] or [
        "- (nenhuma)"
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--input", required=True, help="Arquivo .txt, .csv ou .json, ou '-' para stdin"
    )
    parser.add_argument("--coluna", default="", help="Coluna de texto (CSV)")
    parser.add_argument("--campo", default="", help="Campo de texto (JSON com objetos)")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args(argv)

    if args.input == "-":
        raw, suffix = sys.stdin.read(), ".txt"
    else:
        path = Path(args.input)
        raw, suffix = path.read_text(encoding="utf-8"), path.suffix.lower()
    try:
        items = load_items(raw, suffix, args.coluna, args.campo)
    except (ValueError, KeyError) as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 1
    result = analyze(items)
    print(
        json.dumps(result, ensure_ascii=False, indent=2)
        if args.json
        else render_markdown(result)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
