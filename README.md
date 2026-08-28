# datavault4dbt Agent Skills

A curated collection of [Agent Skills](https://agentskills.io/home) for the
[datavault4dbt](https://github.com/ScalefreeCOM/datavault4dbt) dbt package. These skills help AI agents
build **Data Vault 2** warehouses correctly — staging, hubs, links, satellites, and business-vault
entities — across all adapters datavault4dbt supports.

Maintained by [Scalefree](https://www.scalefree.com/).

---

## What are Agent Skills?

Agent Skills are folders of instructions, examples, and resources that agents discover and load
automatically. They are **not** slash commands: once installed, the agent loads the relevant skill when
your prompt matches its use case. Just describe what you need in natural language.

## What's included

- **Building Data Vault models with datavault4dbt**: how to lay out a project and generate staging,
  hubs, links, satellites, and business-vault models using the package's macros and YAML-metadata
  pattern — with the right hash configuration, naming conventions, and materializations.

## Installation

These skills are distributed as plain skill folders from this repository — there is no plugin
marketplace or registry listing. Install them by cloning the repo and pointing your agent's skills
directory at `skills/datavault4dbt/skills/`.

### 1. Clone the repository

```bash
git clone https://github.com/ScalefreeCOM/datavault4dbt-agent-skills.git
cd datavault4dbt-agent-skills
```

### 2. Link (or copy) the skills into a skills directory

Claude Code auto-discovers skills in two places:

- **User scope** — `~/.claude/skills/`, available in every project.
- **Project scope** — `<your-dbt-project>/.claude/skills/`, loaded once you trust the workspace.

Symlinking keeps the skills up to date with `git pull`:

```bash
# User scope (available everywhere)
mkdir -p ~/.claude/skills
ln -s "$PWD"/skills/datavault4dbt/skills/* ~/.claude/skills/
```

```bash
# Project scope (only in one dbt project)
mkdir -p /path/to/your-dbt-project/.claude/skills
ln -s "$PWD"/skills/datavault4dbt/skills/* /path/to/your-dbt-project/.claude/skills/
```

Prefer a copy if you want a frozen snapshot instead of a live link:

```bash
cp -r skills/datavault4dbt/skills/* ~/.claude/skills/
```

Install a single skill by naming it instead of globbing:

```bash
ln -s "$PWD"/skills/datavault4dbt/skills/using-datavault4dbt ~/.claude/skills/
```

### 3. Verify

Start a session in a dbt project and ask something like *"add a customer hub with datavault4dbt"* — the
agent should load `using-datavault4dbt` on its own. Editing a `SKILL.md` takes effect immediately in the
next session.

### Other agents (Cursor, Cline, Copilot, …)

Any agent that supports the [Agent Skills](https://agentskills.io/home) format works the same way: point
its skills directory at the folders under `skills/datavault4dbt/skills/`. Check your client's docs for
where that directory lives.

### Updating

```bash
git pull                 # symlinked installs pick this up automatically
```

If you copied instead of symlinking, re-run the `cp` after pulling.

## Available skills

| Skill | Status | Description |
|-------|--------|-------------|
| `using-datavault4dbt` | ✅ shipped | Build Data Vault models with datavault4dbt — project layout, choosing entities, and the YAML-metadata macro pattern. Entry point that routes to detailed references (staging, hubs/links, satellites, business vault, conventions). |
| `configuring-datavault4dbt` | ✅ shipped | Install the package, copy global variables into `dbt_project.yml`, hash/naming settings, per-adapter setup. |
| `testing-a-datavault4dbt-project` | ✅ shipped | Data Vault 2 technical tests — hashkey uniqueness/not-null, link→hub referential integrity, satellite key+load-date uniqueness. |
| `rehashing-datavault4dbt-entities` | ✅ shipped | Recalculate hashkeys/hashdiffs after a hash-config change or v1→v2 upgrade, safely and in order. |
| `troubleshooting-datavault4dbt` | ✅ shipped | Diagnose common failures — change-detection, high-water-mark, ghost-record, and YAML-metadata issues. |
| `building-business-vault-with-datavault4dbt` | 🛠 planned (under consideration) | Standalone PIT / snapshot-control skill, if PIT work proves common (currently a `using-datavault4dbt` reference). |

## Prerequisites

Most skills assume:

- dbt is installed and a project with `dbt_project.yml` exists.
- The [datavault4dbt](https://github.com/ScalefreeCOM/datavault4dbt) package is (or will be) installed
  via `packages.yml`.
- Basic familiarity with dbt (models, sources, packages) and Data Vault 2 concepts.

## Compatible agents

These skills work with any AI agent that supports the [Agent Skills](https://agentskills.io/home)
format (Claude Code, Cursor, and others).

## Contributing

See the [Contributing Guide](CONTRIBUTING.md). All skills follow the
[Agent Skills specification](https://agentskills.io/specification).

## Resources

- [Official datavault4dbt Website](https://datavault4dbt.com)
- [datavault4dbt on GitHub](https://github.com/ScalefreeCOM/datavault4dbt)
- [dbt Documentation](https://docs.getdbt.com/)
- [Agent Skills Documentation](https://agentskills.io/home)

## License

See [LICENSE](LICENSE) for details (Apache-2.0).
