"""O plugin precisa funcionar com a sessão no projeto do usuário, fora do repo.

Auditoria 2026-09-28 (achado #2, F-DIST-01): agents, commands e SKILL.md
apontavam para subagents/, scripts/, assets/ etc. por caminho relativo, que só
resolve quando a sessão roda dentro do repo do plugin. E o dispatch usava o nome
curto `mos-copy`, que o runtime não resolve para agent de plugin
("Agent type 'mos-growth' not found"). Estes guards travam as duas classes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as builder  # noqa: E402

PLUGIN_DIRS = r"(?:subagents|scripts|assets|references|workflows|agents|commands|docs|skills/marketing-os)"
RELATIVE_RESOURCE = re.compile(r"(?<![\w/{}$.\-~@])" + PLUGIN_DIRS + r"/")
SHORT_DISPATCH = re.compile(r"subagent_type:\s*[\"']mos-")
ROOT_NOTE = "ficam na raiz do plugin (`${CLAUDE_PLUGIN_ROOT}`)"

PROMPTS = (
    sorted((ROOT / "agents").glob("mos-*.md"))
    + sorted((ROOT / "commands").glob("*.md"))
    + [ROOT / "skills" / "marketing-os" / "SKILL.md"]
)


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def _ids(path: Path) -> str:
    return str(path.relative_to(ROOT))


@pytest.mark.parametrize("path", PROMPTS, ids=_ids)
def test_plugin_resources_are_anchored_to_plugin_root(path: Path) -> None:
    body = _body(path)
    offenders = [
        f"linha {body[: m.start()].count(chr(10)) + 1}: {body[m.start(): m.start() + 50]!r}"
        for m in RELATIVE_RESOURCE.finditer(body)
    ]
    assert not offenders, (
        "Recurso do plugin por caminho relativo (só resolve dentro do repo). "
        "Use ${CLAUDE_PLUGIN_ROOT}/...:\n" + "\n".join(offenders[:10])
    )


@pytest.mark.parametrize("path", PROMPTS, ids=_ids)
def test_dispatch_uses_plugin_qualified_agent_name(path: Path) -> None:
    lines = [
        str(i)
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if SHORT_DISPATCH.search(line)
    ]
    assert not lines, (
        "Dispatch com nome curto não resolve em instalação real; use "
        f"subagent_type: \"marketing-os:mos-*\". Linhas: {', '.join(lines)}"
    )


@pytest.mark.parametrize("path", sorted((ROOT / "agents").glob("mos-*.md")), ids=_ids)
def test_agents_declare_plugin_root_for_kb_paths(path: Path) -> None:
    """Caminhos citados dentro das KBs (arquivos lidos, sem substituição) usam essa raiz."""
    assert ROOT_NOTE in path.read_text(encoding="utf-8")


def test_universal_package_restores_relative_paths(tmp_path: Path) -> None:
    dest = tmp_path / "marketing-os"
    builder.build_plugin(dest)
    prompts = (
        sorted((dest / "agents").glob("*.md"))
        + sorted((dest / "commands").glob("*.md"))
        + [dest / "skills" / "marketing-os" / "SKILL.md"]
    )
    leftovers = [
        p.relative_to(dest).as_posix()
        for p in prompts
        if "${CLAUDE_PLUGIN_ROOT}" in p.read_text(encoding="utf-8")
        or "marketing-os:mos-" in p.read_text(encoding="utf-8")
    ]
    assert not leftovers, leftovers
    copy_agent = (dest / "agents" / "mos-copy.md").read_text(encoding="utf-8")
    assert "`subagents/copy-agent.md`" in copy_agent
    assert "ficam na raiz do plugin, nunca no diretório do projeto" in copy_agent


def test_universal_rewrite_rules() -> None:
    sample = (
        'rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quality_gate.py" post.md` e leia '
        "`${CLAUDE_PLUGIN_ROOT}/subagents/copy-agent.md`. "
        'Agent(subagent_type: "marketing-os:mos-copy", prompt: "x")'
    )
    assert builder.adapt_for_universal(sample) == (
        "rode `python3 scripts/quality_gate.py post.md` e leia "
        "`subagents/copy-agent.md`. "
        'Agent(subagent_type: "mos-copy", prompt: "x")'
    )
