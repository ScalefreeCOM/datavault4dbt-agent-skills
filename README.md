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

### Claude Code (plugin install — recommended)

```bash
# Add the marketplace once
claude plugin marketplace add ScalefreeCOM/datavault4dbt-agent-skills

# Install the plugin
claude plugin install datavault4dbt@datavault4dbt-agent-skills
```

The plugin loads into every Claude Code session automatically. To update:

```bash
claude plugin update datavault4dbt@datavault4dbt-agent-skills
```

### Claude Code (manual install — for offline or frozen snapshots)

Clone the repository and symlink the plugin directory into your skills folder:

```bash
git clone https://github.com/ScalefreeCOM/datavault4dbt-agent-skills.git
cd datavault4dbt-agent-skills

# User scope (available in every project)
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/datavault4dbt
```

Or load it for a single session:

```bash
claude --plugin-dir /path/to/datavault4dbt-agent-skills
```

`git pull` inside the clone keeps symlinked installs up to date.

### Verify

Start a session in a dbt project and ask something like *"add a customer hub with datavault4dbt"* — the
agent should load `using-datavault4dbt` on its own.

### Other agents (Cursor, Cline, Copilot, …)

Any agent that supports the [Agent Skills](https://agentskills.io/home) format works the same way: point
its skills directory at the folders under `skills/datavault4dbt/skills/`. Check your client's docs for
where that directory lives.

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
