#!/usr/bin/env python3
"""
memory_writer.py — Persiste aprendizados na memory opt-in dos agents (append-only).

Escreve entradas datadas em `.claude/agent-memory/<agent>/MEMORY.md` sob a seção
"## Aprendizados", com idempotência e limites anti-poluição do ROADMAP Fase 4.

Uso:
    python3 scripts/memory_writer.py --agent mos-video --categoria resultado \\
        --texto "Hooks com pergunta direta retêm 12% a mais" --fonte "/aprender 2026-07"
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

from init_agent_memory import AGENTS_WITH_MEMORY, MEMORY_ROOT, PLACEHOLDER_TEMPLATE

ALLOWED_CATEGORIES = frozenset(
    {"resultado", "pattern", "anti-padrao", "voz", "benchmark-local"}
)
MAX_TEXT_LENGTH = 400
MAX_ENTRIES_PER_DAY = 20
LEARNING_SECTION = "## Aprendizados"
ENTRY_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2})\] \[([^\]]+)\] (.+) \(fonte: (.+)\)\s*$")


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _memory_path(agent: str) -> Path:
    return MEMORY_ROOT / agent / "MEMORY.md"


def _ensure_memory_file(agent: str) -> Path | None:
    """Cria MEMORY.md com o template do bootstrap se ainda não existir."""
    memory_file = _memory_path(agent)
    if memory_file.exists():
        return memory_file

    agent_dir = memory_file.parent
    agent_dir.mkdir(parents=True, exist_ok=True)
    memory_file.write_text(
        PLACEHOLDER_TEMPLATE.format(agent=agent),
        encoding="utf-8",
    )
    return memory_file


def _split_learning_section(content: str) -> tuple[str, str, str]:
    """Retorna (antes, corpo da seção, depois). Corpo vazio se seção não existe."""
    marker = LEARNING_SECTION
    idx = content.find(marker)
    if idx == -1:
        return content, "", ""

    after_marker = content[idx + len(marker) :]
    # Próxima seção ## encerra o bloco de aprendizados
    next_section = re.search(r"\n## ", after_marker)
    if next_section:
        body = after_marker[: next_section.start()]
        tail = after_marker[next_section.start() + 1 :]  # mantém o ##
        before = content[:idx]
        return before, body, tail

    before = content[:idx]
    return before, after_marker, ""


def _parse_entries(body: str) -> list[tuple[str, str, str, str, str]]:
    """Lista (data, categoria, texto, fonte, linha_original) das entradas válidas."""
    entries: list[tuple[str, str, str, str, str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("["):
            continue
        match = ENTRY_RE.match(stripped)
        if match:
            entries.append((*match.groups(), stripped))
    return entries


def _count_entries_for_date(body: str, target_date: str) -> int:
    return sum(1 for d, *_ in _parse_entries(body) if d == target_date)


def _entry_exists(body: str, categoria: str, texto: str) -> bool:
    for _, cat, txt, _, _ in _parse_entries(body):
        if cat == categoria and txt == texto:
            return True
    return False


def _format_entry(entry_date: str, categoria: str, texto: str, fonte: str) -> str:
    return f"[{entry_date}] [{categoria}] {texto} (fonte: {fonte})"


def append_learning(
    agent: str,
    categoria: str,
    texto: str,
    fonte: str,
    data: str | None = None,
) -> bool:
    """
    Anexa um aprendizado ao MEMORY.md do agent.

    Retorna True se escreveu, False se recusou (motivo em stderr).
    """
    if agent not in AGENTS_WITH_MEMORY:
        allowed = ", ".join(sorted(AGENTS_WITH_MEMORY))
        _log(
            f"ERRO: agent '{agent}' não tem memory opt-in. "
            f"Agents permitidos: {allowed}"
        )
        return False

    if categoria not in ALLOWED_CATEGORIES:
        allowed = ", ".join(sorted(ALLOWED_CATEGORIES))
        _log(f"ERRO: categoria '{categoria}' inválida. Permitidas: {allowed}")
        return False

    texto = texto.strip()
    if not texto:
        _log("ERRO: texto vazio")
        return False

    if len(texto) > MAX_TEXT_LENGTH:
        _log(f"ERRO: texto com {len(texto)} chars excede o máximo de {MAX_TEXT_LENGTH}")
        return False

    fonte = fonte.strip()
    if not fonte:
        _log("ERRO: fonte vazia")
        return False

    if data is None:
        entry_date = date.today().isoformat()
    else:
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            _log(f"ERRO: data inválida '{data}' (use YYYY-MM-DD)")
            return False
        entry_date = data

    memory_file = _ensure_memory_file(agent)
    if memory_file is None:
        _log(
            f"ERRO: MEMORY.md de '{agent}' não existe. "
            "Rode: python3 scripts/init_agent_memory.py"
        )
        return False

    content = memory_file.read_text(encoding="utf-8")
    before, body, tail = _split_learning_section(content)

    if _entry_exists(body, categoria, texto):
        _log("RECUSADO: entrada duplicada (mesmo agent, categoria e texto)")
        return False

    if _count_entries_for_date(body, entry_date) >= MAX_ENTRIES_PER_DAY:
        _log(
            f"AVISO: limite diário de {MAX_ENTRIES_PER_DAY} entradas atingido "
            f"para {agent} em {entry_date}"
        )
        return False

    new_line = _format_entry(entry_date, categoria, texto, fonte)

    if LEARNING_SECTION not in content:
        # Primeira escrita: cria a seção após o placeholder ou no final
        if content.rstrip().endswith(
            "(vazio — preenchido pelos agents conforme rodam)"
        ):
            base = content.rstrip() + "\n\n"
        else:
            base = content.rstrip() + "\n\n" if content.strip() else ""
        updated = base + f"{LEARNING_SECTION}\n\n{new_line}\n"
    else:
        if body.strip():
            new_body = body.rstrip() + "\n" + new_line + "\n"
        else:
            new_body = "\n" + new_line + "\n"
        updated = before + LEARNING_SECTION + new_body
        if tail:
            updated += tail if tail.startswith("##") else "##" + tail

    memory_file.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Persiste aprendizado na memory opt-in de um agent Marketing OS",
    )
    parser.add_argument("--agent", required=True, help="Nome do agent (ex: mos-video)")
    parser.add_argument(
        "--categoria",
        required=True,
        help="Categoria: resultado, pattern, anti-padrao, voz, benchmark-local",
    )
    parser.add_argument(
        "--texto", required=True, help="Texto do aprendizado (máx 400 chars)"
    )
    parser.add_argument(
        "--fonte",
        required=True,
        help="Origem do aprendizado (ex: /aprender 2026-07)",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="Data da entrada YYYY-MM-DD (default: hoje)",
    )
    args = parser.parse_args()

    ok = append_learning(
        agent=args.agent,
        categoria=args.categoria,
        texto=args.texto,
        fonte=args.fonte,
        data=args.data,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
