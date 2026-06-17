# Contributing to datavault4dbt Agent Skills

Thanks for your interest in contributing! This guide helps you create, improve, and submit skills that
help AI agents work effectively with the [datavault4dbt](https://github.com/ScalefreeCOM/datavault4dbt)
dbt package.

## About this repository

This repository contains Agent Skills for building Data Vault 2 warehouses with datavault4dbt. Skills
follow the [Agent Skills specification](https://agentskills.io/specification) and help AI agents create
staging, hub, link, satellite, and business-vault models correctly.

## How to contribute

- **Add a new skill** for a datavault4dbt workflow or entity type.
- **Improve existing skills** — better examples, clearer parameter guidance, adapter-specific notes.
- **Fix issues** — incorrect macro usage, outdated parameters, unclear instructions.

## Setup

```bash
uv sync                              # install dev dependencies (or: pip install -e ".[dev]")
pre-commit install                   # optional: run hooks on commit
python scripts/validate_skills.py    # validate all SKILL.md frontmatter
```

## Creating a new skill

### 1. Create the skill folder

Use a descriptive **gerund** name (verb + -ing) in kebab-case:

```bash
mkdir -p skills/datavault4dbt/skills/creating-datavault4dbt-hubs
```

### 2. Create SKILL.md

```markdown
---
name: creating-datavault4dbt-hubs
description: Generates Data Vault hub models with the datavault4dbt.hub macro, wiring business keys, hashkeys, and multi-source loading. Use when creating or editing hub models, choosing hub business keys, or loading one hub from several sources.
user-invocable: false
metadata:
  author: scalefree
---

# Creating datavault4dbt Hubs

...
```

### 3. Add supporting resources (optional)

Put deep parameter tables, per-adapter notes, and long worked examples in `references/`, and helper
scripts in `scripts/`. Link them inline from `SKILL.md`.

## Style guide

- **Verify against the package**: confirm every macro name, parameter, and default against
  `datavault4dbt`'s `docs/` and `macros/`. Do not document from memory.
- **Naming**: folders in gerund kebab-case; `name` matches the folder exactly; `SKILL.md` uppercase,
  supporting files lowercase.
- **Descriptions**: lead with a concrete capability statement, then "Use when…". Specific triggers stop
  skills from competing for activation.
- **Examples first**: show the `{%- set yaml_metadata -%}` block and the macro call before prose.
- **Adapter awareness**: datavault4dbt supports 11 adapters; call out where behavior/defaults differ.
- **Allowed frontmatter fields only**: `name`, `description`, `user-invocable`, `allowed-tools`,
  `compatibility`, `license`, `metadata`. No top-level `version`, `author`, or `tags`.

## Testing your skill

- Run `python scripts/validate_skills.py`.
- Pressure-test against a real datavault4dbt project (e.g. a copy of `finance-dbt-demo`): have an agent
  use the skill, then confirm the generated models compile and build (`dbt deps && dbt build`).
- See [`evals/`](evals/) for the A/B harness comparing skill variations.

## Submitting a pull request

1. Run `changie new` to add a changelog entry.
2. Ensure validation passes and the README skill table is updated.
3. Open a PR using the template and link any related issue.

## Skill ideas

- Per-entity skills: staging, hubs, links (+ non-historized), satellites (standard/multi-active/
  effectivity/record-tracking/non-historized).
- Configuration: `packages.yml`, global variables, per-adapter setup.
- Business vault: PIT tables, snapshot control, the PIT cleanup hook.
- Operations: testing a Data Vault, rehashing entities.

## License

By contributing, you agree that your contributions will be licensed under the same license as this
repository (Apache-2.0).
