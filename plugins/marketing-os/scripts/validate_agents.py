#!/usr/bin/env python3
"""
validate_agents.py — Valida native subagents do Claude Code em agents/

Checa:
1. YAML frontmatter presente e bem-formado
2. Campos obrigatórios: name, description
3. Campos recomendados: tools, model
4. Knowledge base referenciada existe (se o agent referencia subagents/*.md)
5. Nome do arquivo bate com campo name
6. Sem duplicatas de name
7. Prompt que instrui rodar `python3 scripts/*.py` tem Bash na tools list
   (senão é instrução morta: o agent nunca consegue executar)

Uso:
    python scripts/validate_agents.py
    python scripts/validate_agents.py --strict    # falha em warnings também
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml  # type: ignore

    _HAS_YAML = True
except ImportError:
    yaml = None  # type: ignore
    _HAS_YAML = False


def _parse_simple_yaml(text: str) -> dict:
    """Parser minimal para frontmatter flat: key: value / key: [a, b, c] / key: | ... .

    Não suporta estruturas aninhadas complexas — suficiente para frontmatter
    de native subagents (name, description, tools, model, color).
    """
    result: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            i += 1
            continue
        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'") and len(value) >= 2:
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            items = [
                x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()
            ]
            result[key] = items
            i += 1
            continue
        result[key] = value
        i += 1
    return result


def _yaml_load(text: str) -> dict:
    if _HAS_YAML:
        loaded = yaml.safe_load(text)
        if isinstance(loaded, dict):
            return loaded
        return {}
    return _parse_simple_yaml(text)


AGENTS_DIR = Path("agents")
PROJECT_ROOT = Path(".")

REQUIRED_FIELDS = ["name", "description"]
RECOMMENDED_FIELDS = ["tools", "model"]
VALID_MODELS = {"opus", "sonnet", "haiku", "inherit"}
KNOWN_TOOLS = {
    "Bash",
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "LS",
    "WebSearch",
    "WebFetch",
    "NotebookEdit",
    "NotebookRead",
    "TodoWrite",
    "KillShell",
    "BashOutput",
    "Agent",
    "ExitPlanMode",
    "ExitWorktree",
    "EnterWorktree",
    "EnterPlanMode",
    "AskUserQuestion",
}

KNOWLEDGE_REF_RE = re.compile(r"`?(subagents/[a-zA-Z0-9_\-/]+\.md)`?")

# Scripts que o prompt manda o USUÁRIO rodar (bootstrap manual), não o agent.
# Referenciá-los não exige Bash na tools list.
USER_RUN_SCRIPTS = {"init_agent_memory.py"}

SCRIPT_RUN_RE = re.compile(r"python3?\s+scripts/([a-zA-Z0-9_\-/]+\.py)")


@dataclass
class AgentReport:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def clean(self) -> bool:
        return not self.errors and not self.warnings


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extrai frontmatter YAML do início do arquivo. Retorna (meta, body)."""
    if not content.startswith("---\n"):
        return None, content
    end = content.find("\n---", 4)
    if end == -1:
        return None, content
    fm_str = content[4:end]
    body = content[end + 4 :].lstrip("\n")
    try:
        meta = _yaml_load(fm_str)
    except Exception as e:
        return {"__yaml_error__": str(e)}, body
    if not isinstance(meta, dict):
        return None, body
    return meta, body


def validate_tools(tools_raw, report: AgentReport) -> None:
    if tools_raw is None:
        return
    if isinstance(tools_raw, str):
        tools = [t.strip() for t in tools_raw.split(",") if t.strip()]
    elif isinstance(tools_raw, list):
        tools = [str(t).strip() for t in tools_raw]
    else:
        report.warnings.append(
            f"Campo 'tools' tem tipo inesperado: {type(tools_raw).__name__}"
        )
        return
    unknown = [t for t in tools if t not in KNOWN_TOOLS and not t.startswith("mcp__")]
    if unknown:
        report.warnings.append(
            f"Tools desconhecidas (podem ser válidas se novas): {unknown}"
        )
    report.info["tools_count"] = len(tools)
    report.info["tools"] = tools


def validate_knowledge_refs(body: str, report: AgentReport) -> None:
    refs = set(KNOWLEDGE_REF_RE.findall(body))
    if not refs:
        report.warnings.append(
            "Nenhuma referência a knowledge base (`subagents/*.md`) encontrada. Tier-1 deveria apontar pra tier-2."
        )
        return
    missing = []
    for ref in refs:
        ref_path = PROJECT_ROOT / ref
        if not ref_path.exists():
            missing.append(ref)
    if missing:
        report.errors.append(f"Knowledge refs ausentes no filesystem: {missing}")
    report.info["knowledge_refs"] = sorted(refs)


