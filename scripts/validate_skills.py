#!/usr/bin/env python3
"""Validate SKILL.md frontmatter against the Agent Skills spec.

Checks every `**/SKILL.md` under `skills/` and `.claude/`:
  - frontmatter is present and parseable
  - only allowed top-level fields are used
  - `name` is lowercase letters/digits/hyphens and matches its directory name
  - `description` is present

Exits non-zero on any violation. No third-party dependencies (uses a tiny
frontmatter parser) so it runs in CI without an install step.
"""
from __future__ import annotations

import pathlib
import re
import sys

ALLOWED_FIELDS = {
    "name",
    "description",
    "allowed-tools",
    "compatibility",
    "license",
    "metadata",
    "user-invocable",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def top_level_keys(frontmatter: str) -> list[str]:
    """Return the top-level YAML keys in a frontmatter block (no nesting)."""
    keys = []
    for line in frontmatter.splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#", "-")):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):", line)
        if m:
            keys.append(m.group(1))
    return keys


def validate(skill: pathlib.Path) -> list[str]:
    errors: list[str] = []
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return [f"{skill}: missing frontmatter (must start with '---')"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [f"{skill}: malformed frontmatter (no closing '---')"]
    frontmatter = parts[1]
    keys = top_level_keys(frontmatter)

    extra = sorted(set(keys) - ALLOWED_FIELDS)
    if extra:
        errors.append(f"{skill}: disallowed top-level field(s): {', '.join(extra)}")
    if "name" not in keys:
        errors.append(f"{skill}: missing required field 'name'")
    if "description" not in keys:
        errors.append(f"{skill}: missing required field 'description'")

    name_match = re.search(r"^name:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip().strip("\"'")
        if not NAME_RE.match(name):
            errors.append(f"{skill}: name '{name}' must be lowercase letters/digits/hyphens")
        if name != skill.parent.name:
            errors.append(
                f"{skill}: name '{name}' does not match directory '{skill.parent.name}'"
            )
    return errors


def main() -> int:
    skills = sorted(ROOT.glob("skills/**/SKILL.md")) + sorted(ROOT.glob(".claude/**/SKILL.md"))
    if not skills:
        print("No SKILL.md files found.")
        return 0
    all_errors: list[str] = []
    for skill in skills:
        all_errors.extend(validate(skill))
    if all_errors:
        print("Skill validation FAILED:\n")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print(f"Validated {len(skills)} skill(s): OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
