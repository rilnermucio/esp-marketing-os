#!/usr/bin/env python3
"""Validate the Marketing OS universal ChatGPT Work and Codex package."""

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

PUBLIC_CATEGORIES = {
    "Productivity",
    "Creativity",
    "Developer Tools",
    "Business & Operations",
    "Data & Analytics",
    "Communication",
    "Education & Research",
    "Security",
    "Finance",
    "Healthcare",
    "Travel",
    "Entertainment",
    "Other",
}
PLUGIN_NAME = "marketing-os"
SKILL_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "allowed-tools",
    "license",
    "metadata",
}


def validate_max_length(
    value: str | None, maximum: int, errors: list[str], label: str
) -> None:
    if value is not None and len(value) > maximum:
        errors.append(f"{label} must be at most {maximum} characters")


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

    for field in ("apps", "mcpServers"):
        if field in manifest:
            errors.append(f"skills-only Marketing OS package must not declare {field}")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin.json.interface must be an object")
        return

    public_text_limits = {
        "displayName": 30,
        "shortDescription": 30,
        "longDescription": 4_000,
        "developerName": 80,
    }
    for field, maximum in public_text_limits.items():
        value = require_string(interface, field, errors, "plugin.json.interface")
        validate_max_length(value, maximum, errors, f"plugin.json.interface.{field}")

    category = require_string(interface, "category", errors, "plugin.json.interface")
    if category is not None and category not in PUBLIC_CATEGORIES:
        errors.append(
            "plugin.json.interface.category must be one of "
            f"{sorted(PUBLIC_CATEGORIES)}"
        )

    capabilities = interface.get("capabilities")
    if capabilities is not None:
        if not isinstance(capabilities, list):
            errors.append("plugin.json.interface.capabilities must be a list")
        else:
            if len(capabilities) > 20:
                errors.append(
                    "plugin.json.interface.capabilities must contain at most 20 entries"
                )
            for index, capability in enumerate(capabilities):
                if not isinstance(capability, str) or not capability.strip():
                    errors.append(
                        "plugin.json.interface.capabilities"
                        f"[{index}] must be a non-empty string"
                    )
                elif len(capability) > 120:
                    errors.append(
                        "plugin.json.interface.capabilities"
                        f"[{index}] must be at most 120 characters"
                    )

    for field in (
        "websiteURL",
        "privacyPolicyURL",
        "termsOfServiceURL",
        "supportURL",
    ):
        if field in interface:
            validate_url(interface[field], errors, f"plugin.json.interface.{field}")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts:
        errors.append("plugin.json.interface.defaultPrompt must be a non-empty list")
    else:
        if len(prompts) > 3:
            errors.append(
                "plugin.json.interface.defaultPrompt must contain at most 3 prompts"
            )
        for index, prompt in enumerate(prompts):
            label = f"plugin.json.interface.defaultPrompt[{index}]"
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{label} must be a non-empty string")
                continue
            if "\n" in prompt or "\r" in prompt:
                errors.append(f"{label} must fit on one line")
            validate_max_length(prompt, 128, errors, label)


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

    unsupported = set(frontmatter) - SKILL_FRONTMATTER_FIELDS
    if unsupported:
        errors.append(
            f"Skill {skill_root.name} has unsupported frontmatter fields: "
            f"{sorted(unsupported)}"
        )

    require_string(frontmatter, "name", errors, f"skill {skill_root.name}")
    require_string(frontmatter, "description", errors, f"skill {skill_root.name}")


def validate_skill_agent_metadata(skill_root: Path, errors: list[str]) -> None:
    metadata_path = skill_root / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return
    if yaml is None:
        errors.append("PyYAML is required to validate skill agent metadata")
        return
    try:
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"Skill {skill_root.name} agents/openai.yaml is invalid: {exc}")
        return
    if not isinstance(metadata, dict):
        errors.append(f"Skill {skill_root.name} agents/openai.yaml must be an object")
        return

    interface = metadata.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"Skill {skill_root.name} agents/openai.yaml needs interface")
    else:
        require_string(
            interface,
            "display_name",
            errors,
            f"skill {skill_root.name} agents/openai.yaml.interface",
        )
        require_string(
            interface,
            "short_description",
            errors,
            f"skill {skill_root.name} agents/openai.yaml.interface",
        )

    policy = metadata.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"Skill {skill_root.name} agents/openai.yaml needs policy")
        return
    if "products" in policy:
        errors.append(
            f"Skill {skill_root.name} policy.products must be omitted for universal "
            "host compatibility"
        )
    if policy.get("allow_implicit_invocation") is not True:
        errors.append(
            f"Skill {skill_root.name} policy.allow_implicit_invocation must be true"
        )


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
        validate_skill_agent_metadata(skill_root, errors)


