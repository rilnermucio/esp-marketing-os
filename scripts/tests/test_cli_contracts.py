"""Toda invocação de script citada nos prompts precisa ser aceita pelo argparse do script.

Auditoria 2026-09-28 (achado #8, F-BLOAT-02): agents mandavam rodar
`apify serp "<kw>"` (o script exige --query), `apify_instagram.py "@handle"`
(exige --handle) e `metrics_collector.py --summary` (flag inexistente, e
--metrica obrigatória). `validate_agents.py` só checava se o script existia.

O contrato é lido do código por AST, sem executar os scripts.
"""

from __future__ import annotations

import ast
import re
import shlex
import sys
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import mos  # noqa: E402

SOURCES = (
    sorted((ROOT / "agents").glob("mos-*.md"))
    + sorted((ROOT / "commands").glob("*.md"))
    + [ROOT / "skills" / "marketing-os" / "SKILL.md"]
    + sorted((ROOT / "subagents").glob("*.md"))
    + sorted((ROOT / "workflows").glob("*.md"))
)
INVOCATION = re.compile(
    r"python3?\s+\"?(?:\$\{CLAUDE_PLUGIN_ROOT\}/)?scripts/([A-Za-z0-9_]+)\.py\"?([^`\n]*)"
)
SHELL_BREAK = re.compile(r"\s(?:\||;|&&|2?>)\s?")
NO_VALUE_ACTIONS = {
    "store_true",
    "store_false",
    "count",
    "help",
    "version",
    "store_const",
}


def _literal(node):
    return node.value if isinstance(node, ast.Constant) else None


def _collect_arguments(tree: ast.AST, spec: dict) -> None:
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr == "add_subparsers":
            spec["subcommands"] = True
        if node.func.attr != "add_argument":
            continue
        names = [a.value for a in node.args if isinstance(_literal(a), str)]
        if not names:
            continue
        keywords = {k.arg: k.value for k in node.keywords}
        action = _literal(keywords.get("action"))
        takes_value = action not in NO_VALUE_ACTIONS
        if names[0].startswith("-"):
            for name in names:
                spec["options"][name] = takes_value
            if _literal(keywords.get("required")) is True:
                spec["required"].append(tuple(names))
        else:
            spec["positionals"].append(_literal(keywords.get("nargs")))


@lru_cache(maxsize=None)
def cli_spec(script_name: str) -> dict | None:
    path = SCRIPTS / f"{script_name}.py"
    if not path.exists():
        return {"missing": True}
    tree = ast.parse(path.read_text(encoding="utf-8"))
    spec = {"options": {}, "positionals": [], "required": [], "subcommands": False}
    _collect_arguments(tree, spec)
    helpers = {
        n.func.id
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    }
    if "add_output_args" in helpers:
        formatter = ast.parse(
            (SCRIPTS / "output_formatter.py").read_text(encoding="utf-8")
        )
        _collect_arguments(formatter, spec)
    if not (spec["options"] or spec["positionals"] or spec["subcommands"]):
        return None  # script sem argparse: fora do escopo deste guard
    spec["options"].update({"-h": False, "--help": False})
    return spec


def _is_placeholder(token: str) -> bool:
    return token[:1] in "<{[" or token in ("...", "…") or token.startswith("$")


PLACEHOLDER_SPAN = re.compile(r"<[^<>\n]*>|\{[^{}\n]*\}|\[[^\[\]\n]*\]")


def _tokens(raw: str) -> list[str]:
    raw = SHELL_BREAK.split(raw, maxsplit=1)[0].strip()
    # Placeholder com espaço (<texto escolhido do brief>) vale como um token só.
    raw = PLACEHOLDER_SPAN.sub(lambda m: m.group(0)[0] + "ph" + m.group(0)[-1], raw)
    try:
        return shlex.split(raw)
    except ValueError:
        return raw.split()


def check_invocation(script: str, args: list[str]) -> list[str]:
    if script == "mos":
        if len(args) < 2 or any(_is_placeholder(a) for a in args[:2]):
            return []
        category, command = args[0], args[1]
        if category not in mos.COMMAND_MAP or command not in mos.COMMAND_MAP[category]:
            return [f"`mos.py {category} {command}` não existe no COMMAND_MAP"]
        target = mos.COMMAND_MAP[category][command][0][: -len(".py")]
        transform = mos.SPECIAL_ARGS.get((category, command), lambda a: a)
        return check_invocation(target, transform(list(args[2:])))

    spec = cli_spec(script)
    if spec is None or not args:
        return []  # sem argparse, ou menção em prosa sem argumentos
    if spec.get("missing"):
        return [f"scripts/{script}.py não existe"]
    partial = any(t.startswith("[") or t in ("...", "…") for t in args)
    problems: list[str] = []
    positionals = 0
    present: set[str] = set()
    i = 0
    while i < len(args):
        token = args[i]
        if token.startswith("-") and not re.fullmatch(r"-\d+(\.\d+)?", token):
            flag = token.split("=", 1)[0]
            if flag not in spec["options"]:
                problems.append(f"flag inexistente {flag}")
            else:
                present.add(flag)
                if spec["options"][flag] and "=" not in token and i + 1 < len(args):
                    i += 1
        else:
            positionals += 1
        i += 1

    if not spec["subcommands"]:
        variadic = any(n in ("*", "+", "...") for n in spec["positionals"])
        if not variadic and positionals > len(spec["positionals"]) and not partial:
            problems.append(
                f"{positionals} argumento(s) posicional(is), o script aceita {len(spec['positionals'])}"
            )
    # Com subcomandos, flag obrigatória pertence a um subparser específico.
    if spec["subcommands"]:
        return problems
    if not partial and "--help" not in present and "-h" not in present:
        for names in spec["required"]:
            if not present.intersection(names):
                problems.append(f"flag obrigatória ausente {names[-1]}")
    return problems


def _invocations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        for match in INVOCATION.finditer(line):
            rest, cursor = match.group(2), index
            # Comando quebrado em várias linhas com barra invertida.
            while rest.rstrip().endswith("\\") and cursor + 1 < len(lines):
                cursor += 1
                rest = rest.rstrip()[:-1] + " " + lines[cursor].strip()
            yield index + 1, match.group(1), _tokens(rest)


SOURCES_WITH_CALLS = [p for p in SOURCES if any(True for _ in _invocations(p))]


@pytest.mark.parametrize(
    "path", SOURCES_WITH_CALLS, ids=lambda p: str(p.relative_to(ROOT))
)
def test_documented_invocations_match_argparse(path: Path) -> None:
    failures = []
    for number, script, args in _invocations(path):
        for problem in check_invocation(script, args):
            failures.append(
                f"linha {number}: scripts/{script}.py {' '.join(args)} -> {problem}"
            )
    assert not failures, "\n".join(failures)


def test_checker_catches_the_audited_cases() -> None:
    assert check_invocation("metrics_collector", ["--summary"])
    assert check_invocation("apify_instagram", ["@creator"])
    assert check_invocation("mos", ["apify", "serp", "marketing digital"])
    assert not check_invocation("apify_serp", ["--query", "marketing digital"])
    assert not check_invocation("metrics_collector", ["--help"])
