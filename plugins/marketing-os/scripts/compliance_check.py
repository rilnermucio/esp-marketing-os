#!/usr/bin/env python3
"""Lista trechos de risco regulatório numa peça de marketing, com a norma.

Usa as mesmas regras do hook (COMPLIANCE_RULES em
scripts/hooks/quality_gate_hook.py): o que o gate avisa numa escrita de agent é
o que este CLI mostra para qualquer texto, inclusive o que o usuário escreveu à
mão. A referência completa, com identificações obrigatórias e fontes, fica em
references/compliance-br.md. Sinaliza risco e não substitui parecer jurídico.

Uso:
    python3 scripts/compliance_check.py --input peca.md
    python3 scripts/compliance_check.py --input - --json < peca.txt
    python3 scripts/compliance_check.py --input peca.md --strict
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def _load_hook():
    hook_path = Path(__file__).resolve().parent / "hooks" / "quality_gate_hook.py"
    spec = importlib.util.spec_from_file_location("_mos_quality_gate_hook", hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(text: str) -> list[dict]:
    """Regras disparadas, cada uma com o trecho que disparou e a norma."""
    return _load_hook().compliance_findings(text)


def render_markdown(findings: list[dict]) -> str:
    if not findings:
        return (
            "Nenhum trecho de risco detectado pelas regras automáticas.\n"
            "Isso não cobre tudo: confira identificação obrigatória e avisos da "
            "categoria em references/compliance-br.md.\n"
        )
    lines = [f"# Compliance: {len(findings)} ponto(s) de atenção", ""]
    for item in findings:
        lines.append(f"## {item['regra']}")
        lines.append(f"Trecho: \"{item['trecho']}\"")
        lines.append(item["mensagem"])
        lines.append("")
    lines.append(
        "Sinaliza risco e não substitui parecer jurídico. Referência completa: "
        "references/compliance-br.md."
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--input", required=True, help="Arquivo da peça, ou '-' para stdin"
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Termina com código 1 se houver ponto de atenção",
    )
    args = parser.parse_args(argv)

    if args.input == "-":
        text = sys.stdin.read()
    else:
        path = Path(args.input)
        if not path.is_file():
            print(f"ERRO: arquivo não encontrado: {path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")

    findings = check(text)
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(findings), end="")
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
