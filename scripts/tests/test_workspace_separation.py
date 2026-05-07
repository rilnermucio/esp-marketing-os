"""Validates plugin code does not reference workspace/ paths."""
from __future__ import annotations

from pathlib import Path

import pytest


PLUGIN_DIRS = ["skills", "subagents", "commands", "workflows", "assets", "references", "agents"]
LEAK_PATTERNS = ["workspace/", "../workspace", "/workspace/"]
# Files that legitimately reference workspace/ by design (e.g. commands that read user-local samples)
WORKSPACE_REF_ALLOWLIST = {"commands/criar-meu-clone.md"}


def test_workspace_dir_exists_after_phase_1(project_root: Path) -> None:
    workspace = project_root / "workspace"
    assert workspace.is_dir(), (
        "workspace/ does not exist yet — expected to be created in Phase 1.\n"
        "If Phase 1 completed, this is a regression."
    )


def test_no_plugin_file_references_workspace(project_root: Path) -> None:
    leaks: list[str] = []
    for plugin_dir in PLUGIN_DIRS:
        d = project_root / plugin_dir
        if not d.exists():
            continue
        for path in d.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in {".md", ".yaml", ".yml", ".json", ".py"}:
                continue
            rel = str(path.relative_to(project_root))
            if rel in WORKSPACE_REF_ALLOWLIST:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            for pattern in LEAK_PATTERNS:
                if pattern in content:
                    leaks.append(f"{rel}: contains '{pattern}'")
    assert not leaks, "Plugin files reference workspace paths:\n" + "\n".join(leaks)
