#!/usr/bin/env python3
"""Eval de output do mos-copy: camada determinística + prompt do julgador par-a-par.

Duas responsabilidades, zero chamadas de rede (stdlib puro):

  score  — roda a camada determinística (quality_gate.collect_checks) num output
           gerado e emite scorecard JSON.
  pair   — monta o prompt do julgador par-a-par (protocolo de
           docs/ai-engineering/evals/quality-anchors.md: comparação por critério,
           sem nota absoluta). O chamador roda o prompt 2x (ordem normal e
           --inverter) num modelo juiz e consolida: vitória só quando consistente.

Casos e baseline: docs/ai-engineering/evals/copy-output-cases.json e
copy-output-baseline.md.

Uso:
  python3 scripts/copy_output_eval.py score output.md --formato post
  python3 scripts/copy_output_eval.py pair --candidato novo.md --referencia baseline.md --formato post
  python3 scripts/copy_output_eval.py pair ... --inverter   # segunda rodada
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from quality_gate import collect_checks  # noqa: E402

# formato do caso -> content_type do quality_gate
FORMATO_PARA_TIPO = {
    "headline": "landing-page",
    "post": "post",
    "email": "email",
    "ad": "anuncio",
    "sales": "landing-page",
}

# Critérios do julgador: R4 (RUBRICS.md) condensada em comparação por critério.
CRITERIOS_JUIZ = [
    (
        "hook",
        "Hook/primeira linha: qual segura a atenção do público declarado no briefing?",
    ),
    (
        "especificidade",
        "Especificidade da promessa: qual tem mecanismo e concretude em vez de adjetivo vago?",
    ),
    (
        "prova",
        "Prova/credibilidade: qual sustenta o claim com número, caso ou contexto verificável?",
    ),
    ("cta", "CTA: qual pede UMA ação clara e adequada ao objetivo do briefing?"),
    (
        "naturalidade",
        "Naturalidade PT-BR: qual soa humano (zero vício de IA: travessão, antítese negação-afirmação, clichê, superlativo vazio)?",
    ),
    (
        "fit",
        "Fit com o briefing: qual respeita melhor o nível de consciência, o público e o tom pedidos?",
    ),
]


def cmd_score(args: argparse.Namespace) -> int:
    content = Path(args.arquivo).read_text(encoding="utf-8")
    tipo = FORMATO_PARA_TIPO[args.formato]
    checks, hook_text, score, capped = collect_checks(content, tipo)
    resultado = {
        "arquivo": args.arquivo,
        "formato": args.formato,
        "quality_gate_type": tipo,
        "score": score,
        "capped_by_ai_tells": capped,
        "palavras": len(content.split()),
        "checks": {
            nome: {"score": s, "max": m, "issues": issues}
            for nome, (s, issues, m) in checks.items()
        },
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


def cmd_pair(args: argparse.Namespace) -> int:
    candidato = Path(args.candidato).read_text(encoding="utf-8").strip()
    referencia = Path(args.referencia).read_text(encoding="utf-8").strip()

    # Ordem alternada: na segunda rodada os textos trocam de rótulo. A vitória
    # só conta quando o MESMO texto vence nas duas rodadas (viés de posição).
    texto_a, texto_b = (
        (referencia, candidato) if args.inverter else (candidato, referencia)
    )

    criterios = "\n".join(f"- {cid}: {desc}" for cid, desc in CRITERIOS_JUIZ)
    briefing_bloco = ""
    if args.briefing:
        briefing_bloco = (
            "\nBRIEFING QUE GEROU AS PEÇAS (contexto do critério 'fit'):\n"
            f"{Path(args.briefing).read_text(encoding='utf-8').strip()}\n"
        )

    prompt = f"""Você é julgador de qualidade de copy PT-BR. Compare as duas peças abaixo critério a critério.

REGRAS (protocolo quality-anchors.md do Marketing OS):
1. Compare A vs B em CADA critério; declare o vencedor do critério (A, B ou empate) com UMA frase de motivo.
2. NUNCA dê nota numérica; só comparação.
3. Empate é resposta legítima quando não há diferença clara.
4. Julgue pelo texto, não pelo tamanho: mais longo não é melhor.

CRITÉRIOS:
{criterios}
{briefing_bloco}
PEÇA A:
<<<A
{texto_a}
A>>>

PEÇA B:
<<<B
{texto_b}
B>>>

RESPONDA APENAS com JSON válido neste formato, sem texto fora do JSON:
{{"veredictos": [{{"criterio": "hook", "vencedor": "A|B|empate", "motivo": "..."}}, ...um por critério na ordem dada...], "vencedor_geral": "A|B|empate"}}"""

    print(prompt)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Eval de output do mos-copy")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_score = sub.add_parser(
        "score", help="Camada determinística (quality_gate) em JSON"
    )
    p_score.add_argument("arquivo", help="Arquivo com o output gerado")
    p_score.add_argument(
        "--formato",
        required=True,
        choices=sorted(FORMATO_PARA_TIPO),
        help="Formato do caso",
    )
    p_score.set_defaults(func=cmd_score)

    p_pair = sub.add_parser("pair", help="Imprime o prompt do julgador par-a-par")
    p_pair.add_argument(
        "--candidato", required=True, help="Peça candidata (A na ordem normal)"
    )
    p_pair.add_argument(
        "--referencia", required=True, help="Peça de referência (B na ordem normal)"
    )
    p_pair.add_argument(
        "--briefing", help="Arquivo com o briefing do caso (recomendado)"
    )
    p_pair.add_argument(
        "--inverter", action="store_true", help="Segunda rodada: troca os rótulos A/B"
    )
    p_pair.set_defaults(func=cmd_pair)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
