#!/usr/bin/env python3
"""Build the distributable Codex plugin package."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "marketing-os"
DIST_ROOT = ROOT / "plugins" / PLUGIN_NAME

COPY_DIRS = [
    ".codex-plugin",
    "agents",
    "assets",
    "commands",
    "references",
    "scripts",
    "skills",
    "subagents",
    "workflows",
]

COPY_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "README.md",
    "requirements.txt",
]

EXCLUDED_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    "tests",
}

EXCLUDED_FILE_NAMES = {
    ".DS_Store",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
}


def should_ignore(_: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        path = Path(name)
        if name in EXCLUDED_DIR_NAMES or name in EXCLUDED_FILE_NAMES:
            ignored.add(name)
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            ignored.add(name)
    return ignored


def copy_tree(src: Path, dest: Path) -> None:
    shutil.copytree(src, dest, symlinks=True, ignore=should_ignore)


def build_plugin(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    for dirname in COPY_DIRS:
        src = ROOT / dirname
        if not src.exists():
            raise FileNotFoundError(f"Missing required directory: {src}")
        copy_tree(src, dest / dirname)

    for filename in COPY_FILES:
        src = ROOT / filename
        if not src.exists():
            raise FileNotFoundError(f"Missing required file: {src}")
        shutil.copy2(src, dest / filename)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = ("symlink", str(path.readlink()))
        elif path.is_file():
            result[relative] = ("file", file_digest(path))
    return result


def print_snapshot_diff(
    expected: dict[str, tuple[str, str]], actual: dict[str, tuple[str, str]]
) -> None:
    expected_keys = set(expected)
    actual_keys = set(actual)

    missing = sorted(expected_keys - actual_keys)
    extra = sorted(actual_keys - expected_keys)
    changed = sorted(
        key for key in expected_keys & actual_keys if expected[key] != actual[key]
    )

    if missing:
        print("Missing files in plugins/marketing-os:")
        for key in missing[:50]:
            print(f"  - {key}")
    if extra:
        print("Extra files in plugins/marketing-os:")
        for key in extra[:50]:
            print(f"  - {key}")
    if changed:
        print("Changed files in plugins/marketing-os:")
        for key in changed[:50]:
            print(f"  - {key}")


def check_plugin() -> int:
    if not DIST_ROOT.exists():
        print(f"Missing distributable package: {DIST_ROOT}")
        print("Run: python scripts/build_codex_plugin.py")
        return 1

    with tempfile.TemporaryDirectory(prefix="marketing-os-codex-") as tmp:
        expected_root = Path(tmp) / PLUGIN_NAME
        build_plugin(expected_root)
        expected = snapshot(expected_root)
        actual = snapshot(DIST_ROOT)

    if expected != actual:
        print("plugins/marketing-os is out of sync with source files.")
        print_snapshot_diff(expected, actual)
        print("Run: python scripts/build_codex_plugin.py")
        return 1

    print("plugins/marketing-os is up to date.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify plugins/marketing-os matches the generated package.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        return check_plugin()

    build_plugin(DIST_ROOT)
    print(f"Built Codex plugin package: {DIST_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
