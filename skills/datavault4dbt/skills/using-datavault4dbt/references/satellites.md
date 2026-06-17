# Satellites

Satellites hold descriptive context for a hub or link, tracked over time. Split by source system (one
satellite per source) and often by rate of change or sensitivity. The standard pattern is a `sat_v0`
(incremental, stores history) with a `sat_v1` (view, adds a virtual load-end-date) on top.

## Standard satellite v0 (`datavault4dbt.sat_v0`) — incremental

| Parameter | Required | Meaning |
|-----------|----------|---------|
| `parent_hashkey` | yes | Hashkey of the hub/link this satellite hangs off |
| `source_model` | yes | The staging model |
| `src_payload` | optional | Descriptive attribute columns (see the three modes below) |
| `src_hashdiff` | optional | Hashdiff column from staging; required when `src_payload` has 2+ columns |
| `src_ldts` / `src_rsrc` | optional | Override ldts/rsrc alias names |
| `disable_hwm` | optional | Turn off the high-water mark |
| `source_is_single_batch` | optional | Skip the dedup `QUALIFY` — only if the stage holds one row per entry |
| `additional_columns` | optional | Extra columns to add |

**Payload modes:**

1. **Multiple attributes + hashdiff** (classic) — provide `src_payload` (2+) *and* `src_hashdiff`.
   The payload columns must be exactly the hashdiff's input columns.
2. **Single attribute, no hashdiff** — one `src_payload` column, omit `src_hashdiff`; change detection
   runs directly on that column. Good for a lone status/flag.
3. **No payload** — omit both; the satellite records only that/when a hashkey appeared (plus any
   `additional_columns`). For pure appearance tracking, prefer the record-tracking satellite.

```sql
{{ config(materialized='incremental') }}
{%- set yaml_metadata -%}
parent_hashkey: 'hk_account_h'
src_hashdiff: 'hd_account_s'
src_payload: [name, address, phone, email]   -- must equal the hashdiff inputs in staging
source_model: 'stg_account'
{%- endset -%}
{{ datavault4dbt.sat_v0(yaml_metadata=yaml_metadata) }}
```

## Standard satellite v1 (`datavault4dbt.sat_v1`) — view

Adds a virtualized load-end-date (and optional current flag) on top of a v0 satellite. Create one v1
per v0; needed for PITs.

| Parameter | Required | Meaning |
|-----------|----------|---------|
| `sat_v0` | yes | Name of the underlying v0 satellite model |
| `hashkey` | yes | Same parent hashkey as the v0 |
| `hashdiff` | optional | The v0's hashdiff; omit for single-attribute/no-payload v0 sats |
| `ledts_alias` | optional | Name for the load-end-date column |
| `add_is_current_flag` | optional | Adds an `is_current` boolean (default `False`) |
| `include_payload` | optional | Whether to carry the v0 payload columns (default `True`) |

```sql
{{ config(materialized='view') }}
{%- set yaml_metadata -%}
sat_v0: 'account_v0_s'
hashkey: 'hk_account_h'
hashdiff: 'hd_account_s'
ledts_alias: 'loadenddate'
add_is_current_flag: true
{%- endset -%}
{{ datavault4dbt.sat_v1(yaml_metadata=yaml_metadata) }}
```

## Specialized variants

These follow the same staging-driven pattern but have their own parameters. **Read the package doc
before using them** — don't assume the parameter set matches `sat_v0`.

| Variant | Macro | Purpose | Doc |
|---------|-------|---------|-----|
| Multi-active | `ma_sat_v0` / `ma_sat_v1` | Several active rows per key at once (e.g. multiple phones); needs `multi_active_config` set in staging | `docs/.../10_satellites/12_multi-active-satellites/` |
| Effectivity | `eff_sat_v0` | Tracks active/inactive periods of a relationship | `docs/.../10_satellites/14_effectivity-satellites/` |
| Record-tracking | `rec_track_sat` | Records that/when a key appeared, across sources (uses `rsrc_static`) | `docs/.../10_satellites/15_record-tracking-satellites/` |
| Non-historized | `nh_sat` | Immutable payload on a hub/link without history | `docs/.../10_satellites/16_non-historized-satellites/` |

(Paths are under `dbt_packages/datavault4dbt/docs/01_macro-instructions`.)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `src_payload` ≠ the satellite's hashdiff inputs | Keep them identical — that's what change detection compares |
| Adding a hashdiff for a single-column satellite | Not needed; omit `src_hashdiff` and let change detection run on the column |
| Materializing v1 as a table | v1 is a virtual end-date layer — use `view` |
| One giant satellite per hub | Split by source, and by rate-of-change / sensitivity, for cleaner history and PIT performance |
