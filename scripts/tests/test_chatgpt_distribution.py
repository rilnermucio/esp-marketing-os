"""Contratos da distribuição skills-only para ChatGPT Work e Codex."""

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILL_ROOT = ROOT / "skills" / "marketing-os"


def test_manifest_describes_a_public_skills_only_plugin() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    interface = manifest["interface"]

    assert "ChatGPT Work" in manifest["description"]
    assert "Codex" in manifest["description"]
    assert manifest["skills"] == "./skills/"
    assert "apps" not in manifest
    assert "mcpServers" not in manifest
    assert interface["category"] == "Business & Operations"
    assert len(interface["shortDescription"]) <= 30
    assert 1 <= len(interface["defaultPrompt"]) <= 3
    assert all(
        len(prompt) <= 128 and "\n" not in prompt
        for prompt in interface["defaultPrompt"]
    )


def test_repo_marketplace_is_universal_and_not_product_gated() -> None:
    marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    plugin = next(
        entry for entry in marketplace["plugins"] if entry["name"] == "marketing-os"
    )

    assert plugin["source"] == {
        "source": "local",
        "path": "./plugins/marketing-os",
    }
    assert plugin["category"] == "Business & Operations"
    assert "products" not in plugin["policy"]


def test_skill_declares_the_chatgpt_work_invocation_contract() -> None:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(text.split("---", 2)[1])

    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "marketing-os"
    assert "## Invocação no ChatGPT Work" in text
    assert "@Marketing OS" in text
    assert "/criar-avatar" in text
    assert "/criar-usp" in text
    assert "/criar-oferta" in text


def test_openai_skill_metadata_enables_implicit_invocation() -> None:
    metadata = yaml.safe_load(
        (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )

    assert metadata["interface"]["display_name"] == "Marketing OS"
    assert len(metadata["interface"]["short_description"]) <= 30
    assert metadata["policy"]["allow_implicit_invocation"] is True
    assert "products" not in metadata["policy"]


def test_readme_documents_chatgpt_work_install_and_use() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "### ChatGPT Work" in readme
    assert ".agents/plugins/marketplace.json" in readme
    assert "@Marketing OS" in readme


def test_local_plugin_update_has_a_symlink_safety_preflight() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs/ai-engineering/RELEASE-CHECKLIST.md").read_text(
        encoding="utf-8"
    )

    for document in (agents, checklist):
        assert "F-CODEX-04" in document
        assert "test ! -L" in document
        assert "realpath" in document
        assert "rsync --delete" in document
