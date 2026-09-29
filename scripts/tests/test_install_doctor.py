"""Diagnóstico de cópias instaladas (F-DIST-07, auditoria 2026-09-28 achado #4)."""

from __future__ import annotations

import json
from pathlib import Path

import install_doctor as doctor


def _manifest(directory: Path, version: str) -> None:
    (directory / ".claude-plugin").mkdir(parents=True)
    (directory / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "marketing-os", "version": version}), encoding="utf-8"
    )


def _fake_plugins(tmp_path: Path, synced_version: str) -> Path:
    plugins = tmp_path / "plugins"
    _manifest(
        plugins / "cache" / "mos-marketplace" / "marketing-os" / "6.16.0", "6.16.0"
    )
    synced = plugins / "synced" / "conta_x" / "marketing-os"
    _manifest(synced, synced_version)
    (synced.parent / "marketing-os.meta.json").write_text(
        json.dumps({"marketplace_name": "Marketing-OS"}), encoding="utf-8"
    )
    (plugins / "installed_plugins.json").write_text(
        json.dumps(
            {
                "plugins": {
                    "marketing-os@mos-marketplace": [
                        {"scope": "user", "version": "6.16.0", "installPath": "x"}
                    ],
                    "outro@mkt": [{"scope": "user", "version": "1.0.0"}],
                }
            }
        ),
        encoding="utf-8",
    )
    return plugins


def test_finds_every_copy_with_origin(tmp_path):
    copies = doctor.find_copies(_fake_plugins(tmp_path, "6.1.5"))
    origins = sorted(c["origin"].split(" ")[0] for c in copies)
    assert origins == ["cache", "registro", "sincronizada"]
    synced = next(c for c in copies if c["origin"].startswith("sincronizada"))
    assert synced["version"] == "6.1.5"
    assert synced["marketplace"] == "Marketing-OS"


def test_flags_outdated_synced_copy_with_account_hint(tmp_path):
    copies = doctor.find_copies(_fake_plugins(tmp_path, "6.1.5"))
    warnings = doctor.diagnose(copies, "6.16.0")
    outdated = [w for w in warnings if "6.1.5" in w]
    assert outdated and "claude.ai" in outdated[0] and "Marketing-OS" in outdated[0]


def test_versions_compare_numerically(tmp_path):
    copies = [{"origin": "cache (x)", "version": "6.9.0", "path": ""}]
    assert doctor.diagnose(copies, "6.10.0")
    assert not doctor.diagnose(copies, "6.9.0")


def test_strict_exit_code(tmp_path, capsys):
    plugins = _fake_plugins(tmp_path, "6.1.5")
    assert (
        doctor.main(
            ["--plugins-dir", str(plugins), "--reference", "6.16.0", "--strict"]
        )
        == 1
    )
    assert doctor.main(["--plugins-dir", str(plugins), "--reference", "6.16.0"]) == 0
    assert "AVISO" in capsys.readouterr().out


def test_empty_machine_is_not_an_error(tmp_path, capsys):
    assert (
        doctor.main(["--plugins-dir", str(tmp_path / "vazio"), "--reference", "6.16.0"])
        == 0
    )
    assert "Nenhuma cópia" in capsys.readouterr().out
