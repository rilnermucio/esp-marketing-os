#!/usr/bin/env python3
"""Validate the Marketing OS Codex plugin package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import yaml  # type: ignore
except (
    ImportError
):  # pragma: no cover - CI installs PyYAML, local fallback is explicit.
    yaml = None  # type: ignore


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"Missing file: {path}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path} is not valid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path} must contain a JSON object")
        return None
    return data


def require_string(
    data: dict[str, Any], key: str, errors: list[str], label: str
) -> str | None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{key} must be a non-empty string")
        return None
    return value


def validate_url(value: Any, errors: list[str], label: str) -> None:
    parsed = urlparse(value) if isinstance(value, str) else None
    if parsed is None or parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"{label} must be an absolute https URL")


def validate_manifest(plugin_root: Path, errors: list[str]) -> None:
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path, errors)
    if manifest is None:
        return

    unsupported = set(manifest) - {
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "skills",
        "interface",
        "apps",
        "mcpServers",
    }
    if unsupported:
        errors.append(f"Unsupported plugin.json fields: {sorted(unsupported)}")

    name = require_string(manifest, "name", errors, "plugin.json")
    if name is not None and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("plugin.json.name must be kebab-case")

    version = require_string(manifest, "version", errors, "plugin.json")
    if version is not None and SEMVER_RE.fullmatch(version) is None:
        errors.append("plugin.json.version must be semver")

    require_string(manifest, "description", errors, "plugin.json")
    if manifest.get("skills") != "./skills/":
        errors.append('plugin.json.skills must be "./skills/"')

    for field in ("homepage", "repository"):
        if field in manifest:
            validate_url(manifest[field], errors, f"plugin.json.{field}")

    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append("plugin.json.author must be an object")
    else:
        require_string(author, "name", errors, "plugin.json.author")
        if "url" in author:
            validate_url(author["url"], errors, "plugin.json.author.url")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin.json.interface must be an object")
        return

    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        require_string(interface, field, errors, "plugin.json.interface")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts:
        errors.append("plugin.json.interface.defaultPrompt must be a non-empty list")


def validate_skill_frontmatter(skill_root: Path, errors: list[str]) -> None:
    skill_path = skill_root / "SKILL.md"
    if not skill_path.is_file():
        errors.append(f"Skill {skill_root.name} is missing SKILL.md")
        return

    content = skill_path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        errors.append(f"Skill {skill_root.name} must start with YAML frontmatter")
        return

    end = content.find("\n---", 4)
    if end == -1:
        errors.append(f"Skill {skill_root.name} frontmatter is not closed")
        return

    if yaml is None:
        errors.append("PyYAML is required to validate skill frontmatter")
        return

    try:
        frontmatter = yaml.safe_load(content[4:end])
    except yaml.YAMLError as exc:
        errors.append(f"Skill {skill_root.name} frontmatter is invalid YAML: {exc}")
        return

    if not isinstance(frontmatter, dict):
        errors.append(f"Skill {skill_root.name} frontmatter must be an object")
        return

    require_string(frontmatter, "name", errors, f"skill {skill_root.name}")
    require_string(frontmatter, "description", errors, f"skill {skill_root.name}")


def validate_skills(plugin_root: Path, errors: list[str]) -> None:
    skills_root = plugin_root / "skills"
    if not skills_root.is_dir():
        errors.append("Plugin package is missing skills/")
        return

    skill_dirs = [path for path in skills_root.iterdir() if path.is_dir()]
    if not skill_dirs:
        errors.append("Plugin package must include at least one skill")
        return

    for skill_root in sorted(skill_dirs):
        validate_skill_frontmatter(skill_root, errors)


def validate_symlinks(plugin_root: Path, errors: list[str]) -> None:
    for path in plugin_root.rglob("*"):
        if not path.is_symlink():
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(plugin_root.resolve()):
            errors.append(f"Symlink escapes plugin package: {path}")


def validate_marketplace(repo_root: Path, errors: list[str]) -> None:
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    marketplace = load_json(marketplace_path, errors)
    if marketplace is None:
        return

    if marketplace.get("name") != "marketing-os-marketplace":
        errors.append('marketplace.name must be "marketing-os-marketplace"')

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        errors.append("marketplace.plugins must be a list")
        return

    entry = next(
        (
            item
            for item in plugins
            if isinstance(item, dict) and item.get("name") == "marketing-os"
        ),
        None,
    )
    if entry is None:
        errors.append("marketplace must include a marketing-os plugin entry")
        return

    source = entry.get("source")
    if not isinstance(source, dict):
        errors.append("marketing-os marketplace entry source must be an object")
    elif (
        source.get("source") != "local"
        or source.get("path") != "./plugins/marketing-os"
    ):
        errors.append(
            'marketing-os marketplace source must point to "./plugins/marketing-os"'
        )

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("marketing-os marketplace entry policy must be an object")
    else:
        if policy.get("installation") != "AVAILABLE":
            errors.append('marketing-os policy.installation must be "AVAILABLE"')
        if policy.get("authentication") != "ON_INSTALL":
            errors.append('marketing-os policy.authentication must be "ON_INSTALL"')


def validate(plugin_root: Path) -> list[str]:
    errors: list[str] = []
    validate_manifest(plugin_root, errors)
    validate_skills(plugin_root, errors)
    validate_symlinks(plugin_root, errors)
    validate_marketplace(plugin_root.parents[1], errors)
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_root", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plugin_root = args.plugin_root.resolve()
    errors = validate(plugin_root)
    if errors:
        print("Codex plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Codex plugin validation passed: {plugin_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
