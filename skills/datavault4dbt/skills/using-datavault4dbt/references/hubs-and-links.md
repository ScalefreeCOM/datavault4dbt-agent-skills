# Hubs & links

All three macros (`hub`, `link`, `nh_link`) are insert-only, support multi-source loading, and use a
dynamic high-water mark (HWM) to only scan new source rows. Materialize as `incremental`.

## Hub (`datavault4dbt.hub`)

| Parameter | Required | Meaning |
|-----------|----------|---------|
| `hashkey` | yes | Hub hashkey column (from staging), the hub PK |
| `business_keys` | yes | BK column name(s); must match the hashkey inputs |
| `source_models` | yes | Single source: a string. Multi-source: a list of dicts (see below) |
| `disable_hwm` | no | Turn off the high-water mark (default `False`) |
| `src_ldts` / `src_rsrc` | no | Override the ldts/rsrc alias names if they differ from the globals |
| `additional_columns` | no | Extra columns to carry into the hub |

```sql
{{ config(materialized='incremental') }}
{%- set yaml_metadata -%}
hashkey: 'hk_account_h'
business_keys: [account_key, account_number]
source_models: stg_account
{%- endset -%}
{{ datavault4dbt.hub(yaml_metadata=yaml_metadata) }}
```

## Link (`datavault4dbt.link`)

| Parameter | Required | Meaning |
|-----------|----------|---------|
| `link_hashkey` | yes | Link hashkey (hashed from all connected business keys, in staging) |
| `foreign_hashkeys` | yes | List of the hub hashkeys this link connects |
| `source_models` | yes | String (single source) or list of dicts (multi-source) |
| `disable_hwm`, `src_ldts`, `src_rsrc`, `additional_columns` | no | As for hubs |

```sql
{{ config(materialized='incremental') }}
{%- set yaml_metadata -%}
link_hashkey: 'hk_opportunity_account_l'
foreign_hashkeys: ['hk_opportunity_h', 'hk_account_h']
source_models: stg_opportunity
{%- endset -%}
{{ datavault4dbt.link(yaml_metadata=yaml_metadata) }}
```

## Non-historized link (`datavault4dbt.nh_link`)

Same loading logic as `link`, plus inline `payload` columns. Use for immutable events/transactions.

| Parameter | Required | Meaning |
|-----------|----------|---------|
| `link_hashkey` | yes | NH-link hashkey |
| `payload` | yes | Descriptive attributes carried on the link |
| `source_models` | yes | String or list of dicts |
| `foreign_hashkeys` | recommended | Hub hashkeys it connects (may be empty, one, or many) |
| `union_strategy` | no | `ALL` (default) or `DISTINCT` for unioning multiple sources |
| `source_is_single_batch` | no | Performance: skips dedup `QUALIFY` — only if the stage has exactly one row per link hashkey |
| `disable_hwm`, `src_ldts`, `src_rsrc`, `additional_columns` | no | As above |

```sql
{{ config(materialized='incremental') }}
{%- set yaml_metadata -%}
link_hashkey: 'hk_creditcard_transactions_nl'
foreign_hashkeys: ['hk_creditcard_h']
payload: [transactionid, amount, currency_code, is_canceled, transaction_date]
source_models: stg_creditcard_transactions
{%- endset -%}
{{ datavault4dbt.nh_link(yaml_metadata=yaml_metadata) }}
```

## Multi-source loading & `rsrc_static`

When a hub/link/nh_link is loaded from several sources, pass a list of dicts to `source_models`. Each
dict has `name` and optionally `rsrc_static`, plus source-mapping keys (`hk_column`, `bk_columns` for
hubs; `link_hk`, `fk_columns` for links; `payload` for nh_links) when the input column names differ
between sources:

```sql
source_models:
    - name: stg_opportunity
      rsrc_static: '*/SALESFORCE/Opportunity/*'
    - name: stg_account
      rsrc_static: '*/SAP/Account/*'
      link_hk: 'hashkey_account_opportunity'   # source mapping: different input column names
      fk_columns: [hashkey_opportunity, hashkey_account]
```

`rsrc_static` is **required for the HWM to work on multi-source entities**. It is the static part of the
record-source value (with adapter wildcards, e.g. `*` in BigQuery) that identifies one source across
all its loads, so the package can compute the max load date *per source*. Cases:

- **No dynamic part** in `rsrc` → set `rsrc_static` to the whole literal value (no wildcards).
- **Multiple dynamic parts** → set `rsrc_static` to a list of wildcard expressions.
- **No static part at all** → omit `rsrc_static` (you lose the HWM speedup; consider reshaping `rsrc`).

To disable the HWM instead: single-source → `disable_hwm: true`; multi-source → simply omit
`rsrc_static`.
