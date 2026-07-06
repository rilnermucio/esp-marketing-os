#!/usr/bin/env python3
"""
Testes para memory_writer.py — persistência append-only na memory opt-in.
"""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import init_agent_memory as iam
import memory_writer as mw


@pytest.fixture
def tmp_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(iam, "MEMORY_ROOT", Path(".claude/agent-memory"))
    monkeypatch.setattr(mw, "MEMORY_ROOT", Path(".claude/agent-memory"))
    return tmp_path


def _bootstrap_agent(tmp_cwd, agent: str) -> Path:
    iam.init_memory(force=False, check_only=False)
    return tmp_cwd / ".claude" / "agent-memory" / agent / "MEMORY.md"


class TestAppendLearning:
    def test_primeira_escrita_cria_secao_aprendizados(self, tmp_cwd):
        agent = iam.AGENTS_WITH_MEMORY[0]
        _bootstrap_agent(tmp_cwd, agent)

        ok = mw.append_learning(
            agent,
            "resultado",
            "Hook com pergunta direta reteve melhor",
            "/aprender teste",
            data="2026-07-01",
        )
        assert ok is True
        content = _bootstrap_agent(tmp_cwd, agent).read_text(encoding="utf-8")
        assert mw.LEARNING_SECTION in content
        assert "[2026-07-01] [resultado]" in content

    def test_idempotencia_nao_duplica(self, tmp_cwd):
        agent = iam.AGENTS_WITH_MEMORY[1]
        _bootstrap_agent(tmp_cwd, agent)
        texto = "Subject line com número específico abriu mais"

        assert mw.append_learning(agent, "pattern", texto, "fonte-a", data="2026-07-02")
        assert (
            mw.append_learning(agent, "pattern", texto, "fonte-b", data="2026-07-03")
            is False
        )

        content = _bootstrap_agent(tmp_cwd, agent).read_text(encoding="utf-8")
        assert content.count(texto) == 1

    def test_categoria_invalida_recusada(self, tmp_cwd):
        agent = iam.AGENTS_WITH_MEMORY[0]
        _bootstrap_agent(tmp_cwd, agent)
        ok = mw.append_learning(agent, "insight", "texto válido", "fonte")
        assert ok is False

    def test_texto_acima_400_chars_recusado(self, tmp_cwd):
        agent = iam.AGENTS_WITH_MEMORY[0]
        _bootstrap_agent(tmp_cwd, agent)
        long_text = "a" * 401
        ok = mw.append_learning(agent, "resultado", long_text, "fonte")
        assert ok is False

    def test_agent_fora_da_lista_erro_claro(self, tmp_cwd, capsys):
        ok = mw.append_learning("mos-fantasma", "resultado", "x", "fonte")
        err = capsys.readouterr().err
        assert ok is False
        assert "mos-fantasma" in err
        assert "não tem memory opt-in" in err

    def test_limite_diario_recusa_21a(self, tmp_cwd):
        agent = iam.AGENTS_WITH_MEMORY[2]
        _bootstrap_agent(tmp_cwd, agent)
        target_date = "2026-07-15"

        for i in range(mw.MAX_ENTRIES_PER_DAY):
            ok = mw.append_learning(
                agent,
                "resultado",
                f"entrada número {i}",
                f"fonte-{i}",
                data=target_date,
            )
            assert ok is True

        ok = mw.append_learning(
            agent, "resultado", "entrada número 21", "fonte-21", data=target_date
        )
        assert ok is False

    def test_memory_root_respeita_cwd(self, tmp_cwd):
        agent = iam.AGENTS_WITH_MEMORY[0]
        _bootstrap_agent(tmp_cwd, agent)
        mw.append_learning(
            agent, "voz", "Tom direto converteu melhor", "fonte", data="2026-07-04"
        )

        expected = tmp_cwd / ".claude" / "agent-memory" / agent / "MEMORY.md"
        assert expected.exists()
        assert (Path.cwd() / ".claude" / "agent-memory" / agent / "MEMORY.md").exists()


class TestCli:
    def test_cli_exit_0_quando_escreve(self, tmp_cwd, monkeypatch):
        agent = iam.AGENTS_WITH_MEMORY[0]
        _bootstrap_agent(tmp_cwd, agent)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "memory_writer.py",
                "--agent",
                agent,
                "--categoria",
                "benchmark-local",
                "--texto",
                "CTR acima da média do nicho",
                "--fonte",
                "/aprender cli",
            ],
        )
        assert mw.main() == 0

    def test_cli_exit_1_quando_recusado(self, tmp_cwd, monkeypatch):
        agent = iam.AGENTS_WITH_MEMORY[0]
        _bootstrap_agent(tmp_cwd, agent)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "memory_writer.py",
                "--agent",
                agent,
                "--categoria",
                "categoria-invalida",
                "--texto",
                "x",
                "--fonte",
                "y",
            ],
        )
        assert mw.main() == 1
