#!/usr/bin/env python3
"""
init_agent_memory.py — Cria a estrutura de memory opt-in para os agents do Marketing OS.

Cria `.claude/agent-memory/mos-<agent>/MEMORY.md` para cada agent que tem
`memory: project` no frontmatter. A pasta `.claude/` está gitignored (memory é
per-projeto, não distribuída pelo plugin).

Uso:
    python3 scripts/init_agent_memory.py              # cria os 9 diretórios + MEMORY.md placeholder
    python3 scripts/init_agent_memory.py --check      # apenas reporta o estado, não cria nada
    python3 scripts/init_agent_memory.py --force      # sobrescreve MEMORY.md existentes (cuidado)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Mantenha sincronizado com o frontmatter `memory: project` em agents/mos-*.md
# e com a seção "Memory automática" em skills/marketing-os/SKILL.md
AGENTS_WITH_MEMORY = [
    "mos-ads",
    "mos-analytics",
    "mos-brand",
    "mos-community",
    "mos-copy",
    "mos-design",
    "mos-email",
    "mos-funnel",
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

    for agent in AGENTS_WITH_MEMORY:
        agent_dir = MEMORY_ROOT / agent
        memory_file = agent_dir / "MEMORY.md"

        if check_only:
            status = "EXISTE" if memory_file.exists() else "FALTA"
            print(f"  [{status}] {memory_file}")
            continue

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
    if not (created or overwritten or skipped):
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