def validate_symlinks(plugin_root: Path, errors: list[str]) -> None:
    for path in plugin_root.rglob("*"):
        if not path.is_symlink():
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(plugin_root.resolve()):
            errors.append(f"Symlink escapes plugin package: {path}")


def validate_marketplace(
    repo_root: Path, errors: list[str], require_name: bool = True
) -> None:
    """Checks the marketplace that lists the plugin.

    The name is only required in the source repository; a personal marketplace
    (e.g. ~/.agents with its own name) may list the plugin too, and then only
    the marketing-os entry is checked.
    """
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    marketplace = load_json(marketplace_path, errors)
    if marketplace is None:
        return

    if require_name and marketplace.get("name") != "marketing-os-marketplace":
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
        if "products" in policy:
            errors.append("marketing-os marketplace policy must not gate products")

    if entry.get("category") not in PUBLIC_CATEGORIES:
        errors.append(
            "marketing-os marketplace category must be one of "
            f"{sorted(PUBLIC_CATEGORIES)}"
        )


def _marketplace_owns(candidate: Path, plugin_root: Path) -> bool:
    """True if the marketplace at `candidate` lists this plugin root.

    The source repository owns both its own root and the generated package it
    points to. A marketplace that merely sits in an ancestor directory (e.g. a
    personal Codex marketplace in the home folder) does not own the package.
    """
    marketplace = candidate / ".agents" / "plugins" / "marketplace.json"
    try:
        data = json.loads(marketplace.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    for entry in data.get("plugins") or []:
        if not isinstance(entry, dict) or entry.get("name") != PLUGIN_NAME:
            continue
        source = entry.get("source")
        path = source.get("path") if isinstance(source, dict) else source
        if plugin_root == candidate:
            return True
        if isinstance(path, str) and (candidate / path).resolve() == plugin_root:
            return True
    return False


def find_repo_root(plugin_root: Path) -> Path | None:
    """Find the repository that owns a source or generated plugin root.

    Ancestor marketplaces that do not list this plugin are skipped (follow-up
    of release v6.16.0: a staged copy under ~/plugins picked up the personal
    ~/.agents marketplace and failed validation).
    """
    plugin_root = plugin_root.resolve()
    for candidate in (plugin_root, *plugin_root.parents):
        marketplace = candidate / ".agents" / "plugins" / "marketplace.json"
        if marketplace.is_file() and _marketplace_owns(candidate, plugin_root):
            return candidate
    return None


def validate(plugin_root: Path) -> list[str]:
    plugin_root = plugin_root.resolve()
    errors: list[str] = []
    validate_manifest(plugin_root, errors)
    validate_skills(plugin_root, errors)
    validate_symlinks(plugin_root, errors)
    repo_root = find_repo_root(plugin_root)
    if repo_root is not None:
        is_source_repo = (repo_root / ".claude-plugin").is_dir()
        validate_marketplace(repo_root, errors, require_name=is_source_repo)
    elif (plugin_root / "plugins" / PLUGIN_NAME).is_dir():
        # Source repository without its marketplace: that is a real error.
        errors.append(
            "Could not locate repository marketplace at "
            '".agents/plugins/marketplace.json" for the source repository'
        )
    # A standalone package (staged or installed copy) has no owning marketplace
    # to check; manifest, skills and symlinks were validated above.
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "plugin_root",
        type=Path,
        help="Repository root or generated plugins/marketing-os package root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plugin_root = args.plugin_root.resolve()
    errors = validate(plugin_root)
    if errors:
        print("ChatGPT Work and Codex plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"ChatGPT Work and Codex plugin validation passed: {plugin_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