def validate_script_refs_require_bash(
    meta: dict, body: str, report: AgentReport
) -> None:
    """Prompt que manda rodar scripts exige Bash em tools, senão é instrução morta."""
    if "tools" not in meta:
        # Sem campo tools o agent herda o toolset completo (inclui Bash)
        return
    tools = report.info.get("tools", [])
    refs = {
        m
        for m in SCRIPT_RUN_RE.findall(body)
        if m.rsplit("/", 1)[-1] not in USER_RUN_SCRIPTS
    }
    if refs and "Bash" not in tools:
        report.warnings.append(
            f"Body instrui rodar scripts ({sorted(refs)}) mas 'Bash' não está em tools. "
            "Instrução morta: adicione Bash ao frontmatter ou remova a referência."
        )


def validate_agent(path: Path, seen_names: dict[str, Path]) -> AgentReport:
    report = AgentReport(path=path)
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        report.errors.append(f"Falha ao ler arquivo: {e}")
        return report

    meta, body = parse_frontmatter(content)
    if meta is None:
        report.errors.append("Frontmatter YAML ausente ou malformado")
        return report
    if "__yaml_error__" in meta:
        report.errors.append(f"YAML inválido: {meta['__yaml_error__']}")
        return report

    for field_name in REQUIRED_FIELDS:
        if field_name not in meta or not meta[field_name]:
            report.errors.append(f"Campo obrigatório ausente: '{field_name}'")

    for field_name in RECOMMENDED_FIELDS:
        if field_name not in meta:
            report.warnings.append(f"Campo recomendado ausente: '{field_name}'")

    name = meta.get("name")
    if name:
        expected_filename = f"{name}.md"
        if path.name != expected_filename:
            report.errors.append(
                f"Nome do arquivo '{path.name}' não bate com campo name='{name}' (esperado '{expected_filename}')"
            )
        if name in seen_names:
            report.errors.append(f"Nome duplicado '{name}' (já em {seen_names[name]})")
        else:
            seen_names[name] = path

    description = meta.get("description", "")
    if description and len(description) < 50:
        report.warnings.append(
            f"Description curta ({len(description)} chars). Recomendado 100+ chars com triggers claros."
        )
    if description and len(description) > 800:
        report.warnings.append(
            f"Description muito longa ({len(description)} chars). Recomendado < 500 chars."
        )

    model = meta.get("model")
    if model and model not in VALID_MODELS:
        report.warnings.append(f"Model '{model}' fora de {VALID_MODELS}")

    validate_tools(meta.get("tools"), report)
    validate_knowledge_refs(body, report)
    validate_script_refs_require_bash(meta, body, report)

    report.info["body_lines"] = body.count("\n")
    report.info["name"] = name
    report.info["description_len"] = len(description) if description else 0

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida native subagents Claude Code")
    parser.add_argument("--strict", action="store_true", help="Falha em warnings")
    parser.add_argument(
        "--dir", type=Path, default=AGENTS_DIR, help="Diretório de agents"
    )
    args = parser.parse_args()

    agents_dir = args.dir
    if not agents_dir.exists():
        print(f"ERRO: diretório não existe: {agents_dir}", file=sys.stderr)
        return 2

    agent_files = sorted(agents_dir.glob("*.md"))
    if not agent_files:
        print(f"AVISO: nenhum agent encontrado em {agents_dir}")
        return 0

    seen_names: dict[str, Path] = {}
    reports = [validate_agent(p, seen_names) for p in agent_files]

    total = len(reports)
    ok = sum(1 for r in reports if r.ok)
    clean = sum(1 for r in reports if r.clean)
    with_errors = total - ok
    with_warnings = sum(1 for r in reports if r.warnings)

    print(f"\n{'='*60}")
    print(f"Validação de Native Subagents — {agents_dir}")
    print(f"{'='*60}\n")

    for r in reports:
        status = "OK" if r.clean else ("WARN" if r.ok else "FAIL")
        print(f"[{status}] {r.path.name}")
        if r.info.get("name"):
            parts = [f"name={r.info['name']}"]
            if r.info.get("tools_count"):
                parts.append(f"tools={r.info['tools_count']}")
            if r.info.get("body_lines"):
                parts.append(f"lines={r.info['body_lines']}")
            if r.info.get("knowledge_refs"):
                parts.append(f"knowledge={len(r.info['knowledge_refs'])}")
            print(f"  {' | '.join(parts)}")
        for err in r.errors:
            print(f"  ERROR: {err}")
        for warn in r.warnings:
            print(f"  WARN: {warn}")
        print()

    print(f"{'='*60}")
    print(
        f"Total: {total} | Clean: {clean} | OK (sem erros): {ok} | Com warnings: {with_warnings} | Falhas: {with_errors}"
    )
    print(f"{'='*60}\n")

    if with_errors > 0:
        return 1
    if args.strict and with_warnings > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
