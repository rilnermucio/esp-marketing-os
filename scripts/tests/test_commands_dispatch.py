"""
test_commands_dispatch.py — Validates static dispatch structure of slash commands.

Ensures every command in commands/ (except declared utility commands) dispatches
real subagents via the Agent(subagent_type: "mos-*", prompt: "...") pattern.

Does not test runtime behavior (that requires a live Claude Code session) — only
static structural properties that can be verified by parsing the command file.

Catches regressions where a new command ships without proper dispatch wiring.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
COMMANDS_DIR = PROJECT_ROOT / "commands"
AGENTS_DIR = PROJECT_ROOT / "agents"

# Commands that are pure utilities (do not need to dispatch mos-* agents).
# Add new entries here when a command is intentionally non-dispatching
# (e.g. it only routes to other commands or only calls MCP tools directly).
UTILITY_COMMANDS = {
    "publicar-notion.md",  # routes to other /criar-* commands when generation is needed
    "campanha.md",  # index of /campanha-* sub-commands; pure router, no direct dispatch
    "projeto.md",  # workflow orchestrator; dispatch is dynamic per pipeline stage at runtime
    "datas-sazonais.md",  # data utility (seasonal_calendar_br); shows dates, no agent dispatch
}

# Regex to extract the agent name from any Agent(subagent_type: "mos-*") call.
# Tolerates single quotes, double quotes, or no quotes around the value.
DISPATCH_RE = re.compile(r'subagent_type:\s*["\']?(mos-[a-z-]+)["\']?')

# YAML frontmatter delimiter regex.
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

# Section markers that satisfy the "consolidation/output" requirement.
# Commands must surface a clear consolidation step, a final output schema,
# a phased dispatch breakdown, or an explicit checklist/KPI block so the
# orchestrator knows how to compose subagent results.
CONSOLIDATION_MARKERS = (
    "## Consolidação",
    "## Consolidacao",
    "## Consolidação do",
    "## Output",
    "## Final output",
    "## Saída",
    "## Saida",
    "OUTPUT STRUCTURE",
    "## Brief Consolidado",
    "Brief Consolidado:",
    "## Fase 3",
    "## Phase 3",
    "## Phase 4",
    "## Phase pos-dispatch",
    "### Checklist",
    "### Cronograma",
    "### KPIs",
)


def get_all_commands() -> list[Path]:
    return sorted(COMMANDS_DIR.glob("*.md"))


def get_existing_agents() -> set[str]:
    return {p.stem for p in AGENTS_DIR.glob("mos-*.md")}


def get_dispatch_commands() -> list[Path]:
    """Commands expected to dispatch (excludes declared utilities)."""
    return [p for p in get_all_commands() if p.name not in UTILITY_COMMANDS]


class TestCommandStructure:
    """Basic structural sanity checks for every command file."""

    @pytest.mark.parametrize("cmd", get_all_commands(), ids=lambda p: p.name)
    def test_has_frontmatter(self, cmd: Path) -> None:
        content = cmd.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(content)
        assert match, f"{cmd.name} has no YAML frontmatter"

    @pytest.mark.parametrize("cmd", get_all_commands(), ids=lambda p: p.name)
    def test_frontmatter_has_description(self, cmd: Path) -> None:
        content = cmd.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(content)
        assert match, f"{cmd.name} has no YAML frontmatter"
        fm = match.group(1)
        assert "description:" in fm, (
            f"{cmd.name} frontmatter is missing the 'description' field"
        )


class TestCommandDispatch:
    """Production commands must dispatch real, existing agents."""

    @pytest.mark.parametrize(
        "cmd", get_dispatch_commands(), ids=lambda p: p.name
    )
    def test_command_dispatches_at_least_one_agent(self, cmd: Path) -> None:
        content = cmd.read_text(encoding="utf-8")
        agents_dispatched = DISPATCH_RE.findall(content)
        assert agents_dispatched, (
            f"{cmd.name} does not dispatch any agent "
            f"(expected at least one Agent(subagent_type: 'mos-*'))"
        )

    @pytest.mark.parametrize(
        "cmd", get_dispatch_commands(), ids=lambda p: p.name
    )
    def test_dispatched_agents_exist(self, cmd: Path) -> None:
        content = cmd.read_text(encoding="utf-8")
        agents_dispatched = set(DISPATCH_RE.findall(content))
        existing = get_existing_agents()
        missing = agents_dispatched - existing
        assert not missing, (
            f"{cmd.name} dispatches agents that do not exist in agents/: "
            f"{sorted(missing)}"
        )


class TestCommandConsolidation:
    """Dispatch commands must show how subagent outputs are consolidated."""

    @pytest.mark.parametrize(
        "cmd", get_dispatch_commands(), ids=lambda p: p.name
    )
    def test_has_consolidacao_or_output_section(self, cmd: Path) -> None:
        content = cmd.read_text(encoding="utf-8")
        has_section = any(marker in content for marker in CONSOLIDATION_MARKERS)
        assert has_section, (
            f"{cmd.name} has no consolidation/output section. "
            f"Add one of: {', '.join(CONSOLIDATION_MARKERS)}"
        )


class TestCommandQualityGates:
    """Dispatch commands must reference Quality Gates explicitly or via SKILL.md."""

    @pytest.mark.parametrize(
        "cmd", get_dispatch_commands(), ids=lambda p: p.name
    )
    def test_has_quality_gates_reference(self, cmd: Path) -> None:
        content = cmd.read_text(encoding="utf-8").lower()
        has_qg = (
            "quality gate" in content
            or "quality_gate" in content
            or "skill.md" in content  # indirect reference via SKILL.md import
        )
        assert has_qg, (
            f"{cmd.name} has no reference to Quality Gates "
            f"(expected 'Quality Gate', 'quality_gate', or 'SKILL.md')"
        )


class TestUtilityCommands:
    """Utility commands must be explicitly declared in UTILITY_COMMANDS."""

    def test_utility_commands_exist(self) -> None:
        for utility in UTILITY_COMMANDS:
            path = COMMANDS_DIR / utility
            assert path.exists(), (
                f"Utility command {utility} does not exist "
                f"(review UTILITY_COMMANDS set)"
            )

    def test_no_unexpected_non_dispatch_commands(self) -> None:
        """Fail if a non-utility command silently ships without dispatch.

        Catches the regression where someone writes a new command without the
        Agent(subagent_type: 'mos-*') pattern and forgets to mark it as utility.
        """
        offenders = []
        for cmd in get_dispatch_commands():
            content = cmd.read_text(encoding="utf-8")
            if not DISPATCH_RE.search(content):
                offenders.append(cmd.name)
        assert not offenders, (
            f"Commands without dispatch (add to UTILITY_COMMANDS if intentional): "
            f"{offenders}"
        )
