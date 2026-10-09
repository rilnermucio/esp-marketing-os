"""Estado do usuário vai para o projeto onde a sessão roda, nunca para a pasta do plugin.

Auditoria 2026-09-28 (achado #5, F-DIST-03): /projeto, relatórios semanais e a
coleta de tendências do TikTok gravavam dentro da pasta do plugin, que numa
instalação real é um cache trocado a cada update e compartilhado entre projetos.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

# Diretório de saída ancorado no próprio script: o padrão que causou o achado.
STATE_NEXT_TO_SCRIPT = re.compile(
    r"(__file__|BASE_DIR|REPO_ROOT)[^\n]{0,60}[\"'](output|outputs|workspace|reports)[\"'/]"
)


def test_user_workspace_follows_session_directory(tmp_path, monkeypatch):
    import workspace_paths

    monkeypatch.delenv("MOS_WORKSPACE", raising=False)
    monkeypatch.chdir(tmp_path)
    assert workspace_paths.user_workspace() == tmp_path / "workspace"


def test_user_workspace_override(tmp_path, monkeypatch):
    import workspace_paths

    monkeypatch.setenv("MOS_WORKSPACE", str(tmp_path / "custom"))
    assert workspace_paths.user_workspace() == tmp_path / "custom"


@pytest.mark.parametrize(
    "module,attribute",
    [
        ("project_manager", "PROJECTS_ROOT"),
        ("weekly_report", "OUTPUT_DIR"),
    ],
)
def test_state_dirs_live_outside_plugin(tmp_path, monkeypatch, module, attribute):
    monkeypatch.delenv("MOS_WORKSPACE", raising=False)
    monkeypatch.chdir(tmp_path)
    mod = importlib.reload(importlib.import_module(module))
    state_dir = Path(getattr(mod, attribute)).resolve()
    assert tmp_path.resolve() in state_dir.parents
    assert ROOT not in state_dir.parents


def test_no_script_writes_state_next_to_itself():
    offenders = []
    for path in sorted(SCRIPTS.glob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if STATE_NEXT_TO_SCRIPT.search(line):
                offenders.append(f"{path.name}:{number}: {line.strip()}")
    assert (
        not offenders
    ), "Estado do usuário ancorado na pasta do plugin:\n" + "\n".join(offenders)
