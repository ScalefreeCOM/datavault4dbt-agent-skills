# Project layout & materializations

datavault4dbt projects are built in layers. A common, proven layout (mirroring the `finance-dbt-demo`
reference project):

```
models/
├── 00_control/        # snapshot control tables (control_snap_v0/v1)        → table
├── 01_sources/        # source definitions + any batch/union shaping        → view
├── 02_staging/        # one stage model per source table (datavault4dbt.stage) → view
├── 03_raw_vault/      # hubs, links, satellites, non-historized links       → incremental
└── 04_info_delivery/  # dims, facts, marts built from the vault             → table
```

Configure materializations per layer in `dbt_project.yml`:

```yaml
models:
  my_project:
    01_sources:      {+schema: source_data,  +materialized: view}
    02_staging:      {+schema: stage,         +materialized: view}
    03_raw_vault:    {+schema: rdv,           +materialized: incremental}
    04_info_delivery:{+schema: info_delivery, +materialized: table}
    00_control:      {+schema: control,       +materialized: table}
```

## Materialization rules of thumb

| Entity | Materialization | Why |
|--------|-----------------|-----|
| Staging | `view` | Recomputed each run; no need to persist |
| Hub / Link / NH-Link | `incremental` | Insert-only; high-water mark appends new rows |
| Satellite v0 | `incremental` | Insert-only history |
| Satellite v1 (load-end-date) | `view` | Virtualized end-dating on top of v0; no storage needed |
| PIT | `incremental` (+ cleanup post-hook) | Snapshot-based, append per active snapshot |
| Snapshot control | `incremental` / `view` (v0 / v1) | Drives PITs |
| Dims / Facts | `table` | End-user query performance |

## Build order

```bash
dbt deps                                  # install datavault4dbt
dbt seed                                  # if sources come from seeds
dbt run --select 02_staging               # staging first
dbt run --select 03_raw_vault             # then raw vault
dbt run --select 04_info_delivery         # then delivery
# or, end to end:
dbt build                                 # run + test everything
```

Each raw-vault entity depends on its staging model, so `dbt build --select stg_account+` builds a
stage and everything downstream of it, running tests along the way.

## Naming the models (demo convention)

- Staging: `stg__<source>__<table>` (e.g. `stg__crm__src_crm_customers`)
- Hub: `<entity>_h` · Link: `<…>_l` · Non-historized link: `<…>_nl`
- Satellite: `<entity>_<source>_<class>_s_v0` / `_v1` — the `<class>` token lets you split one hub's
  attributes into multiple satellites (e.g. a non-PII `n` satellite and a PII `p` satellite).

Adopt whatever convention the client project already uses; consistency matters more than the exact
tokens.
