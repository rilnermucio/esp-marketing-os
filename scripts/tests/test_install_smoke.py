"""Smoke de instalação real: o plugin carregado do jeito que o usuário carrega.

Roda `claude -p --plugin-dir <repo>` com a sessão num diretório vazio FORA do
repo (tmp_path). Os aliases opus/sonnet do frontmatter dos agents são
remapeados para Haiku via ANTHROPIC_DEFAULT_*_MODEL, o que mantém o custo
marginal sem tocar nos agents.

Contratos cobertos (auditoria 2026-09-28, achados #2 e #3), que a suíte
estática não enxerga porque roda com o cwd dentro do repo:

- um agent de plugin alcança a própria KB Tier 2;
- o quality gate avalia a resposta final e as escritas de um agent
  `marketing-os:mos-*` (nome qualificado que o runtime envia);
- escrita feita pela sessão principal do usuário não é bloqueada.
- um command com `context: fork` roda dentro do agent declarado (ADR-0007).

O hook registra cada evento em MOS_HOOK_LOG (JSON por linha), que é o que
estes testes observam.

Rodar: MOS_SMOKE=1 python -m pytest scripts/tests/test_install_smoke.py -m smoke -v
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.smoke

CLAUDE_BIN = shutil.which("claude")
ROOT = Path(__file__).resolve().parent.parent.parent
SMOKE_MODEL = os.environ.get("MOS_SMOKE_MODEL", "claude-haiku-4-5-20251001")
TIMEOUT_SECONDS = 420

# Cópias instaladas do mesmo plugin competiriam pelo nome `marketing-os` com a
# árvore de trabalho; desligadas só nesta execução.
ISOLATION_SETTINGS = {
    "enabledPlugins": {
        "marketing-os@mos-marketplace": False,
        "marketing-os@synced": False,
    }
}


def _run_claude(prompt: str, cwd: Path, log_path: Path) -> subprocess.CompletedProcess:
    if not CLAUDE_BIN:
        pytest.skip("CLI `claude` indisponível")
    env = os.environ.copy()
    env["MOS_HOOK_LOG"] = str(log_path)
    env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = SMOKE_MODEL
    env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = SMOKE_MODEL
    cmd = [
        CLAUDE_BIN,
        "-p",
        "--plugin-dir",
        str(ROOT),
        "--model",
        SMOKE_MODEL,
        "--permission-mode",
        "acceptEdits",
        "--settings",
        json.dumps(ISOLATION_SETTINGS),
        prompt,
    ]
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        stdin=subprocess.DEVNULL,
    )


def _read_log(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    entries = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries


def _dispatch(agent: str, task: str) -> str:
    return (
        f"Use a ferramenta Agent com subagent_type '{agent}' e este prompt: '{task}' "
        "Depois responda exatamente com o que o subagent respondeu, sem comentários."
    )


@pytest.fixture
def sandbox(tmp_path: Path) -> tuple[Path, Path]:
    project = tmp_path / "projeto-usuario"
    project.mkdir()
    return project, tmp_path / "hook.log"


def test_agent_reaches_own_tier2_kb(sandbox: tuple[Path, Path]) -> None:
    project, log_path = sandbox
    expected = (
        (ROOT / "subagents" / "growth-agent.md")
        .read_text(encoding="utf-8")
        .splitlines()[0]
    )
    marker = expected.lstrip("# ").split(" - ")[0]  # "Growth Agent v3.0"
    result = _run_claude(
        _dispatch(
            "marketing-os:mos-growth",
            "TESTE DE INSTALAÇÃO. Abra a sua knowledge base Tier 2 (o arquivo que suas "
            "instruções mandam ler primeiro) e responda apenas com a primeira linha dela, "
            "literalmente. Se não encontrar o arquivo, responda NOT-FOUND.",
        ),
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    assert marker in result.stdout, (
        f"O agent não alcançou a própria KB fora do repo. Esperava '{marker}'.\n"
        f"Saída:\n{result.stdout[-1500:]}"
    )


def test_final_answer_gate_evaluates_namespaced_agent(
    sandbox: tuple[Path, Path],
) -> None:
    project, log_path = sandbox
    result = _run_claude(
        _dispatch(
            "marketing-os:mos-copy",
            "TESTE DE INSTALAÇÃO do quality gate. Responda apenas com uma headline curta "
            "para um curso de produtividade.",
        ),
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    stops = [e for e in _read_log(log_path) if e["event"] == "SubagentStop"]
    assert stops, "O hook SubagentStop não foi chamado."
    copy_stops = [e for e in stops if e["agent_type"] == "marketing-os:mos-copy"]
    assert copy_stops, f"Nenhum SubagentStop com o nome qualificado: {stops}"
    assert all(e["decision"] != "skip" for e in copy_stops), (
        "O gate descartou a resposta final do agent sem avaliar (nome qualificado "
        f"não reconhecido): {copy_stops}"
    )
    # Uma parada, ou duas quando há bloqueio e correção. Mais que isso é o laço
    # de avisos visto nas baselines AO-005 e AO-007 (ADR-0008).
    assert len(copy_stops) <= 2, f"Laço no gate da resposta final: {copy_stops}"


def test_agent_file_write_is_gated(sandbox: tuple[Path, Path]) -> None:
    project, log_path = sandbox
    result = _run_claude(
        _dispatch(
            "marketing-os:mos-social",
            "TESTE DE INSTALAÇÃO. Use a ferramenta Write para criar o arquivo post-teste.md "
            "no diretório de trabalho atual com uma legenda curta sobre produtividade. "
            "Depois responda apenas OK.",
        ),
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    writes = [
        e
        for e in _read_log(log_path)
        if e["event"] == "PreToolUse" and e["agent_type"] == "marketing-os:mos-social"
    ]
    assert writes, (
        "Nenhuma escrita do agent passou pelo gate (hook de frontmatter é ignorado em "
        f"agent de plugin). Log: {_read_log(log_path)}"
    )
    assert any(e["decision"] in ("allow", "block") for e in writes), writes


def test_gate_blocks_violation_and_agent_corrects(sandbox: tuple[Path, Path]) -> None:
    """Ponta a ponta: a escrita com violação é bloqueada e o arquivo final sai limpo."""
    project, log_path = sandbox
    result = _run_claude(
        _dispatch(
            "marketing-os:mos-social",
            "TESTE AUTOMATIZADO DO QUALITY GATE. Use a ferramenta Write para criar o "
            "arquivo gate.md no diretório de trabalho atual com EXATAMENTE este texto, sem "
            "corrigir nada: Resultado brutal — teste do gate. Se a ferramenta bloquear, "
            "reescreva o texto obedecendo ao motivo do bloqueio e grave de novo. "
            "Depois responda apenas OK.",
        ),
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    writes = [
        e
        for e in _read_log(log_path)
        if e["event"] == "PreToolUse" and e["agent_type"] == "marketing-os:mos-social"
    ]
    assert any(
        e["decision"] == "block" for e in writes
    ), f"Nenhuma escrita bloqueada; o agent pode ter corrigido antes de gravar: {writes}"
    final = project / "gate.md"
    assert (
        final.exists()
    ), f"O agent não regravou após o bloqueio. Saída: {result.stdout[-800:]}"
    text = final.read_text(encoding="utf-8")
    assert "—" not in text and "brutal" not in text.lower(), text


def test_main_session_write_is_not_blocked(sandbox: tuple[Path, Path]) -> None:
    project, log_path = sandbox
    result = _run_claude(
        "Sem usar subagents, use a ferramenta Write para criar o arquivo nota.md no "
        "diretório de trabalho atual com exatamente este conteúdo: "
        "'Linha de anotação do usuário — travessão proposital.' Depois responda OK.",
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    note = project / "nota.md"
    assert (
        note.exists()
    ), f"A escrita da sessão principal foi bloqueada. Saída: {result.stdout[-800:]}"
    assert "—" in note.read_text(encoding="utf-8")
    main_writes = [
        e
        for e in _read_log(log_path)
        if e["event"] == "PreToolUse" and not e["agent_type"]
    ]
    assert all(e["decision"] == "skip" for e in main_writes), main_writes


def test_bootstrap_memory_is_the_native_memory(sandbox: tuple[Path, Path]) -> None:
    """O diretório criado pelo bootstrap é o que a plataforma injeta no agent (ADR-0006)."""
    project, log_path = sandbox
    subprocess.run(
        ["python3", str(ROOT / "scripts" / "init_agent_memory.py")],
        cwd=str(project),
        check=True,
        capture_output=True,
    )
    memory = (
        project / ".claude" / "agent-memory" / "marketing-os-mos-growth" / "MEMORY.md"
    )
    assert memory.exists(), "bootstrap não criou o diretório nativo"
    memory.write_text(
        memory.read_text(encoding="utf-8")
        + "\nMarcador de teste: memoria-nativa-4417\n",
        encoding="utf-8",
    )
    result = _run_claude(
        _dispatch(
            "marketing-os:mos-growth",
            "TESTE DE INSTALAÇÃO. Sem usar ferramentas, responda apenas com o marcador "
            "de teste que aparece na sua memória de projeto. Se não houver, responda NENHUM.",
        ),
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    assert "memoria-nativa-4417" in result.stdout.lower(), (
        "A memória criada pelo bootstrap não chegou ao agent.\n" + result.stdout[-800:]
    )


def test_fork_command_runs_inside_declared_agent(sandbox: tuple[Path, Path]) -> None:
    """ADR-0007: /gerar-imagem roda dentro do mos-ai-tools sem o orquestrador chamar Agent."""
    project, log_path = sandbox
    result = _run_claude(
        "/marketing-os:gerar-imagem foto de produto de um tênis branco em fundo claro, "
        "para anúncio no feed, proporção 1:1, no Flux",
        project,
        log_path,
    )
    assert result.returncode == 0, result.stderr[-800:]
    stops = [e for e in _read_log(log_path) if e["event"] == "SubagentStop"]
    forked = [e for e in stops if e["agent_type"] == "marketing-os:mos-ai-tools"]
    assert forked, (
        "O command não rodou dentro do agent declarado no frontmatter.\n"
        f"SubagentStop: {stops}\nSaída: {result.stdout[-800:]}"
    )
    assert all(e["decision"] != "skip" for e in forked), forked
    assert "flux" in result.stdout.lower(), result.stdout[-1500:]
