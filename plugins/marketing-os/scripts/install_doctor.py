#!/usr/bin/env python3
"""Diagnóstico de instalação: quais cópias do Marketing OS existem nesta máquina.

O Claude Code guarda o plugin em lugares diferentes conforme a origem
(marketplace local, cache versionado, cópia sincronizada da conta claude.ai).
Na auditoria de 2026-09-28 o app desktop carregava uma cópia sincronizada
congelada na v6.1.5 enquanto a 6.16.0 estava instalada; nada avisava. Este
script lista todas as cópias, compara com a versão de referência (a deste
checkout) e aponta divergências.

Uso:
    python3 scripts/install_doctor.py
    python3 scripts/install_doctor.py --plugins-dir ~/.claude/plugins --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PLUGIN_NAME = "marketing-os"
REFERENCE_MANIFEST = (
    Path(__file__).resolve().parent.parent / ".claude-plugin" / "plugin.json"
)


def _version_tuple(version: str) -> tuple:
    parts = []
    for piece in version.split("+")[0].split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _manifest_version(plugin_dir: Path) -> str:
    for candidate in (
        plugin_dir / ".claude-plugin" / "plugin.json",
        plugin_dir / "plugin.json",
    ):
        data = _read_json(candidate)
        if data.get("name") == PLUGIN_NAME:
            return str(data.get("version", "?"))
    return ""


def find_copies(plugins_dir: Path) -> list[dict]:
    """Todas as cópias do plugin sob `plugins_dir`, com origem e versão."""
    copies: list[dict] = []

    for version_dir in sorted((plugins_dir / "cache").glob(f"*/{PLUGIN_NAME}/*")):
        version = _manifest_version(version_dir)
        if version:
            copies.append(
                {
                    "origin": f"cache ({version_dir.parent.parent.name})",
                    "version": version,
                    "path": str(version_dir),
                }
            )

    for synced_dir in sorted((plugins_dir / "synced").glob(f"*/{PLUGIN_NAME}*")):
        if not synced_dir.is_dir():
            continue
        version = _manifest_version(synced_dir)
        if not version:
            continue
        meta = _read_json(synced_dir.parent / f"{synced_dir.name}.meta.json")
        copies.append(
            {
                "origin": "sincronizada da conta claude.ai",
                "marketplace": meta.get("marketplace_name", "?"),
                "version": version,
                "path": str(synced_dir),
            }
        )

    installed = _read_json(plugins_dir / "installed_plugins.json")
    entries = installed.get("plugins", installed) if isinstance(installed, dict) else {}
    for key, records in (entries or {}).items():
        if not str(key).startswith(f"{PLUGIN_NAME}@"):
            continue
        for record in records if isinstance(records, list) else [records]:
            if isinstance(record, dict):
                copies.append(
                    {
                        "origin": f"registro de instalação ({key}, escopo {record.get('scope', '?')})",
                        "version": str(record.get("version", "?")),
                        "path": str(record.get("installPath", "")),
                    }
                )
    return copies


def diagnose(copies: list[dict], reference: str) -> list[str]:
    warnings: list[str] = []
    ref = _version_tuple(reference) if reference else None
    for copy in copies:
        if ref is None or copy["version"] == "?":
            continue
        if _version_tuple(copy["version"]) < ref:
            hint = ""
            if copy["origin"].startswith("sincronizada"):
                hint = (
                    " O app desktop pode estar carregando esta cópia. Remova ou atualize o "
                    f"marketplace '{copy.get('marketplace', '?')}' nas configurações de plugins "
                    "da sua conta claude.ai."
                )
            warnings.append(
                f"{copy['origin']} está na {copy['version']}, abaixo da referência {reference}.{hint}"
            )
    synced = [c for c in copies if c["origin"].startswith("sincronizada")]
    local = [c for c in copies if not c["origin"].startswith("sincronizada")]
    if synced and local:
        warnings.append(
            "Há cópia sincronizada da conta e cópia instalada localmente com o mesmo nome "
            f"'{PLUGIN_NAME}'. Mantenha uma só origem para saber qual versão está ativa."
        )
    return warnings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--plugins-dir",
        default=str(Path.home() / ".claude" / "plugins"),
        help="Diretório de plugins do Claude Code (padrão: ~/.claude/plugins)",
    )
    parser.add_argument(
        "--reference",
        default="",
        help="Versão de referência (padrão: a do plugin.json deste checkout)",
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    parser.add_argument(
        "--strict", action="store_true", help="Exit 1 quando houver divergência"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    reference = args.reference or str(_read_json(REFERENCE_MANIFEST).get("version", ""))
    copies = find_copies(Path(args.plugins_dir).expanduser())
    warnings = diagnose(copies, reference)

    if args.json:
        print(
            json.dumps(
                {"reference": reference, "copies": copies, "warnings": warnings},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Marketing OS: referência {reference or '?'}")
        if not copies:
            print("Nenhuma cópia instalada encontrada.")
        for copy in copies:
            print(
                f"- {copy['version']:>8}  {copy['origin']}\n            {copy['path']}"
            )
        for warning in warnings:
            print(f"AVISO: {warning}")
        if copies and not warnings:
            print("Tudo coerente.")
    return 1 if (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
