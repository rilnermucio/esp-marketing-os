"""Contratos executáveis dos workflows de integração e release."""

from pathlib import Path

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
