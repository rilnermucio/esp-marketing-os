#!/usr/bin/env python3
"""Eval reutilizável de outputs de marketing.

O nome do arquivo foi preservado para compatibilidade com os comandos e
worklogs existentes. A interface cobre quatro operações:

  score        aplica a camada determinística do quality gate.
  pair         monta uma comparação par a par com critérios do domínio.
  consolidate  cruza as duas ordens do julgamento e remove viés de posição.
  profiles     lista os perfis disponíveis.

Uso:
  python3 scripts/copy_output_eval.py score output.md --formato post
  python3 scripts/copy_output_eval.py score output.md --profile video
  python3 scripts/copy_output_eval.py pair --candidato novo.md --referencia baseline.md --profile seo
  python3 scripts/copy_output_eval.py pair --candidato novo.md --referencia baseline.md --profile seo --inverter
  python3 scripts/copy_output_eval.py consolidate --normal normal.json --invertida invertida.json --profile seo
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PROFILES_PATH = SCRIPT_DIR / "evals" / "output-profiles.json"

sys.path.insert(0, str(SCRIPT_DIR))

from quality_gate import collect_checks  # noqa: E402

FORMATO_PARA_PROFILE = {
    "headline": "copy-headline",
    "post": "copy-post",
    "email": "email",
    "ad": "ads",
    "sales": "copy-sales",
}

# Compatibilidade para consumidores que consultavam esse mapa diretamente.
FORMATO_PARA_TIPO = {
    "headline": "landing-page",
    "post": "post",
    "email": "email",
    "ad": "anuncio",
    "sales": "landing-page",
}


@dataclass(frozen=True)
class Criterion:
    """Critério individual usado pelo julgador par a par."""

    id: str
    description: str


@dataclass(frozen=True)
class EvalProfile:
    """Contrato de avaliação de um domínio do Marketing OS."""

    id: str
    agent: str
    quality_gate_type: str
    criteria: tuple[Criterion, ...]


def load_profiles(path: Path | None = None) -> dict[str, EvalProfile]:
    """Carrega e valida os perfis de avaliação versionados."""

    profiles_path = path or DEFAULT_PROFILES_PATH
    payload = json.loads(profiles_path.read_text(encoding="utf-8"))
    if payload.get("version") != 1:
        raise ValueError("output-profiles.json precisa usar version 1")

    criteria_sets = payload.get("criteria_sets")
    raw_profiles = payload.get("profiles")
    if not isinstance(criteria_sets, dict) or not isinstance(raw_profiles, dict):
        raise ValueError(
            "output-profiles.json precisa definir criteria_sets e profiles"
        )

    profiles: dict[str, EvalProfile] = {}
    for profile_id, raw_profile in raw_profiles.items():
        if not isinstance(raw_profile, dict):
            raise ValueError(f"Perfil inválido: {profile_id}")

        criteria_set_id = raw_profile.get("criteria_set")
        raw_criteria = criteria_sets.get(criteria_set_id)
        if not isinstance(raw_criteria, list) or not raw_criteria:
            raise ValueError(
                f"Perfil {profile_id} referencia criteria_set inválido: "
                f"{criteria_set_id}"
            )

        criteria: list[Criterion] = []
        seen_ids: set[str] = set()
        for raw_criterion in raw_criteria:
            if not isinstance(raw_criterion, dict):
                raise ValueError(f"Critério inválido no perfil {profile_id}")
            criterion_id = raw_criterion.get("id")
            description = raw_criterion.get("description")
            if not isinstance(criterion_id, str) or not criterion_id.strip():
                raise ValueError(f"Critério sem id no perfil {profile_id}")
            if not isinstance(description, str) or not description.strip():
                raise ValueError(
                    f"Critério {criterion_id} sem descrição no perfil {profile_id}"
                )
            if criterion_id in seen_ids:
                raise ValueError(
                    f"Critério duplicado no perfil {profile_id}: {criterion_id}"
                )
            seen_ids.add(criterion_id)
            criteria.append(Criterion(criterion_id, description))

        agent = raw_profile.get("agent")
        quality_gate_type = raw_profile.get("quality_gate_type")
        if not isinstance(agent, str) or not agent.startswith("mos-"):
            raise ValueError(f"Agent inválido no perfil {profile_id}: {agent}")
        if not isinstance(quality_gate_type, str) or not quality_gate_type:
            raise ValueError(f"quality_gate_type inválido no perfil {profile_id}")

        profiles[profile_id] = EvalProfile(
            id=profile_id,
            agent=agent,
            quality_gate_type=quality_gate_type,
            criteria=tuple(criteria),
        )

    return profiles


def resolve_profile(
    profile_id: str | None = None,
    *,
    formato: str | None = None,
    profiles_path: Path | None = None,
) -> EvalProfile:
    """Resolve um perfil explícito ou um formato legado."""

    if profile_id and formato:
        raise ValueError("Informe profile_id ou formato, nunca os dois")
    if formato:
        try:
            profile_id = FORMATO_PARA_PROFILE[formato]
        except KeyError as exc:
            raise ValueError(f"Formato desconhecido: {formato}") from exc
    if not profile_id:
        raise ValueError("Informe profile_id ou formato")

    profiles = load_profiles(profiles_path)
    try:
        return profiles[profile_id]
    except KeyError as exc:
        raise ValueError(f"Perfil desconhecido: {profile_id}") from exc


def score_text(content: str, profile: EvalProfile) -> dict[str, Any]:
    """Aplica o quality gate e retorna um scorecard independente de arquivo."""

    checks, _hook_text, score, capped = collect_checks(
        content, profile.quality_gate_type
    )
    return {
        "profile": profile.id,
        "agent": profile.agent,
        "quality_gate_type": profile.quality_gate_type,
        "score": score,
        "capped_by_ai_tells": capped,
        "palavras": len(content.split()),
        "checks": {
            name: {"score": value, "max": maximum, "issues": issues}
            for name, (value, issues, maximum) in checks.items()
        },
    }


def build_pair_prompt(
    candidate: str,
    reference: str,
    *,
    profile: EvalProfile,
    briefing: str = "",
    invert: bool = False,
) -> str:
    """Monta uma rodada do julgamento par a par para o perfil informado."""

    text_a, text_b = (reference, candidate) if invert else (candidate, reference)
    criteria = "\n".join(
        f"- {criterion.id}: {criterion.description}" for criterion in profile.criteria
    )
    briefing_block = ""
    if briefing.strip():
        briefing_block = (
            "\nBRIEFING QUE GEROU AS PEÇAS (contexto do critério de fit):\n"
            f"{briefing.strip()}\n"
        )

    return f"""Você é julgador de qualidade de outputs de marketing PT-BR para o agente {profile.agent}. Compare as duas peças abaixo critério a critério.

