"""Distribuição Codex validada pelas interfaces públicas de build e validate."""

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_codex_plugin as builder  # noqa: E402
import validate_codex_plugin as validator  # noqa: E402


def _generated_repo(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    plugin = repo / "plugins" / "marketing-os"
    builder.build_plugin(plugin)
    marketplace = repo / ".agents" / "plugins" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    shutil.copy2(ROOT / ".agents" / "plugins" / "marketplace.json", marketplace)
    return repo, plugin


def test_builder_produces_installable_surface_without_test_sources(tmp_path):
    _, plugin = _generated_repo(tmp_path)

    assert (plugin / ".codex-plugin" / "plugin.json").is_file()
    assert (plugin / "skills" / "marketing-os" / "SKILL.md").is_file()
    assert (plugin / "scripts" / "quality_gate.py").is_file()
    assert (plugin / "scripts" / "evals" / "output-profiles.json").is_file()
    assert not (plugin / "scripts" / "tests").exists()

    completed = subprocess.run(
        [sys.executable, str(plugin / "scripts" / "copy_output_eval.py"), "profiles"],
        capture_output=True,
        text=True,
        check=True,
        cwd=tmp_path,
    )
    profiles = json.loads(completed.stdout)
    assert profiles["video"]["agent"] == "mos-video"


def test_builder_check_detects_package_drift(tmp_path, monkeypatch, capsys):
    _, plugin = _generated_repo(tmp_path)
    monkeypatch.setattr(builder, "DIST_ROOT", plugin)

    assert builder.check_plugin() == 0
    (plugin / "scripts" / "quality_gate.py").unlink()
    assert builder.check_plugin() == 1
    assert "Missing files" in capsys.readouterr().out


def test_validator_accepts_generated_package(tmp_path):
    _, plugin = _generated_repo(tmp_path)

    assert validator.validate(plugin) == []


def test_validator_rejects_invalid_manifest_and_escaping_symlink(tmp_path):
    repo, plugin = _generated_repo(tmp_path)
    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["name"] = "Marketing OS"
    manifest["version"] = "latest"
    manifest["skills"] = "skills"
    manifest["unsupported"] = True
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    outside = repo / "outside.txt"
    outside.write_text("fora", encoding="utf-8")
    (plugin / "escape").symlink_to(outside)

    errors = validator.validate(plugin)

    assert any("Unsupported" in error for error in errors)
    assert any("kebab-case" in error for error in errors)
    assert any("semver" in error for error in errors)
    assert any('skills must be "./skills/"' in error for error in errors)
    assert any("Symlink escapes" in error for error in errors)
