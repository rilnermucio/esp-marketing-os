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


def test_validator_accepts_repository_root():
    assert validator.validate(ROOT) == []


def test_validator_finds_repo_from_source_and_generated_roots(tmp_path):
    repo, plugin = _generated_repo(tmp_path)

    assert validator.find_repo_root(repo) == repo
    assert validator.find_repo_root(plugin) == repo


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


def test_validator_rejects_invalid_public_listing_metadata(tmp_path):
    _, plugin = _generated_repo(tmp_path)
    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["interface"]["shortDescription"] = "x" * 31
    manifest["interface"]["category"] = "Marketing"
    manifest["interface"]["defaultPrompt"] = ["prompt"] * 4
    manifest["mcpServers"] = {}
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = validator.validate(plugin)

    assert any("shortDescription must be at most 30" in error for error in errors)
    assert any("category must be one of" in error for error in errors)
    assert any("defaultPrompt must contain at most 3" in error for error in errors)
    assert any("must not declare mcpServers" in error for error in errors)


def test_validator_rejects_nonportable_skill_metadata(tmp_path):
    _, plugin = _generated_repo(tmp_path)
    skill_root = plugin / "skills" / "marketing-os"
    skill_path = skill_root / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    skill_path.write_text(
        skill.replace("\n---\n", "\nargument-hint: briefing\n---\n", 1),
        encoding="utf-8",
    )

    metadata_path = skill_root / "agents" / "openai.yaml"
    metadata = metadata_path.read_text(encoding="utf-8")
    metadata_path.write_text(
        metadata.rstrip() + "\n  products:\n    - codex\n",
        encoding="utf-8",
    )

    errors = validator.validate(plugin)

    assert any("unsupported frontmatter fields" in error for error in errors)
    assert any("policy.products must be omitted" in error for error in errors)


def test_validator_ignores_foreign_ancestor_marketplace(tmp_path):
    """Cópia staged sob ~/plugins não herda o marketplace pessoal de ~/.agents (v6.16.0)."""
    home = tmp_path / "home"
    foreign = home / ".agents" / "plugins" / "marketplace.json"
    foreign.parent.mkdir(parents=True)
    foreign.write_text(
        json.dumps(
            {"name": "plugins-cli", "plugins": [{"name": "outro", "source": "./x"}]}
        ),
        encoding="utf-8",
    )
    staged = home / "plugins" / "marketing-os"
    builder.build_plugin(staged)

    assert validator.find_repo_root(staged) is None
    assert validator.validate(staged) == []


def test_validator_still_requires_marketplace_in_source_repo(tmp_path):
    repo, _ = _generated_repo(tmp_path)
    (repo / ".agents" / "plugins" / "marketplace.json").unlink()
    (repo / ".codex-plugin").mkdir()
    shutil.copy2(
        ROOT / ".codex-plugin" / "plugin.json", repo / ".codex-plugin" / "plugin.json"
    )
    errors = validator.validate(repo)
    assert any("Could not locate repository marketplace" in e for e in errors)


def test_validator_accepts_personal_marketplace_listing_the_plugin(tmp_path):
    """Caso real da v6.16.0: ~/.agents/plugins/marketplace.json (plugins-cli) lista o plugin."""
    home = tmp_path / "home"
    personal = home / ".agents" / "plugins" / "marketplace.json"
    personal.parent.mkdir(parents=True)
    entry = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )["plugins"][0]
    personal.write_text(
        json.dumps({"name": "plugins-cli", "plugins": [entry]}), encoding="utf-8"
    )
    staged = home / "plugins" / "marketing-os"
    builder.build_plugin(staged)

    assert validator.find_repo_root(staged) == home.resolve()
    assert validator.validate(staged) == []