REGRAS (protocolo quality-anchors.md do Marketing OS):
1. Compare A vs B em CADA critério; declare o vencedor do critério (A, B ou empate) com UMA frase de motivo.
2. NUNCA dê nota numérica; use somente comparação.
3. Empate é resposta legítima quando não há diferença clara.
4. Julgue pelo texto e pelo briefing. Tamanho isolado não indica qualidade.

PERFIL: {profile.id}
CRITÉRIOS:
{criteria}
{briefing_block}
PEÇA A:
<<<A
{text_a.strip()}
A>>>

PEÇA B:
<<<B
{text_b.strip()}
B>>>

RESPONDA APENAS com JSON válido neste formato, sem texto fora do JSON:
{{"veredictos": [{{"criterio": "{profile.criteria[0].id}", "vencedor": "A|B|empate", "motivo": "..."}}, ...um por critério na ordem dada...], "vencedor_geral": "A|B|empate"}}"""


def _verdicts_by_criterion(
    payload: dict[str, Any], profile: EvalProfile, round_name: str
) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError(f"Rodada {round_name} precisa ser um objeto JSON")
    raw_verdicts = payload.get("veredictos")
    if not isinstance(raw_verdicts, list):
        raise ValueError(f"Rodada {round_name} sem lista de veredictos")

    verdicts: dict[str, str] = {}
    for raw_verdict in raw_verdicts:
        if not isinstance(raw_verdict, dict):
            raise ValueError(f"Veredicto inválido na rodada {round_name}")
        criterion = raw_verdict.get("criterio")
        winner = raw_verdict.get("vencedor")
        reason = raw_verdict.get("motivo")
        if not isinstance(criterion, str) or winner not in {"A", "B", "empate"}:
            raise ValueError(f"Veredicto inválido na rodada {round_name}")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(
                f"Veredicto sem motivo na rodada {round_name}: {criterion}"
            )
        if criterion in verdicts:
            raise ValueError(f"Critério duplicado na rodada {round_name}: {criterion}")
        verdicts[criterion] = winner

    expected = {criterion.id for criterion in profile.criteria}
    if set(verdicts) != expected:
        missing = sorted(expected - set(verdicts))
        extra = sorted(set(verdicts) - expected)
        raise ValueError(
            f"Critérios divergentes na rodada {round_name}; "
            f"faltando={missing}, extras={extra}"
        )
    return verdicts


def _physical_winner(label: str, *, inverted: bool) -> str:
    if label == "empate":
        return "empate"
    if inverted:
        return "referencia" if label == "A" else "candidato"
    return "candidato" if label == "A" else "referencia"


def _consolidated_winner(normal: str, inverted: str) -> str:
    return normal if normal == inverted else "inconclusivo"


def consolidate_pair(
    normal: dict[str, Any],
    inverted: dict[str, Any],
    *,
    profile: EvalProfile,
) -> dict[str, Any]:
    """Consolida duas ordens e só declara vitória quando elas concordam."""

    normal_verdicts = _verdicts_by_criterion(normal, profile, "normal")
    inverted_verdicts = _verdicts_by_criterion(inverted, profile, "invertida")

    verdicts = []
    for criterion in profile.criteria:
        normal_winner = _physical_winner(normal_verdicts[criterion.id], inverted=False)
        inverted_winner = _physical_winner(
            inverted_verdicts[criterion.id], inverted=True
        )
        verdicts.append(
            {
                "criterio": criterion.id,
                "rodada_normal": normal_winner,
                "rodada_invertida": inverted_winner,
                "vencedor": _consolidated_winner(normal_winner, inverted_winner),
            }
        )

    normal_overall = normal.get("vencedor_geral")
    inverted_overall = inverted.get("vencedor_geral")
    if normal_overall not in {"A", "B", "empate"}:
        raise ValueError("vencedor_geral inválido na rodada normal")
    if inverted_overall not in {"A", "B", "empate"}:
        raise ValueError("vencedor_geral inválido na rodada invertida")

    normal_physical = _physical_winner(normal_overall, inverted=False)
    inverted_physical = _physical_winner(inverted_overall, inverted=True)
    overall = _consolidated_winner(normal_physical, inverted_physical)
    consistent = overall != "inconclusivo" and all(
        verdict["vencedor"] != "inconclusivo" for verdict in verdicts
    )

    return {
        "profile": profile.id,
        "agent": profile.agent,
        "veredictos": verdicts,
        "rodadas": {
            "normal": normal_physical,
            "invertida": inverted_physical,
        },
        "vencedor_geral": overall,
        "consistente": consistent,
    }


def _profile_from_args(
    args: argparse.Namespace, *, default: str | None = None
) -> EvalProfile:
    profile_id = getattr(args, "profile", None)
    formato = getattr(args, "formato", None)
    if not profile_id and not formato:
        profile_id = default
    return resolve_profile(profile_id=profile_id, formato=formato)


def cmd_score(args: argparse.Namespace) -> int:
    profile = _profile_from_args(args)
    content = Path(args.arquivo).read_text(encoding="utf-8")
    result = {"arquivo": args.arquivo, **score_text(content, profile)}
    if args.formato:
        result["formato"] = args.formato
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_pair(args: argparse.Namespace) -> int:
    profile = _profile_from_args(args, default="copy-post")
    candidate = Path(args.candidato).read_text(encoding="utf-8")
    reference = Path(args.referencia).read_text(encoding="utf-8")
    briefing = ""
    if args.briefing:
        briefing = Path(args.briefing).read_text(encoding="utf-8")

    print(
        build_pair_prompt(
            candidate,
            reference,
            profile=profile,
            briefing=briefing,
            invert=args.inverter,
        )
    )
    return 0


def cmd_consolidate(args: argparse.Namespace) -> int:
    profile = _profile_from_args(args, default="copy-post")
    normal = json.loads(Path(args.normal).read_text(encoding="utf-8"))
    inverted = json.loads(Path(args.invertida).read_text(encoding="utf-8"))
    result = consolidate_pair(normal, inverted, profile=profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_profiles(_args: argparse.Namespace) -> int:
    profiles = load_profiles()
    result = {
        profile_id: {
            "agent": profile.agent,
            "quality_gate_type": profile.quality_gate_type,
            "criteria": [criterion.id for criterion in profile.criteria],
        }
        for profile_id, profile in sorted(profiles.items())
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _add_profile_selector(parser: argparse.ArgumentParser, *, required: bool) -> None:
    selector = parser.add_mutually_exclusive_group(required=required)
    selector.add_argument(
        "--profile",
        choices=sorted(load_profiles()),
        help="Perfil de avaliação por domínio",
    )
    selector.add_argument(
        "--formato",
        choices=sorted(FORMATO_PARA_PROFILE),
        help="Formato legado de copy",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="comando", required=True)

    score_parser = sub.add_parser(
        "score", help="Aplica o quality gate e emite scorecard JSON"
    )
    score_parser.add_argument("arquivo", help="Arquivo com o output gerado")
    _add_profile_selector(score_parser, required=True)
    score_parser.set_defaults(func=cmd_score)

    pair_parser = sub.add_parser(
        "pair", help="Imprime uma rodada do julgador par a par"
    )
    pair_parser.add_argument("--candidato", required=True, help="Peça candidata")
    pair_parser.add_argument("--referencia", required=True, help="Peça de referência")
    pair_parser.add_argument("--briefing", help="Arquivo com o briefing do caso")
    pair_parser.add_argument(
        "--inverter", action="store_true", help="Troca os rótulos A e B"
    )
    _add_profile_selector(pair_parser, required=False)
    pair_parser.set_defaults(func=cmd_pair)

    consolidate_parser = sub.add_parser(
        "consolidate", help="Consolida os julgamentos normal e invertido"
    )
    consolidate_parser.add_argument(
        "--normal", required=True, help="JSON retornado na ordem normal"
    )
    consolidate_parser.add_argument(
        "--invertida", required=True, help="JSON retornado na ordem invertida"
    )
    _add_profile_selector(consolidate_parser, required=False)
    consolidate_parser.set_defaults(func=cmd_consolidate)

    profiles_parser = sub.add_parser(
        "profiles", help="Lista os perfis de avaliação disponíveis"
    )
    profiles_parser.set_defaults(func=cmd_profiles)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
