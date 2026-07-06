#!/usr/bin/env python3
"""
project_manager.py - Workflow de projetos de marketing com handoffs e approval gates.

State machine declarativa por projeto:
- project.md (frontmatter YAML + body)
- runs.jsonl (append-only log de execucoes)
- decisions.md (historico de aprovacoes/rejeicoes)
- pastas <NN>-<stage>/ (artifacts por estagio, criadas sob demanda)

Uso:
    python project_manager.py novo "Lancamento Curso IA" --tipo lancamento
    python project_manager.py list
    python project_manager.py status lancamento-curso-ia
    python project_manager.py avancar lancamento-curso-ia
    python project_manager.py aprovar lancamento-curso-ia
    python project_manager.py rejeitar lancamento-curso-ia "feedback"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_ROOT = REPO_ROOT / "workspace" / "projects"
TEMPLATES_DIR = REPO_ROOT / "scripts" / "templates" / "projeto"

PROJECT_TYPES = ("lancamento", "perpetuo", "consultoria", "mentoria")


# ---------- helpers ----------


def slugify(text: str) -> str:
    """Converte texto livre em slug URL-safe."""
    text = text.lower().strip()
    accent_map = {
        "[àáâãä]": "a",
        "[èéêë]": "e",
        "[ìíîï]": "i",
        "[òóôõö]": "o",
        "[ùúûü]": "u",
        "[ç]": "c",
    }
    for pattern, repl in accent_map.items():
        text = re.sub(pattern, repl, text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def load_template(project_type: str) -> str:
    """Carrega template de um tipo de projeto."""
    if project_type not in PROJECT_TYPES:
        raise ValueError(
            f"invalid type '{project_type}'. Valid: {', '.join(PROJECT_TYPES)}"
        )
    template_path = TEMPLATES_DIR / f"{project_type}.md"
    return template_path.read_text(encoding="utf-8")


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extrai frontmatter YAML + body de um arquivo Markdown."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content
    fm = yaml.safe_load(match.group(1)) or {}
    body = match.group(2)
    return fm, body


def serialize_frontmatter(fm: dict, body: str) -> str:
    """Serializa frontmatter + body de volta pra Markdown."""
    yaml_str = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{yaml_str}\n---\n\n{body.strip()}\n"


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# ---------- create ----------


def create_project(name: str, project_type: str) -> Path:
    """Cria estrutura nova do projeto em workspace/projects/<slug>/."""
    if project_type not in PROJECT_TYPES:
        raise ValueError(
            f"invalid type '{project_type}'. Valid: {', '.join(PROJECT_TYPES)}"
        )

    slug = slugify(name)
    project_dir = PROJECTS_ROOT / slug

    if project_dir.exists():
        raise FileExistsError(f"projeto ja existe: {slug}")

    project_dir.mkdir(parents=True, exist_ok=True)

    template = load_template(project_type)
    created_at = datetime.now().isoformat(timespec="seconds")
    rendered = template.format(name=name, slug=slug, created_at=created_at)
    (project_dir / "project.md").write_text(rendered, encoding="utf-8")

    (project_dir / "runs.jsonl").touch()
    (project_dir / "decisions.md").write_text(
        f"# Decisoes: {name}\n\n", encoding="utf-8"
    )

    return project_dir


# ---------- list ----------


def list_projects() -> list[dict]:
    """Lista todos os projetos com snapshot de estado."""
    if not PROJECTS_ROOT.exists():
        return []
    out = []
    for entry in sorted(PROJECTS_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        project_md = entry / "project.md"
        if not project_md.is_file():
            continue
        fm, _ = parse_frontmatter(project_md.read_text(encoding="utf-8"))
        out.append(
            {
                "slug": fm.get("slug", entry.name),
                "name": fm.get("name", entry.name),
                "type": fm.get("type", "?"),
                "status": fm.get("status", "?"),
                "current_stage": fm.get("current_stage", "?"),
            }
        )
    return out


# ---------- status ----------


def project_status(slug: str) -> dict:
    """Snapshot completo do estado de um projeto."""
    project_dir = PROJECTS_ROOT / slug
    project_md = project_dir / "project.md"
    if not project_md.is_file():
        raise FileNotFoundError(f"projeto nao encontrado: {slug}")

    fm, _ = parse_frontmatter(project_md.read_text(encoding="utf-8"))
    runs = _read_jsonl(project_dir / "runs.jsonl")

    return {
        "slug": slug,
        "name": fm.get("name", slug),
        "type": fm.get("type"),
        "status": fm.get("status"),
        "current_stage": fm.get("current_stage"),
        "pipeline": fm.get("pipeline", []),
        "default_approval": fm.get("default_approval", "required"),
        "last_run": runs[-1] if runs else None,
        "total_runs": len(runs),
    }


# ---------- run log ----------


def append_run(slug: str, run: dict) -> dict:
    """Appenda uma linha em runs.jsonl. Preenche run_id e started_at se faltarem."""
    project_dir = PROJECTS_ROOT / slug
    runs_path = project_dir / "runs.jsonl"
    existing = _read_jsonl(runs_path)
    next_id = f"run_{len(existing) + 1:03d}"

    run = dict(run)
    run.setdefault("run_id", next_id)
    run.setdefault("started_at", datetime.now().isoformat(timespec="seconds"))

    with runs_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(run, ensure_ascii=False) + "\n")
    return run


# ---------- state machine ----------


def _update_frontmatter(slug: str, updates: dict) -> dict:
    """Mescla updates no frontmatter do project.md e regrava."""
    project_md = PROJECTS_ROOT / slug / "project.md"
    fm, body = parse_frontmatter(project_md.read_text(encoding="utf-8"))
    fm.update(updates)
    project_md.write_text(serialize_frontmatter(fm, body), encoding="utf-8")
    return fm


def _next_stage(pipeline: list[dict], current_id: str) -> Optional[dict]:
    for i, stage in enumerate(pipeline):
        if stage["id"] == current_id and i + 1 < len(pipeline):
            return pipeline[i + 1]
    return None


def _current_stage_def(pipeline: list[dict], current_id: str) -> Optional[dict]:
    for stage in pipeline:
        if stage["id"] == current_id:
            return stage
    return None


def _stage_iteration(slug: str, stage_id: str) -> int:
    """Quantas vezes esse stage rodou ate agora? (proxima iteracao = N+1)"""
    runs = _read_jsonl(PROJECTS_ROOT / slug / "runs.jsonl")
    return sum(1 for r in runs if r.get("stage_id") == stage_id) + 1


def _stage_index(pipeline: list[dict], stage_id: str) -> int:
    """Retorna posicao 1-based do stage no pipeline (pra prefixo de pasta)."""
    for i, s in enumerate(pipeline, start=1):
        if s["id"] == stage_id:
            return i
    raise ValueError(f"stage '{stage_id}' nao esta na pipeline")


def stage_folder(slug: str, stage_id: str) -> Path:
    """Caminho da pasta do stage (NN-stage_id, auto-criada por advance_stage)."""
    state = project_status(slug)
    idx = _stage_index(state["pipeline"], stage_id)
    return PROJECTS_ROOT / slug / f"{idx:02d}-{stage_id}"


def _rewrite_runs(slug: str, runs: list[dict]) -> None:
    runs_path = PROJECTS_ROOT / slug / "runs.jsonl"
    runs_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in runs) + "\n",
        encoding="utf-8",
    )


def _append_decision(
    slug: str, stage_id: str, run_id: str, decision: str, feedback: Optional[str]
) -> None:
    when = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = [f"\n## {when} {stage_id} ({run_id})", f"- **Decisao:** {decision}"]
    if feedback:
        block.append(f"- **Feedback:** {feedback}")
    block.append("")
    decisions_md = PROJECTS_ROOT / slug / "decisions.md"
    with decisions_md.open("a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")


def advance_stage(slug: str) -> dict:
    """Cria run pendente pro stage atual + auto-cria pasta do stage.

    Nao executa o agente. Quem executa eh o slash command /projeto.
    Esse helper registra "vai rodar isso agora" e prepara filesystem.
    """
    state = project_status(slug)
    stage_def = _current_stage_def(state["pipeline"], state["current_stage"])
    if stage_def is None:
        raise ValueError(f"stage atual '{state['current_stage']}' nao esta na pipeline")
    iteration = _stage_iteration(slug, stage_def["id"])

    folder = stage_folder(slug, stage_def["id"])
    folder.mkdir(parents=True, exist_ok=True)

    run = append_run(
        slug,
        {
            "stage_id": stage_def["id"],
            "agent": stage_def["agent"],
            "iteration": iteration,
            "status": "pending",
            "source": "pipeline",
            "folder": str(folder.relative_to(PROJECTS_ROOT / slug)),
        },
    )
    return run


def complete_run(slug: str, output_path: Optional[str] = None) -> dict:
    """Marca ultimo run pending como pending_approval com output path.

    Auto-aprova se o stage tem approval: skip (avanca pra proximo stage automaticamente).
    Chamado pelo /projeto avancar depois que o agente devolveu output.
    """
    project_dir = PROJECTS_ROOT / slug
    runs = _read_jsonl(project_dir / "runs.jsonl")
    if not runs:
        raise ValueError("nenhum run pra completar")
    last = runs[-1]
    if last.get("status") != "pending":
        raise ValueError(f"ultimo run nao esta pending: {last.get('status')}")

    last["status"] = "pending_approval"
    last["completed_at"] = datetime.now().isoformat(timespec="seconds")
    if output_path:
        last["output"] = output_path
    _rewrite_runs(slug, runs)

    state = project_status(slug)
    stage_def = _current_stage_def(state["pipeline"], last["stage_id"])
    approval = (
        stage_def.get("approval", state["default_approval"])
        if stage_def
        else "required"
    )
    if approval == "skip":
        return approve_stage(slug)
    return state


def approve_stage(slug: str) -> dict:
    """Aprova ultimo run pendente e avanca current_stage.

    Se ja for o ultimo stage da pipeline, marca status: completed.
    """
    project_dir = PROJECTS_ROOT / slug
    runs = _read_jsonl(project_dir / "runs.jsonl")
    if not runs:
        raise ValueError("nenhum run para aprovar")

    last = runs[-1]
    if last.get("status") not in ("pending", "running", "pending_approval"):
        raise ValueError(
            f"ultimo run nao esta aguardando aprovacao: {last.get('status')}"
        )

    last["status"] = "approved"
    last["approved_at"] = datetime.now().isoformat(timespec="seconds")
    _rewrite_runs(slug, runs)

    _append_decision(slug, last["stage_id"], last["run_id"], "aprovado", feedback=None)

    state = project_status(slug)
    next_stage = _next_stage(state["pipeline"], last["stage_id"])
    if next_stage is None:
        _update_frontmatter(slug, {"status": "completed"})
    else:
        _update_frontmatter(slug, {"current_stage": next_stage["id"]})

    return project_status(slug)


def reject_stage(slug: str, feedback: str) -> dict:
    """Rejeita ultimo run e mantem current_stage (proxima execucao re-roda com feedback)."""
    project_dir = PROJECTS_ROOT / slug
    runs = _read_jsonl(project_dir / "runs.jsonl")
    if not runs:
        raise ValueError("nenhum run para rejeitar")

    last = runs[-1]
    last["status"] = "rejected"
    last["rejected_at"] = datetime.now().isoformat(timespec="seconds")
    last["feedback"] = feedback
    _rewrite_runs(slug, runs)

    _append_decision(
        slug, last["stage_id"], last["run_id"], "rejeitado", feedback=feedback
    )
    return project_status(slug)


# ---------- CLI ----------


def _print_status(state: dict) -> None:
    print(f"\nProjeto: {state['name']} ({state['slug']})")
    print(f"Tipo: {state['type']}  Status: {state['status']}")
    print(f"Stage atual: {state['current_stage']}")
    print(f"Total de runs: {state['total_runs']}")
    if state.get("last_run"):
        lr = state["last_run"]
        print(
            f"Ultimo run: {lr.get('run_id')} stage={lr.get('stage_id')} "
            f"status={lr.get('status')} iter={lr.get('iteration')}"
        )
    print("\nPipeline:")
    for s in state["pipeline"]:
        marker = ">" if s["id"] == state["current_stage"] else " "
        approval = s.get("approval", state["default_approval"])
        print(f"  {marker} {s['id']:<14} agent={s['agent']:<18} approval={approval}")


def _print_list(projects: list[dict]) -> None:
    if not projects:
        print("Nenhum projeto encontrado em workspace/projects/.")
        return
    print(f"\n{len(projects)} projeto(s):\n")
    for p in projects:
        print(
            f"  [{p['status']:<10}] {p['slug']:<28} tipo={p['type']:<12} "
            f"stage={p['current_stage']}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Workflow de projetos do Marketing OS (handoffs + approvals)."
    )
    sub = parser.add_subparsers(dest="cmd")

    p_novo = sub.add_parser("novo", help="Criar novo projeto")
    p_novo.add_argument("name")
    p_novo.add_argument(
        "--tipo", required=True, choices=PROJECT_TYPES, help="Tipo do projeto"
    )

    sub.add_parser("list", help="Listar projetos")

    p_status = sub.add_parser("status", help="Mostrar estado de um projeto")
    p_status.add_argument("slug")

    p_avancar = sub.add_parser(
        "avancar", help="Cria run pendente pro stage atual + auto-cria pasta"
    )
    p_avancar.add_argument("slug")

    p_completar = sub.add_parser(
        "completar", help="Marca run pending como pending_approval (com output)"
    )
    p_completar.add_argument("slug")
    p_completar.add_argument(
        "--output", help="Path relativo do output (ex: 01-research/draft-v1.md)"
    )

    p_aprovar = sub.add_parser("aprovar", help="Aprova ultimo run e avanca stage")
    p_aprovar.add_argument("slug")

    p_rejeitar = sub.add_parser("rejeitar", help="Rejeita ultimo run com feedback")
    p_rejeitar.add_argument("slug")
    p_rejeitar.add_argument("feedback")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    try:
        if args.cmd == "novo":
            project_dir = create_project(args.name, args.tipo)
            print(f"Projeto criado em {project_dir}")
            _print_status(project_status(slugify(args.name)))
        elif args.cmd == "list":
            _print_list(list_projects())
        elif args.cmd == "status":
            _print_status(project_status(args.slug))
        elif args.cmd == "avancar":
            run = advance_stage(args.slug)
            print(
                f"Run pendente criado: {run['run_id']} stage={run['stage_id']} agent={run['agent']}"
            )
            print(f"Pasta do stage: workspace/projects/{args.slug}/{run['folder']}/")
            print(
                "Agora /projeto despacha o agente. Quando terminar, use 'completar' + 'aprovar'/'rejeitar'."
            )
        elif args.cmd == "completar":
            state = complete_run(args.slug, args.output)
            print(
                f"Run completado. Stage: {state['current_stage']} status={state['status']}"
            )
            if state.get("last_run", {}).get("status") == "approved":
                print(f"(approval: skip detectado, auto-aprovado e avancado)")
        elif args.cmd == "aprovar":
            state = approve_stage(args.slug)
            print(
                f"Stage aprovado. Novo stage atual: {state['current_stage']} (status={state['status']})"
            )
        elif args.cmd == "rejeitar":
            state = reject_stage(args.slug, args.feedback)
            print(f"Stage rejeitado. Stage atual continua: {state['current_stage']}")
            print("Feedback registrado em decisions.md.")
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
