#!/usr/bin/env python3
"""Guard-rails que travam o drift de consistência do repo.

Estes testes convertem achados de auditoria manual (contagens erradas, badge de
versão defasado, travessão em conteúdo distribuído, regressão de manifesto) em
falha de CI. Se você adicionar um agent/command/clone, atualize os docs ou estes
testes apontam exatamente o que ficou inconsistente.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS = sorted((ROOT / "agents").glob("mos-*.md"))
COMMANDS = sorted((ROOT / "commands").glob("*.md"))
CLONES = [d for d in (ROOT / "assets" / "clones").iterdir() if d.is_dir()]
CONFORMING_CLONES = [d for d in CLONES if (d / "profile.md").exists()]

# Linhas que DEFINEM a regra do travessão (mostram o caractere de propósito).
_RULE = re.compile(r"travess|em[- ]dash|`—`|quality gate|gates? univers", re.I)


def _load(name: str) -> dict:
    return json.loads((ROOT / ".claude-plugin" / name).read_text(encoding="utf-8"))


# --------------------------------------------------------------- versão
def test_version_is_consistent_across_manifests_and_readme():
    plugin = _load("plugin.json")
    market = _load("marketplace.json")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    badge = re.search(r"version-(\d+\.\d+\.\d+)-", readme)
    assert badge, "badge de versão não encontrado no README"

    versions = {
        "plugin.json": plugin["version"],
        "marketplace.json (top)": market["version"],
        "marketplace.json (plugin)": market["plugins"][0]["version"],
        "README badge": badge.group(1),
    }
    assert len(set(versions.values())) == 1, f"versões divergentes: {versions}"


# --------------------------------------------------------------- contagens
def test_readme_counts_match_filesystem():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    expected = {
        "subagentes": len(AGENTS),
        "slash commands": len(COMMANDS),
        "voice clones": len(CONFORMING_CLONES),
    }
    for noun, real in expected.items():
        for m in re.finditer(rf"(\d+)\s+{re.escape(noun)}", readme):
            assert int(m.group(1)) == real, (
                f"README diz '{m.group(0)}' mas o real é {real} {noun}"
            )


# Guard consciente: mudar este número exige atualizar contagens em README,
# AGENTS.md, SKILL.md e manifests (tabela de sincronia no MAINTAINER-HANDBOOK).
EXPECTED_AGENT_COUNT = 19  # 19º: mos-offer (jul/2026)


def test_agents_count_matches_expected():
    assert len(AGENTS) == EXPECTED_AGENT_COUNT, (
        f"agents/mos-*.md tem {len(AGENTS)} arquivos, esperado {EXPECTED_AGENT_COUNT}. "
        "Adicionou/removeu agent? Atualize EXPECTED_AGENT_COUNT e as contagens dos docs."
    )


def test_every_agent_references_an_existing_tier2_file():
    # Cada agent cita seu Tier-2 como `subagents/<algo>-agent.md`. O nome nem sempre
    # segue strip-prefix (ex: mos-infoproduct -> infoproduct-builder-agent.md), então
    # validamos a referência real, não um nome adivinhado.
    broken = []
    for a in AGENTS:
        body = a.read_text(encoding="utf-8")
        refs = re.findall(r"subagents/([\w-]+-agent\.md)", body)
        if not refs:
            broken.append(f"{a.name}: nenhuma referência a Tier-2")
            continue
        for ref in set(refs):
            if not (ROOT / "subagents" / ref).exists():
                broken.append(f"{a.name} -> subagents/{ref} (inexistente)")
    assert not broken, f"referências Tier-2 quebradas: {broken}"


def test_all_clone_dirs_conform_or_are_documented_exception():
    # 34 clones conformes + 'design' (design-dna-system.md) como exceção conhecida.
    non_conforming = [d.name for d in CLONES if d not in CONFORMING_CLONES]
    assert non_conforming == ["design"], (
        f"clones fora do padrão inesperados: {non_conforming}"
    )


# --------------------------------------------------------------- manifesto
def test_plugin_manifest_distribution_rules():
    """Trava as regras que quebraram install em v6.1.0-v6.1.6 (ver AGENTS.md)."""
    p = _load("plugin.json")
    assert isinstance(p.get("author"), dict), "author deve ser objeto, não string"
    assert isinstance(p.get("category"), str), "category deve ser singular (string)"
    assert "skills" not in p, "não declarar 'skills' (default discovery cobre)"
    assert p.get("version"), "version ausente"


def test_marketplace_manifest_rules():
    m = _load("marketplace.json")
    assert m.get("version") and m.get("description"), "use version/description top-level"
    src = m["plugins"][0]["source"]
    assert src.startswith("./"), f"source deve começar com ./ (achei {src!r})"


# --------------------------------------------------------------- quality gate
def test_memory_agents_match_init_script():
    # Trava o drift que o comentário de init_agent_memory.py avisa: o set de agents
    # com `memory: project` no frontmatter tem que bater com AGENTS_WITH_MEMORY.
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    import init_agent_memory as iam

    declared = {
        a.stem
        for a in AGENTS
        if re.search(r"^memory:\s*project\s*$", a.read_text(encoding="utf-8"), re.M)
    }
    listed = set(iam.AGENTS_WITH_MEMORY)
    assert declared == listed, f"frontmatter memory != init list: {declared ^ listed}"


def test_every_agent_declares_the_emdash_gate():
    missing = [a.name for a in AGENTS if not _RULE.search(a.read_text(encoding="utf-8"))]
    assert not missing, f"agents sem o quality gate do travessão: {missing}"


# --------------------------------------------------------------- travessão
def _emdash_violations(path: Path) -> list[int]:
    out, infence = [], False
    for i, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if ln.lstrip().startswith("```"):
            infence = not infence
            continue
        if infence or "—" not in ln:
            continue
        if ln.lstrip().startswith(">") or _RULE.search(ln):
            continue
        out.append(i)
    return out


@pytest.mark.parametrize("path", AGENTS + COMMANDS, ids=lambda p: p.name)
def test_no_emdash_in_distributed_prose(path: Path):
    bad = _emdash_violations(path)
    assert not bad, f"travessão fora de regra/código em {path.name}: linhas {bad}"
