#!/usr/bin/env python3
"""Guard-rails que travam o drift de consistência do repo.

Estes testes convertem achados de auditoria manual (contagens erradas, badge de
versão defasado, travessão em conteúdo distribuído, regressão de manifesto) em
falha de CI. Se você adicionar um agent/command/clone, atualize os docs ou estes
testes apontam exatamente o que ficou inconsistente.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS = sorted((ROOT / "agents").glob("mos-*.md"))
COMMANDS = sorted((ROOT / "commands").glob("*.md"))
CLONES = [d for d in (ROOT / "assets" / "clones").iterdir() if d.is_dir()]
CONFORMING_CLONES = [d for d in CLONES if (d / "profile.md").exists()]
SUBAGENTS = sorted((ROOT / "subagents").glob("*-agent.md"))

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
            assert (
                int(m.group(1)) == real
            ), f"README diz '{m.group(0)}' mas o real é {real} {noun}"


# Guard consciente: mudar este número exige atualizar contagens em README,
# AGENTS.md, SKILL.md e manifests (tabela de sincronia no MAINTAINER-HANDBOOK).
EXPECTED_AGENT_COUNT = 21  # 20º: mos-community, 21º: mos-partnerships (jul/2026)


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
    assert non_conforming == [
        "design"
    ], f"clones fora do padrão inesperados: {non_conforming}"


_CLONE_INVENTORY_PATTERNS = (
    re.compile(
        r"(?:Inventário Completo dos|sistema de|tem acesso a|paralelo aos)\s+"
        r"\**(?P<count>\d+)\s+(?:voice\s+)?clones?",
        re.I,
    ),
    re.compile(
        r"(?:voice\s+)?clones?[^\d\n]{0,80}(?P<count>\d+)\s+disponíveis",
        re.I,
    ),
    re.compile(
        r"(?P<count>\d+)\s+(?:voice\s+)?clones?\**\s+"
        r"(?:disponíveis|profundos|wired)",
        re.I,
    ),
    # Inventário em docs de usuário (auditoria 2026-09-28: "35 perfis" escapou).
    re.compile(
        r"(?P<count>\d+)\s+perfis\s+(?:de\s+copywriters|disponíveis|em\s+\W?assets/clones)",
        re.I,
    ),
    re.compile(r"(?P<count>\d+)\s+(?:voice\s+clones|clones\s+de\s+voz)\b", re.I),
)

# Documentos vivos que citam o inventário. Histórico (worklogs, CHANGELOG,
# planos arquivados) registra o que era verdade na época e fica de fora.
_HISTORICAL = ("docs/ai-engineering/worklogs/", "docs/superpowers/", "docs/archive/")
LIVE_DOCS = sorted(
    p
    for p in ROOT.rglob("*.md")
    if not any(
        part in {"plugins", "workspace", ".git", "node_modules"}
        for part in p.relative_to(ROOT).parts
    )
    and not str(p.relative_to(ROOT)).startswith(_HISTORICAL)
    and p.name != "CHANGELOG.md"
)


def test_clone_inventory_claims_match_filesystem():
    """Inventory totals in distributed prompts must follow the real clone count."""
    real = len(CONFORMING_CLONES)
    mismatches = []
    for path in LIVE_DOCS:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            for pattern in _CLONE_INVENTORY_PATTERNS:
                match = pattern.search(line)
                if match and int(match.group("count")) != real:
                    mismatches.append(
                        f"{path.relative_to(ROOT)}:{line_number} diz "
                        f"{match.group('count')}, real {real}"
                    )
                    break
    assert not mismatches, "contagens de clones divergentes:\n" + "\n".join(mismatches)


def test_agent_smoke_matrix_covers_every_native_agent():
    """Every Tier 1 agent needs an explicit external-runtime smoke scenario."""
    path = ROOT / "scripts" / "tests" / "test_agents_smoke.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    matrix = None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "REPRESENTATIVE_AGENTS"
            for target in node.targets
        ):
            matrix = ast.literal_eval(node.value)
            break
    assert matrix is not None, "REPRESENTATIVE_AGENTS não encontrado"
    covered = {row[0] for row in matrix}
    expected = {path.stem for path in AGENTS}
    assert covered == expected, f"matriz smoke divergente: {covered ^ expected}"


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
    assert m.get("version") and m.get(
        "description"
    ), "use version/description top-level"
    src = m["plugins"][0]["source"]
    assert src.startswith("./"), f"source deve começar com ./ (achei {src!r})"


def test_project_manager_runtime_dependency_is_declared():
    """O /projeto precisa funcionar após o install documentado do requirements."""
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
    declared = {
        re.match(r"[a-z0-9_.-]+", line.split("#", 1)[0].strip()).group(0)
        for line in requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert "pyyaml" in declared, (
        "project_manager.py importa yaml no startup; PyYAML precisa estar em "
        "requirements.txt para /projeto e a suite funcionarem em ambiente limpo"
    )


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
    missing = [
        a.name for a in AGENTS if not _RULE.search(a.read_text(encoding="utf-8"))
    ]
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
