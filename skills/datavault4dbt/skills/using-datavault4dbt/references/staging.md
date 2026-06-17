# Staging (`datavault4dbt.stage`)

The staging layer is for **hashing** and light shaping (derived columns, prejoins, NULL placeholders
for missing columns). It is **not** for harmonization or business logic. Create **one stage per source
table**. Materialize as a `view`.

## Required parameters

| Parameter | Meaning |
|-----------|---------|
| `ldts` | Column (or SQL expression) holding the load date timestamp. If omitted, the package's `current_timestamp` is used. |
| `rsrc` | Column, SQL expression, or static string for the record source. A static string must start with `!` (e.g. `!SAP.account`). |
| `source_model` | The upstream dbt model name (string), or a `{source_name: source_table}` dict to read from a dbt `source()`. |

## Key optional parameters

| Parameter | Meaning |
|-----------|---------|
| `hashed_columns` | Defines every hashkey and hashdiff. Hashkey value = list of business keys. Hashdiff value = a dict with `is_hashdiff: true` and `columns: [...]`. Optional per-hashdiff `use_trim` / `use_rtrim` override the global trim behavior. |
| `derived_columns` | Calculated columns: each has a `value` (a source column, a SQL expression, or a `!literal`) and a `datatype`. |
| `prejoined_columns` | Left-joins to other source tables to pull in a business key for a link/hub. Each entry needs `src_name`, `src_table`, `bk`, `this_column_name`, `ref_column_name`. |
| `missing_columns` | Adds NULL columns (name → SQL datatype) so hashdiffs/payloads don't break when a source column disappears. |
| `multi_active_config` | For multi-active sources: `multi_active_key` (the column[s] making rows unique per key+ldts) and `main_hashkey_column`. Omit for single-active stages. |
| `enable_ghost_records` | Default `True`. Creates the unknown/error ghost records used for referential safety. Disables both at once when `False`. |
| `include_source_columns` | Default `True`. Whether all source columns flow through, or only the generated ones. |

## Hashed columns: the central idea

Define **one hashkey per hub** the source feeds, **one link hashkey per link** the source feeds, and
**one hashdiff per satellite** the source feeds. Downstream macros only reference these names.

```sql
{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: 'src_account'
ldts: 'edwLoadDate'
rsrc: 'edwRecordSource'
hashed_columns:
    hk_account_h:                         # hub hashkey
        - account_number
        - account_key
    hd_account_s:                         # satellite hashdiff
        is_hashdiff: true
        columns: [name, address, phone, email]
    hk_account_contract_l:                # link hashkey (all BKs of the connected hubs)
        - account_number
        - contractnumber
{%- endset -%}

{{ datavault4dbt.stage(yaml_metadata=yaml_metadata) }}
```

**The cardinal rule:** a satellite's `src_payload` must be exactly the columns listed in that
satellite's hashdiff. If they drift, change detection silently breaks.

## Derived, prejoined, missing columns (richer example)

```yaml
derived_columns:
    conversion_duration:
        value: 'TIMESTAMP_DIFF(conversion_date, created_date, DAY)'
        datatype: 'INT64'
    country_isocode:
        value: '!GER'                     # static value → leading !
        datatype: 'STRING'
prejoined_columns:
    contractnumber:                       # pull a link BK from another source table
        src_name: 'source_data'
        src_table: 'contract'
        bk: 'contractnumber'
        this_column_name: 'ContractId'
        ref_column_name: 'Id'
missing_columns:
    legacy_account_uuid: 'INT64'          # column that disappeared from the source
```

- **derived_columns** — compute a value, duplicate/rename a column, or inject a literal.
- **prejoined_columns** — make a foreign business key available so a link hashkey can be hashed in
  staging. For self-prejoins or repeated objects, alias the result to avoid duplicate column names.
- **missing_columns** — add NULL stand-ins so hashdiff/payload definitions stay stable across schema
  changes.

## Notes

- `ldts` and `rsrc` can be SQL expressions, e.g. `rsrc: "CONCAT(source_system, '||', source_object)"`.
- Multi-active staging requires that `business_keys + multi_active_key + ldts` is unique per row. If
  the source has no natural multi-active key, generate one (e.g. `ROW_NUMBER()`) one layer earlier.
- Read the full docs in `dbt_packages/datavault4dbt/docs/01_macro-instructions/02_staging/` (staging,
  prejoining, derived-columns, add-new-columns-to-hashdiff).
