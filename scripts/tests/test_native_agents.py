"""Roda scripts/validate_agents.py em modo strict sobre agents/ (agents do plugin).

Até 2026-09 este teste procurava .claude/agents/, que não existe desde a
reestruturação plugin-first (v6.0), e por isso pulava sempre.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_validate_agents_script_exists(project_root: Path) -> None:
    script = project_root / "scripts" / "validate_agents.py"
    assert script.exists(), f"validate_agents.py missing: {script}"


def test_plugin_agents_dir_exists(project_root: Path) -> None:
    assert (project_root / "agents").is_dir(), "agents/ ausente"


def test_plugin_agents_validate_strict(project_root: Path) -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_agents.py", "--strict"],
        capture_output=True,
        text=True,
        cwd=str(project_root),
        timeout=60,
    )
    assert result.returncode == 0, (
        f"validate_agents.py --strict falhou (exit {result.returncode}):\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
