# datavault4dbt Agent Skills

A curated collection of [Agent Skills](https://agentskills.io/home) for the
[datavault4dbt](https://github.com/ScalefreeCOM/datavault4dbt) dbt package. These skills help AI agents
build **Data Vault 2** warehouses correctly — staging, hubs, links, satellites, and business-vault
entities — across all adapters datavault4dbt supports.

Maintained by [Scalefree](https://www.scalefree.com/).

---

## 🚧 Pre-release installation (internal rollout)

> **Temporary.** These skills are not yet published to any public registry (skills.sh, Tessl, the
> Cursor marketplace). Until then, install **directly from this repository** using one of the methods
> below. Once published, use the standard [Installation](#installation) section instead — this block
> will be removed.

Because the repo may be **private** during the internal rollout, make sure your git access is set up
first (`gh auth login`, an SSH key loaded in `ssh-agent`, or a `GITHUB_TOKEN`/`GH_TOKEN` env var for
non-interactive/background updates). Claude Code clones the repo with your existing git credentials.

### Claude Code — straight from the repo

```bash
# Add this repo as a plugin marketplace (reads .claude-plugin/marketplace.json from the repo)
/plugin marketplace add ScalefreeCOM/datavault4dbt-agent-skills
# Optional: pin to a branch or tag → ScalefreeCOM/datavault4dbt-agent-skills@main

# Install the plugin from that marketplace
/plugin install datavault4dbt@datavault4dbt-agent-marketplace

# Verify
/plugin marketplace list
/plugin list
```

Update / remove later with `/plugin update datavault4dbt@datavault4dbt-agent-marketplace` and
`/plugin uninstall datavault4dbt@datavault4dbt-agent-marketplace`.

### Claude Code — from a local clone (fully offline / air-gapped)

```bash
git clone https://github.com/ScalefreeCOM/datavault4dbt-agent-skills.git
# Point the marketplace at the local checkout
/plugin marketplace add ./datavault4dbt-agent-skills
/plugin install datavault4dbt@datavault4dbt-agent-marketplace
```

### Claude Code — manual fallback (no plugin system)

Copy the individual skill folders into a skills directory Claude Code auto-discovers — project scope
`.claude/skills/` (loads after you trust the workspace) or user scope `~/.claude/skills/` (loads in
every project):

```bash
git clone https://github.com/ScalefreeCOM/datavault4dbt-agent-skills.git
mkdir -p ~/.claude/skills
cp -r datavault4dbt-agent-skills/skills/datavault4dbt/skills/* ~/.claude/skills/
```

Each skill keeps its `SKILL.md`; editing it takes effect immediately in the session.

### Cursor / other agents — Vercel Skills CLI from the repo

```bash
# Works against the GitHub repo before public listing (private repo needs git access)
npx skills add ScalefreeCOM/datavault4dbt-agent-skills            # all skills
npx skills add ScalefreeCOM/datavault4dbt-agent-skills --skill using-datavault4dbt
```

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

> Once the skills are published to the public registries, use the commands below. During the internal
> rollout, follow [Pre-release installation](#-pre-release-installation-internal-rollout) above instead.

### Claude Code

```bash
# Add the marketplace
/plugin marketplace add ScalefreeCOM/datavault4dbt-agent-skills

# Install the datavault4dbt skills
/plugin install datavault4dbt@datavault4dbt-agent-marketplace
```

### Other AI clients (Cursor, Cline, Copilot, …) via the Vercel Skills CLI

```bash
# Preview available skills
npx skills add ScalefreeCOM/datavault4dbt-agent-skills --list

# Install all skills
npx skills add ScalefreeCOM/datavault4dbt-agent-skills

# Install a specific skill
npx skills add ScalefreeCOM/datavault4dbt-agent-skills --skill using-datavault4dbt
```

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

- [datavault4dbt on GitHub](https://github.com/ScalefreeCOM/datavault4dbt)
- [dbt Documentation](https://docs.getdbt.com/)
- [Agent Skills Documentation](https://agentskills.io/home)

## License

See [LICENSE](LICENSE) for details (Apache-2.0).
