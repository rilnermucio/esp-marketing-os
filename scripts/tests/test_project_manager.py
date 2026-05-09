"""Testes para project_manager.py - workflow com handoffs e approval gates."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from project_manager import (  # noqa: E402
    PROJECT_TYPES,
    advance_stage,
    append_run,
    approve_stage,
    complete_run,
    create_project,
    list_projects,
    load_template,
    parse_frontmatter,
    project_status,
    reject_stage,
    serialize_frontmatter,
    slugify,
    stage_folder,
)


@pytest.fixture
def tmp_workspace(monkeypatch):
    """Workspace isolado em tmpdir."""
    tmpdir = tempfile.mkdtemp()
    workspace = Path(tmpdir) / "workspace" / "projects"
    workspace.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("project_manager.PROJECTS_ROOT", workspace)
    yield workspace


def _read_jsonl_lines(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# ---------- slugify ----------

def test_slugify_basic():
    assert slugify("Lançamento Curso IA") == "lancamento-curso-ia"


def test_slugify_strips_special_chars():
    assert slugify("Cliente: ACME Inc.") == "cliente-acme-inc"


def test_slugify_collapses_whitespace():
    assert slugify("  varios   espacos  ") == "varios-espacos"


# ---------- templates ----------

def test_load_template_valid_type():
    tpl = load_template("lancamento")
    assert "{name}" in tpl
    assert "{slug}" in tpl
    assert "type: lancamento" in tpl


def test_load_template_invalid_type_raises():
    with pytest.raises(ValueError, match="invalid"):
        load_template("invalid")


def test_all_project_types_have_templates():
    for t in PROJECT_TYPES:
        tpl = load_template(t)
        assert f"type: {t}" in tpl


# ---------- frontmatter ----------

def test_parse_frontmatter_extracts_dict_and_body():
    content = """---
name: test
type: lancamento
current_stage: research
---

