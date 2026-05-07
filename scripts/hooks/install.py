#!/usr/bin/env python3
"""
Marketing OS — Hook Installer

Adiciona o bloco `hooks:` no frontmatter de cada `agents/mos-*.md`,
ativando o quality gate automatico (Write/Edit/MultiEdit).

Idempotente: se o agent ja tem hooks, pula sem alterar.
Seguro: nao toca em nada fora de agents/mos-*.md.

Uso:
    python3 scripts/hooks/install.py

Por que esse script existe:
    O diretorio .claude/agents/ e gitignored, entao os hooks frontmatter nao
    propagam via git. Quem cria novos mos-*.md localmente deve rodar este
    script para garantir que o quality gate esteja ativo em todos.
"""
import os
import re
import sys
import glob

HOOK_BLOCK = """hooks:
  PreToolUse:
    - matcher: "Write|Edit|MultiEdit"
      hooks:
        - type: command
          command: "python3 scripts/hooks/quality_gate_hook.py"
"""

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENTS_DIR = os.path.join(PROJECT_ROOT, ".claude", "agents")


def has_hooks(frontmatter: str) -> bool:
    return bool(re.search(r"^hooks:\s*$", frontmatter, flags=re.MULTILINE))


def inject(filepath: str) -> str:
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip() != "":
        return "skip-malformed"

    fm = parts[1]
    if has_hooks(fm):
        return "skip-existing"

    body = parts[2]
    new_fm = fm.rstrip() + "\n" + HOOK_BLOCK
    new_text = "---" + new_fm + "---" + body

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_text)
    return "ok"


def main() -> int:
    if not os.path.isdir(AGENTS_DIR):
        print(f"Diretorio nao encontrado: {AGENTS_DIR}")
        print("Crie agents nativos em agents/mos-*.md primeiro.")
        return 1

    files = sorted(glob.glob(os.path.join(AGENTS_DIR, "mos-*.md")))
    if not files:
        print(f"Nenhum mos-*.md encontrado em {AGENTS_DIR}")
        return 1

    counts = {"ok": 0, "skip-existing": 0, "skip-malformed": 0}
    for fp in files:
        result = inject(fp)
        counts[result] += 1
        name = os.path.basename(fp)
        print(f"  {result}: {name}")

    print(f"\nTotal: {len(files)} arquivos | adicionados: {counts['ok']} | "
          f"ja-tinham: {counts['skip-existing']} | pulados: {counts['skip-malformed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
