"""Contratos executáveis dos workflows de integração e release."""

import os
from pathlib import Path
import re
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[2]


def _workflow(name: str) -> dict:
    return yaml.safe_load(
        (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
    )


def test_codecov_uses_current_files_input():
    workflow = _workflow("tests.yml")
    steps = workflow["jobs"]["test"]["steps"]
    upload = next(step for step in steps if step.get("uses", "").startswith("codecov/"))
    inputs = upload.get("with", {})

    assert inputs.get("files") == "./coverage.xml"
    assert "file" not in inputs


def test_release_waits_for_full_verification():
    workflow = _workflow("release.yml")
    jobs = workflow["jobs"]

    assert "verify" in jobs, "release por tag precisa de job verify próprio"
    needs = jobs["release"].get("needs", [])
    if isinstance(needs, str):
        needs = [needs]
    assert "verify" in needs

    commands = "\n".join(
        step.get("run", "") for step in jobs["verify"].get("steps", [])
    )
    for required in (
        "--cov-fail-under=70",
        "black --check --diff scripts/*.py scripts/hooks/",
        "flake8 scripts/",
        "validate_agents.py --strict",
        "build_codex_plugin.py --check",
        "validate_codex_plugin.py plugins/marketing-os",
    ):
        assert required in commands, f"verify sem comando obrigatório: {required}"


def test_release_extracts_notes_from_canonical_changelog(tmp_path):
    workflow = _workflow("release.yml")
    steps = workflow["jobs"]["release"]["steps"]
    extraction = next(step for step in steps if step.get("id") == "changelog")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## v(?P<version>\d+\.\d+\.\d+) ", changelog, re.MULTILINE)
    assert match, "CHANGELOG sem seção canônica de versão"

    output_path = tmp_path / "github-output.txt"
    env = os.environ | {
        "GITHUB_REF_NAME": f"v{match.group('version')}",
        "GITHUB_OUTPUT": str(output_path),
    }
    subprocess.run(
        ["bash", "-eu", "-o", "pipefail", "-c", extraction["run"]],
        cwd=ROOT,
        env=env,
        check=True,
    )

    output = output_path.read_text(encoding="utf-8")
    assert "Esta release" in output
    assert "ver CHANGELOG.md para detalhes" not in output