# Body content here
"""
    fm, body = parse_frontmatter(content)
    assert fm["name"] == "test"
    assert fm["type"] == "lancamento"
    assert fm["current_stage"] == "research"
    assert "Body content here" in body


def test_parse_frontmatter_no_frontmatter_returns_empty_dict():
    fm, body = parse_frontmatter("# No frontmatter here")
    assert fm == {}
    assert "No frontmatter" in body


def test_serialize_frontmatter_roundtrip():
    fm = {"name": "x", "type": "lancamento", "pipeline": [{"id": "a", "agent": "mos-x"}]}
    body = "# Hi"
    serialized = serialize_frontmatter(fm, body)
    fm2, body2 = parse_frontmatter(serialized)
    assert fm2 == fm
    assert body2.strip() == body.strip()


# ---------- create_project ----------

def test_create_project_creates_structure(tmp_workspace):
    create_project("Lançamento Curso IA", "lancamento")
    project_dir = tmp_workspace / "lancamento-curso-ia"
    assert project_dir.is_dir()
    assert (project_dir / "project.md").is_file()
    assert (project_dir / "runs.jsonl").is_file()
    assert (project_dir / "decisions.md").is_file()


def test_create_project_writes_frontmatter_correctly(tmp_workspace):
    create_project("Curso X", "lancamento")
    content = (tmp_workspace / "curso-x" / "project.md").read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    assert fm["name"] == "Curso X"
    assert fm["slug"] == "curso-x"
    assert fm["type"] == "lancamento"
    assert fm["current_stage"] == "research"
    assert fm["status"] == "active"
    assert isinstance(fm["pipeline"], list)
    assert len(fm["pipeline"]) > 0
    assert "Briefing" in body


def test_create_project_rejects_invalid_type(tmp_workspace):
    with pytest.raises(ValueError):
        create_project("X", "invalid")


def test_create_project_rejects_duplicate(tmp_workspace):
    create_project("Curso Y", "perpetuo")
    with pytest.raises(FileExistsError):
        create_project("Curso Y", "perpetuo")


def test_create_consultoria_starts_at_discovery(tmp_workspace):
    create_project("Cliente ACME", "consultoria")
    state = project_status("cliente-acme")
    assert state["current_stage"] == "discovery"


def test_create_mentoria_starts_at_planejamento(tmp_workspace):
    create_project("Cohort 2026", "mentoria")
    state = project_status("cohort-2026")
    assert state["current_stage"] == "planejamento"


# ---------- list ----------

def test_list_projects_empty(tmp_workspace):
    assert list_projects() == []


def test_list_projects_returns_all(tmp_workspace):
    create_project("Projeto A", "lancamento")
    create_project("Projeto B", "perpetuo")
    projects = list_projects()
    assert len(projects) == 2
    slugs = {p["slug"] for p in projects}
    assert slugs == {"projeto-a", "projeto-b"}
    assert all(p["status"] == "active" for p in projects)


# ---------- status ----------

def test_project_status_returns_state(tmp_workspace):
    create_project("Status Test", "lancamento")
    state = project_status("status-test")
    assert state["slug"] == "status-test"
    assert state["current_stage"] == "research"
    assert state["status"] == "active"
    assert state["pipeline"][0]["id"] == "research"
    assert state["last_run"] is None
    assert state["total_runs"] == 0


def test_project_status_unknown_slug_raises(tmp_workspace):
    with pytest.raises(FileNotFoundError):
        project_status("nao-existe")


# ---------- run log ----------

def test_append_run_writes_jsonl_line(tmp_workspace):
    create_project("Run Test", "lancamento")
    append_run("run-test", {
        "stage_id": "research",
        "agent": "mos-research",
        "iteration": 1,
        "status": "running",
    })
    runs = _read_jsonl_lines(tmp_workspace / "run-test" / "runs.jsonl")
    assert len(runs) == 1
    assert runs[0]["stage_id"] == "research"
    assert runs[0]["status"] == "running"
    assert "run_id" in runs[0]
    assert "started_at" in runs[0]


def test_append_run_increments_run_id(tmp_workspace):
    create_project("Multi", "perpetuo")
    append_run("multi", {"stage_id": "research", "agent": "mos-research", "status": "running"})
    append_run("multi", {"stage_id": "research", "agent": "mos-research", "status": "running"})
    runs = _read_jsonl_lines(tmp_workspace / "multi" / "runs.jsonl")
    assert runs[0]["run_id"] == "run_001"
    assert runs[1]["run_id"] == "run_002"


# ---------- state machine ----------

def test_advance_stage_creates_pending_run(tmp_workspace):
    create_project("Advance Test", "lancamento")
    run = advance_stage("advance-test")
    assert run["stage_id"] == "research"
    assert run["agent"] == "mos-research"
    assert run["status"] == "pending"
    assert run["iteration"] == 1
    assert run["source"] == "pipeline"


def test_approve_stage_advances_current_stage(tmp_workspace):
    create_project("Approve Test", "perpetuo")
    advance_stage("approve-test")
    runs_path = tmp_workspace / "approve-test" / "runs.jsonl"
    runs = _read_jsonl_lines(runs_path)
    runs[-1]["status"] = "pending_approval"
    runs_path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")

    state = approve_stage("approve-test")
    assert state["current_stage"] == "funil"
    assert state["last_run"]["status"] == "approved"
    assert "approved_at" in state["last_run"]


def test_approve_last_stage_completes_project(tmp_workspace):
    create_project("Final", "perpetuo")
    pipeline = project_status("final")["pipeline"]
    for stage in pipeline:
        advance_stage("final")
        runs_path = tmp_workspace / "final" / "runs.jsonl"
        runs = _read_jsonl_lines(runs_path)
        runs[-1]["status"] = "pending_approval"
        runs_path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")
        approve_stage("final")

    state = project_status("final")
    assert state["status"] == "completed"


def test_reject_stage_keeps_current_and_logs_feedback(tmp_workspace):
    create_project("Reject Test", "lancamento")
    advance_stage("reject-test")
    runs_path = tmp_workspace / "reject-test" / "runs.jsonl"
    runs = _read_jsonl_lines(runs_path)
    runs[-1]["status"] = "pending_approval"
    runs_path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")

    state = reject_stage("reject-test", "muito formal")
    assert state["current_stage"] == "research"
    assert state["last_run"]["status"] == "rejected"
    assert state["last_run"]["feedback"] == "muito formal"

    decisions = (tmp_workspace / "reject-test" / "decisions.md").read_text(encoding="utf-8")
    assert "muito formal" in decisions


def test_reject_then_advance_creates_iteration_2(tmp_workspace):
    create_project("Iter Test", "lancamento")
    advance_stage("iter-test")
    runs_path = tmp_workspace / "iter-test" / "runs.jsonl"
    runs = _read_jsonl_lines(runs_path)
    runs[-1]["status"] = "pending_approval"
    runs_path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")
    reject_stage("iter-test", "tenta de novo")

    run2 = advance_stage("iter-test")
    assert run2["iteration"] == 2
    assert run2["stage_id"] == "research"


# ---------- stage_folder + auto-mkdir ----------

def test_advance_stage_creates_folder(tmp_workspace):
    create_project("Folder Test", "lancamento")
    run = advance_stage("folder-test")
    assert run["folder"] == "01-research"
    folder = tmp_workspace / "folder-test" / "01-research"
    assert folder.is_dir()


def test_stage_folder_returns_correct_index(tmp_workspace):
    create_project("Idx Test", "lancamento")
    folder = stage_folder("idx-test", "copy")
    assert folder.name == "04-copy"


def test_stage_folder_unknown_stage_raises(tmp_workspace):
    create_project("Idx Test 2", "lancamento")
    with pytest.raises(ValueError, match="nao esta na pipeline"):
        stage_folder("idx-test-2", "naoexiste")


# ---------- complete_run ----------

def test_complete_run_updates_status_and_output(tmp_workspace):
    create_project("Complete Test", "lancamento")
    advance_stage("complete-test")
    state = complete_run("complete-test", "01-research/draft-v1.md")
    runs = _read_jsonl_lines(tmp_workspace / "complete-test" / "runs.jsonl")
    assert runs[-1]["output"] == "01-research/draft-v1.md"
    assert "completed_at" in runs[-1]
    assert state["current_stage"] in ("estrategia", "research")


def test_complete_run_with_skip_approval_auto_advances(tmp_workspace):
    create_project("Skip Test", "lancamento")
    advance_stage("skip-test")
    state = complete_run("skip-test", "01-research/draft-v1.md")
    assert state["current_stage"] == "estrategia"
    assert state["last_run"]["status"] == "approved"


def test_complete_run_with_required_approval_pauses(tmp_workspace):
    create_project("Pause Test", "perpetuo")
    advance_stage("pause-test")
    runs_path = tmp_workspace / "pause-test" / "runs.jsonl"
    runs = _read_jsonl_lines(runs_path)
    runs[-1]["status"] = "approved"
    runs_path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")
    _update_fm = __import__("project_manager")._update_frontmatter
    _update_fm("pause-test", {"current_stage": "funil"})

    advance_stage("pause-test")
    state = complete_run("pause-test", "02-funil/draft-v1.md")
    assert state["current_stage"] == "funil"
    assert state["last_run"]["status"] == "pending_approval"


def test_complete_run_without_pending_raises(tmp_workspace):
    create_project("Fail Test", "lancamento")
    with pytest.raises(ValueError, match="nenhum run"):
        complete_run("fail-test")


def test_complete_run_when_already_approved_raises(tmp_workspace):
    create_project("Twice Test", "perpetuo")
    advance_stage("twice-test")
    runs_path = tmp_workspace / "twice-test" / "runs.jsonl"
    runs = _read_jsonl_lines(runs_path)
    runs[-1]["status"] = "approved"
    runs_path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="nao esta pending"):
        complete_run("twice-test")
