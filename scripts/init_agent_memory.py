#!/usr/bin/env python3
"""
init_agent_memory.py: prepara a memória de projeto dos agents do Marketing OS.

Cria `.claude/agent-memory/marketing-os-mos-<agent>/MEMORY.md` para cada agent
com `memory: project` no frontmatter. Esse é o diretório nativo que o Claude
Code usa para agent de plugin (`<plugin>-<agent>`): a plataforma injeta o
início do MEMORY.md no contexto do agent. Até 2026-09 o plugin usava
`.claude/agent-memory/mos-<agent>/`, que a plataforma não lê para agent de
plugin; esses diretórios antigos são migrados sem perda (ADR-0006).

Uso:
    python3 scripts/init_agent_memory.py              # migra o legado e cria os diretórios
    python3 scripts/init_agent_memory.py --check      # apenas reporta o estado, não cria nada
    python3 scripts/init_agent_memory.py --force      # sobrescreve MEMORY.md existentes (cuidado)
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

# Mantenha sincronizado com o frontmatter `memory: project` em agents/mos-*.md
# e com a seção "Memory automática" em skills/marketing-os/SKILL.md
AGENTS_WITH_MEMORY = [
    "mos-ab-testing",
    "mos-ads",
    "mos-ai-tools",
    "mos-analytics",
    "mos-audio",
    "mos-brand",
    "mos-community",
    "mos-copy",
    "mos-design",
    "mos-email",
    "mos-funnel",
    "mos-growth",
    "mos-infoproduct",
    "mos-launch",
    "mos-offer",
    "mos-partnerships",
    "mos-research",
    "mos-seo",
    "mos-social",
    "mos-storytelling",
    "mos-video",
]

MEMORY_ROOT = Path(".claude/agent-memory")
PLUGIN_NAME = "marketing-os"
MIGRATED_SUFFIX = ".migrado"


def short_agent_name(agent: str) -> str:
    """`marketing-os:mos-copy` ou `mos-copy` -> `mos-copy`."""
    return agent.rpartition(":")[2]


def memory_dir_name(agent: str) -> str:
    """Nome do diretório nativo de memória de agent de plugin: `<plugin>-<agent>`."""
    return f"{PLUGIN_NAME}-{short_agent_name(agent)}"


def memory_dir(agent: str) -> Path:
    return MEMORY_ROOT / memory_dir_name(agent)


def legacy_memory_dir(agent: str) -> Path:
    """Diretório usado pelo plugin até 2026-09, que a plataforma não lê."""
    return MEMORY_ROOT / short_agent_name(agent)


def migrate_legacy(agent: str, today: str | None = None) -> str:
    """Leva a memória antiga para o diretório nativo sem perder conteúdo.

    Retorna "movido" (só existia o antigo), "mesclado" (existiam os dois: o
    conteúdo antigo é anexado ao nativo e o antigo vira `<nome>.migrado`) ou ""
    quando não há o que migrar.
    """
    legacy = legacy_memory_dir(agent)
    target = memory_dir(agent)
    if not legacy.is_dir() or legacy == target:
        return ""
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        legacy.rename(target)
        return "movido"
    legacy_memory = legacy / "MEMORY.md"
    if legacy_memory.exists():
        stamp = today or date.today().isoformat()
        old = legacy_memory.read_text(encoding="utf-8").strip()
        target_memory = target / "MEMORY.md"
        current = (
            target_memory.read_text(encoding="utf-8") if target_memory.exists() else ""
        )
        merged = (
            current.rstrip()
            + f"\n\n## Migrado de {legacy.as_posix()} ({stamp})\n\n"
            + old
            + "\n"
        )
        target_memory.write_text(merged.lstrip(), encoding="utf-8")
    parked = legacy.with_name(legacy.name + MIGRATED_SUFFIX)
    counter = 1
    while parked.exists():
        counter += 1
        parked = legacy.with_name(f"{legacy.name}{MIGRATED_SUFFIX}{counter}")
    legacy.rename(parked)
    return "mesclado"


PLACEHOLDER_TEMPLATE = """# {agent} — Memory

Este arquivo persiste aprendizados não-óbvios entre sessões para o agent `{agent}`.
Ele é carregado automaticamente quando o agent roda neste projeto.

Cada agent define no seu próprio system prompt (em `agents/{agent}.md`, seção
"Atualize a Memory ao final") o que deve ser salvo aqui e o que NÃO deve.

Regra geral: salve patterns transferíveis (o que funcionou/não funcionou e por
quê), não o conteúdo gerado em si (esse vai pra git/output).

---

(vazio — preenchido pelos agents conforme rodam)
"""


def init_memory(force: bool = False, check_only: bool = False) -> int:
    """Cria a estrutura. Retorna exit code (0 ok, 1 erro)."""
    if not check_only:
        MEMORY_ROOT.mkdir(parents=True, exist_ok=True)

    created = []
    skipped = []
    overwritten = []
    migrated = []

    for agent in AGENTS_WITH_MEMORY:
        agent_dir = memory_dir(agent)
        memory_file = agent_dir / "MEMORY.md"

        if check_only:
            status = "EXISTE" if memory_file.exists() else "FALTA"
            legacy = legacy_memory_dir(agent)
            extra = f"  (legado a migrar: {legacy})" if legacy.is_dir() else ""
            print(f"  [{status}] {memory_file}{extra}")
            continue

        outcome = migrate_legacy(agent)
        if outcome:
            migrated.append((legacy_memory_dir(agent), outcome))

        agent_dir.mkdir(parents=True, exist_ok=True)

        if memory_file.exists() and not force:
            skipped.append(memory_file)
            continue

        if memory_file.exists() and force:
            overwritten.append(memory_file)
        else:
            created.append(memory_file)

        memory_file.write_text(
            PLACEHOLDER_TEMPLATE.format(agent=agent),
            encoding="utf-8",
        )

    if check_only:
        print(f"\nTotal esperado: {len(AGENTS_WITH_MEMORY)} arquivos em {MEMORY_ROOT}/")
        return 0

    print(f"\nMemory bootstrap concluído em {MEMORY_ROOT}/")
    if migrated:
        print(f"  Legado migrado: {len(migrated)}")
        for p, outcome in migrated:
            print(f"    > {p} ({outcome})")
    if created:
        print(f"  Criados: {len(created)}")
        for p in created:
            print(f"    + {p}")
    if overwritten:
        print(f"  Sobrescritos (--force): {len(overwritten)}")
        for p in overwritten:
            print(f"    ! {p}")
    if skipped:
        print(f"  Já existiam (preservados): {len(skipped)}")
        for p in skipped:
            print(f"    = {p}")
    if not (created or overwritten or skipped or migrated):
        print("  (nada a fazer)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap da memory opt-in dos agents Marketing OS",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Apenas reporta o estado, não cria nada",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve MEMORY.md existentes (perde conteúdo acumulado!)",
    )
    args = parser.parse_args()

    if args.check and args.force:
        print("ERRO: --check e --force são mutuamente exclusivos", file=sys.stderr)
        return 2

    return init_memory(force=args.force, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
