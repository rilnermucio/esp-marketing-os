#!/usr/bin/env python3
"""
Testes para init_agent_memory.py — bootstrap da memory opt-in dos agents.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import init_agent_memory as iam


# --------------------------------------------------------------------- helpers
@pytest.fixture
def tmp_cwd(tmp_path, monkeypatch):
    """Roda o script com cwd em diretório temporário (evita sujar repo real)."""
    monkeypatch.chdir(tmp_path)
    # Reaponta MEMORY_ROOT pra dentro do tmp_path (Path relativo respeita cwd)
    monkeypatch.setattr(iam, "MEMORY_ROOT", Path(".claude/agent-memory"))
    return tmp_path


# --------------------------------------------------------------------- estado
def test_lista_agents_com_memory_nao_esta_vazia():
    assert len(iam.AGENTS_WITH_MEMORY) >= 1
    assert all(name.startswith("mos-") for name in iam.AGENTS_WITH_MEMORY)


def test_template_memory_tem_placeholder_agent():
    assert "{agent}" in iam.PLACEHOLDER_TEMPLATE


def test_memory_root_eh_path_relativo():
    # MEMORY_ROOT padrão deve apontar para .claude/agent-memory (gitignored)
    assert ".claude" in str(iam.MEMORY_ROOT)


# ------------------------------------------------------- init_memory criação
def test_init_memory_cria_estrutura_completa(tmp_cwd):
    rc = iam.init_memory(force=False, check_only=False)
    assert rc == 0

    for agent in iam.AGENTS_WITH_MEMORY:
        memory_file = (
            tmp_cwd / ".claude" / "agent-memory" / f"marketing-os-{agent}" / "MEMORY.md"
        )
        assert memory_file.exists(), f"MEMORY.md não criado para {agent}"
        content = memory_file.read_text(encoding="utf-8")
        assert agent in content, f"Nome do agent não substituído em {memory_file}"


def test_init_memory_idempotente(tmp_cwd):
    """Rodar 2x não estoura nada e preserva conteúdo customizado."""
    iam.init_memory(force=False, check_only=False)

    # Customiza um arquivo
    target = (
        tmp_cwd
        / ".claude"
        / "agent-memory"
        / f"marketing-os-{iam.AGENTS_WITH_MEMORY[0]}"
        / "MEMORY.md"
    )
    custom = "# Conteúdo customizado importante\nNão pode ser perdido"
    target.write_text(custom, encoding="utf-8")

    rc = iam.init_memory(force=False, check_only=False)
    assert rc == 0
    assert (
        target.read_text(encoding="utf-8") == custom
    ), "Conteúdo customizado foi sobrescrito sem --force"


def test_init_memory_force_sobrescreve(tmp_cwd):
    iam.init_memory(force=False, check_only=False)
    target = (
        tmp_cwd
        / ".claude"
        / "agent-memory"
        / f"marketing-os-{iam.AGENTS_WITH_MEMORY[0]}"
        / "MEMORY.md"
    )
    target.write_text("conteúdo antigo", encoding="utf-8")

    rc = iam.init_memory(force=True, check_only=False)
    assert rc == 0
    novo = target.read_text(encoding="utf-8")
    assert "conteúdo antigo" not in novo
    assert iam.AGENTS_WITH_MEMORY[0] in novo


def test_init_memory_check_only_nao_cria_nada(tmp_cwd):
    rc = iam.init_memory(force=False, check_only=True)
    assert rc == 0
    # Diretório não deve nem ter sido criado
    assert not (tmp_cwd / ".claude" / "agent-memory").exists()


def test_init_memory_check_only_reporta_existencia(tmp_cwd, capsys):
    # Cria primeiro, depois roda check
    iam.init_memory(force=False, check_only=False)
    capsys.readouterr()  # limpa stdout das criações

    rc = iam.init_memory(force=False, check_only=True)
    out = capsys.readouterr().out
    assert rc == 0
    assert "EXISTE" in out, "Modo --check deveria reportar arquivos existentes"


def test_init_memory_check_only_reporta_falta(tmp_cwd, capsys):
    rc = iam.init_memory(force=False, check_only=True)
    out = capsys.readouterr().out
    assert rc == 0
    assert "FALTA" in out, "Modo --check deveria reportar arquivos faltando"


# ------------------------------------------------------------------- main CLI
def test_main_check_e_force_sao_mutuamente_exclusivos(tmp_cwd, capsys):
    with patch.object(sys, "argv", ["init_agent_memory.py", "--check", "--force"]):
        rc = iam.main()
    err = capsys.readouterr().err
    assert rc == 2
    assert "mutuamente exclusivos" in err


def test_main_sem_args_cria_estrutura(tmp_cwd):
    with patch.object(sys, "argv", ["init_agent_memory.py"]):
        rc = iam.main()
    assert rc == 0
    assert (tmp_cwd / ".claude" / "agent-memory").exists()


def test_main_check_apenas_reporta(tmp_cwd, capsys):
    with patch.object(sys, "argv", ["init_agent_memory.py", "--check"]):
        rc = iam.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "FALTA" in out  # nada criado ainda
    assert not (tmp_cwd / ".claude" / "agent-memory").exists()


def test_main_force_sobrescreve(tmp_cwd):
    iam.init_memory(force=False, check_only=False)
    target = (
        tmp_cwd
        / ".claude"
        / "agent-memory"
        / f"marketing-os-{iam.AGENTS_WITH_MEMORY[1]}"
        / "MEMORY.md"
    )
    target.write_text("custom", encoding="utf-8")

    with patch.object(sys, "argv", ["init_agent_memory.py", "--force"]):
        rc = iam.main()
    assert rc == 0
    assert "custom" not in target.read_text(encoding="utf-8")


# -------------------------------------------------------------- integridade
def test_template_compativel_com_format(tmp_cwd):
    """Garantir que o template não tem placeholders quebrados."""
    # Precisa formatar com agent e não quebrar
    rendered = iam.PLACEHOLDER_TEMPLATE.format(agent="mos-test")
    assert "mos-test" in rendered
    assert "{" not in rendered or "}" not in rendered  # nada esquecido


def test_arquivo_resultante_eh_utf8(tmp_cwd):
    iam.init_memory(force=False, check_only=False)
    for agent in iam.AGENTS_WITH_MEMORY:
        memory_file = (
            tmp_cwd / ".claude" / "agent-memory" / f"marketing-os-{agent}" / "MEMORY.md"
        )
        # Levanta UnicodeDecodeError se não for utf-8
        memory_file.read_text(encoding="utf-8")


def test_nome_do_diretorio_nativo():
    """Padrão do Claude Code para agent de plugin: <plugin>-<agent> (sonda 2026-09-28)."""
    assert iam.memory_dir_name("mos-copy") == "marketing-os-mos-copy"
    assert iam.memory_dir_name("marketing-os:mos-copy") == "marketing-os-mos-copy"


def test_migracao_move_legado_sem_diretorio_nativo(tmp_cwd):
    legacy = tmp_cwd / ".claude" / "agent-memory" / "mos-copy"
    legacy.mkdir(parents=True)
    (legacy / "MEMORY.md").write_text("aprendizado antigo", encoding="utf-8")
    assert iam.migrate_legacy("mos-copy") == "movido"
    native = (
        tmp_cwd / ".claude" / "agent-memory" / "marketing-os-mos-copy" / "MEMORY.md"
    )
    assert native.read_text(encoding="utf-8") == "aprendizado antigo"
    assert not legacy.exists()


def test_migracao_mescla_quando_existem_os_dois_sem_apagar(tmp_cwd):
    root = tmp_cwd / ".claude" / "agent-memory"
    (root / "mos-copy").mkdir(parents=True)
    (root / "mos-copy" / "MEMORY.md").write_text("do plugin antigo", encoding="utf-8")
    (root / "marketing-os-mos-copy").mkdir(parents=True)
    (root / "marketing-os-mos-copy" / "MEMORY.md").write_text(
        "nativo", encoding="utf-8"
    )
    assert iam.migrate_legacy("mos-copy", today="2026-09-28") == "mesclado"
    merged = (root / "marketing-os-mos-copy" / "MEMORY.md").read_text(encoding="utf-8")
    assert merged.startswith("nativo")
    assert "## Migrado de .claude/agent-memory/mos-copy (2026-09-28)" in merged
    assert "do plugin antigo" in merged
    assert (root / "mos-copy.migrado" / "MEMORY.md").exists()


def test_migracao_idempotente(tmp_cwd):
    assert iam.migrate_legacy("mos-copy") == ""
    iam.init_memory(force=False, check_only=False)
    iam.init_memory(force=False, check_only=False)
    root = tmp_cwd / ".claude" / "agent-memory"
    assert not any(p.name.startswith("mos-") for p in root.iterdir())
