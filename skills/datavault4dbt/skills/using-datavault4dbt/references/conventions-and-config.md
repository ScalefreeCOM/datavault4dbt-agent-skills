# Conventions & configuration

## Installing the package

`packages.yml`:

```yaml
packages:
  - package: ScalefreeCOM/datavault4dbt
    version: [">=1.9.0", "<2.0.0"]   # 1.9+ allows passing yaml_metadata directly (recommended)
```

Then `dbt deps`. The package's defaults live in `dbt_packages/datavault4dbt/dbt_project.yml`.

## Global variables

datavault4dbt is configured through global variables, all prefixed `datavault4dbt.`. To override a
default, copy the variable into your own project's `dbt_project.yml` under `vars:`. The most commonly
adjusted ones:

### Column aliases (names of the technical columns the package generates)

| Variable | Default | Meaning |
|----------|---------|---------|
| `ldts_alias` | `ldts` | Load date timestamp column in all DV entities |
| `rsrc_alias` | `rsrc` | Record source column |
| `ledts_alias` | `ledts` | Load-end date in v1 satellites |
| `sdts_alias` | `sdts` | Snapshot date in snapshot tables and PITs |
| `is_current_col_alias` | `is_current` | Current-row flag in v1 satellites |
| `stg_alias` | `stg` | Staging-model marker in record-tracking satellites |

### Hash configuration

| Variable | Default | Meaning |
|----------|---------|---------|
| `hash` | `MD5` | Algorithm: `MD5`, `SHA1`, or `SHA2`. MD5 is fine for dev/workshops; prefer SHA for production collision-resistance |
| `hash_datatype` | adapter-specific | Datatype of hash columns; must fit the algorithm output |
| `hashkey_input_case_sensitive` | `FALSE` | Business-key input case sensitivity for hashkeys |
| `hashdiff_input_case_sensitive` | `TRUE` | Descriptor input case sensitivity for hashdiffs |
| `hashdiff_use_trim` | `TRUE` | Whether hashdiff inputs are wrapped in `TRIM()` |

> Changing `hash`/`hash_datatype` after data is loaded changes every hashkey and hashdiff. Use the
> package's rehashing macros to migrate rather than dropping and reloading.

### Ghost records, zero keys, technical timestamps

`beginning_of_all_times` / `end_of_all_times` (and their `_date` forms) plus `timestamp_format` define
the technical date range used for ghost records and end-dating. `default_unknown_rsrc` /
`default_error_rsrc` and the per-datatype error/unknown values control ghost-record contents. These
default per adapter — don't hard-code timestamps; rely on the variables.

For the complete list, read `dbt_packages/datavault4dbt/docs/26_general-usage-notes/29_global-variables`.

## Naming conventions

| Object | Pattern | Example |
|--------|---------|---------|
| Hub hashkey | `hk_<entity>_h` | `hk_account_h` |
| Link hashkey | `hk_<a>_<b>_l` | `hk_opportunity_account_l` |
| Non-historized link hashkey | `hk_<…>_nl` | `hk_creditcard_transactions_nl` |
| Satellite hashdiff | `hd_<entity>_s` | `hd_account_s` |
| PIT dimension key | `<hashkey>_d` | `hk_account_d` |

These are conventions, not hard requirements — but datavault4dbt's docs and examples follow them, and
the satellite/PIT macros read more clearly when you do. Match an existing client project's scheme if it
already has one.

## Static strings need a leading `!`

Anywhere a macro accepts a *literal* value instead of a column reference, prefix it with `!`:

- `rsrc: '!SAP.account'` in staging (a constant record source)
- `pit_type: '!Regular PIT'` in a PIT

Without the `!`, the value is treated as a column name and compilation fails or picks the wrong column.

## Supported adapters

BigQuery, Snowflake, Redshift, PostgreSQL, Databricks, Trino, Exasol, Oracle, SQL Server, Synapse,
Fabric. Several defaults (timestamp formats, datatypes, wildcard syntax for `rsrc_static`, first day of
week) differ per adapter — check
`dbt_packages/datavault4dbt/docs/26_general-usage-notes/33_adapter-specific-notes/<adapter>` when a
project targets a specific warehouse.
