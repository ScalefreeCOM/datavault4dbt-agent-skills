# Releasing

This document covers how updates to this repository are published to plugin marketplaces.

## Before releasing

Bump the `version` field in each plugin manifest that changed, and keep the Claude and Cursor
manifests in sync:

| Plugin | Manifest files |
|--------|----------------|
| datavault4dbt | `skills/datavault4dbt/.claude-plugin/plugin.json`, `skills/datavault4dbt/.cursor-plugin/plugin.json` |
| tessl (all plugins) | `tile.json` |

Generate the changelog from the unreleased entries:

```bash
changie batch <version>
changie merge
```

## Claude marketplace

The Claude marketplace scans this repository automatically — no manual action after merging to `main`.
Users install with:

```bash
/plugin marketplace add ScalefreeCOM/datavault4dbt-agent-skills
/plugin install datavault4dbt@datavault4dbt-agent-marketplace
```

## Cursor plugin marketplace

After merging to `main`, notify the Cursor marketplace team to sync the listing (see Cursor's plugin
publishing instructions). Keep `.cursor-plugin/` manifests in sync with `.claude-plugin/`.

## Vercel Skills CLI / skills.sh

[skills.sh](https://skills.sh) scans the repository automatically. Skills are also installable via the
Vercel Skills CLI (`npx skills add ScalefreeCOM/datavault4dbt-agent-skills`).

## Tessl

[Tessl](https://tessl.io) can ingest this repository's skills via `tile.json`. If a publishing GitHub
Action is configured, it submits on merge to `main`; otherwise submit manually. Bump the `version` in
`tile.json` before releasing.
