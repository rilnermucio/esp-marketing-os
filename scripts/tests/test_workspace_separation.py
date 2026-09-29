"""Validates plugin code does not reference workspace/ paths and that personal files never ship."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


PLUGIN_DIRS = ["skills", "subagents", "commands", "workflows", "assets", "references", "agents"]
LEAK_PATTERNS = ["workspace/", "../workspace", "/workspace/"]
# Files that legitimately reference workspace/ by design (e.g. commands that read user-local samples)
WORKSPACE_REF_ALLOWLIST = {
    "commands/criar-meu-clone.md",
    "commands/auditoria.md",  # writes audit output (RELATORIO.md/pdf) to workspace/auditorias/<run>/
    "commands/auditoria-pro.md",  # writes premium audit (RELATORIO.html/pdf + screenshots/charts) to workspace/auditorias/<run>-pro/
    "commands/projeto.md",  # manages user-side projects in workspace/projects/<slug>/
    "skills/marketing-os/SKILL.md",  # documents that /criar-meu-clone reads from workspace/
    "agents/mos-copy.md",  # swipe file pessoal: lê/escreve winners em workspace/swipe-files/aprovados.md
    "agents/mos-ads.md",  # swipe file pessoal: lê/escreve criativos vencedores em workspace/swipe-files/ads-aprovados.md
    "agents/mos-offer.md",  # swipe file pessoal: lê/escreve ofertas aprovadas em workspace/swipe-files/ofertas-aprovadas.md
    "subagents/copy-agent.md",  # documenta o loop de swipe-files vivos (trilho 1 em workspace/)
    "commands/otimizar-copy.md",  # aponta winners do teste pro swipe file pessoal em workspace/
    "commands/renderizar-imagem.md",  # salva PNGs gerados em workspace/media/imagens/
    "commands/gerar-thumbnail.md",  # salva fundo+thumb em workspace/media/thumbnails/
    "commands/produzir-reels.md",  # pipeline de áudio/composição/vídeo em workspace/media/reels/
    "commands/aprender.md",  # lê exports de métricas do usuário em workspace/ antes do metrics_collector
}


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


# Formatos típicos de material de cliente. A fonte do marketplace é a raiz do
# repo, então qualquer arquivo rastreado é distribuído em toda instalação.
OFFICE_EXTENSIONS = {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".key", ".numbers", ".pages", ".odt", ".ods"}
# Exceções deliberadas, com justificativa. Vazio por padrão.
OFFICE_FILE_ALLOWLIST: set[str] = set()


def _tracked_files(project_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(project_root), "ls-files", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip("fora de um checkout git (ex: cache de instalação do plugin)")
    return [p for p in result.stdout.decode("utf-8").split("\0") if p]


def test_workspace_tracks_only_gitkeep(project_root: Path) -> None:
    """Invariante real do workspace: só .gitkeep é versionado.

    Adicionar uma regra ao .gitignore não remove do índice um arquivo que já
    estava rastreado. Foi assim que 3 .docx de cliente ficaram no repo público
    de 2026-05-06 a 2026-09-28 (auditoria 2026-09-28, achado #1).
    """
    tracked = [p for p in _tracked_files(project_root) if p.startswith("workspace/")]
    personal = [p for p in tracked if not p.endswith(".gitkeep")]
    assert not personal, (
        "Arquivos pessoais rastreados em workspace/ (rode `git rm --cached <arquivo>`):\n"
        + "\n".join(personal)
    )


def test_no_office_documents_tracked(project_root: Path) -> None:
    offenders = [
        p
        for p in _tracked_files(project_root)
        if Path(p).suffix.lower() in OFFICE_EXTENSIONS and p not in OFFICE_FILE_ALLOWLIST
    ]
    assert not offenders, (
        "Documentos de escritório versionados (provável material de cliente):\n"
        + "\n".join(offenders)
    )
