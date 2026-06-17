# Scenario: build a customer hub + satellite from a flat source

## Task

The project has a staging-ready source table `src_crm_customers` with columns:
`CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, CITY, CUSTOMER_SEGMENT, LOAD_DATE`, record source
`CRM.customers`.

Using datavault4dbt, create:
1. a staging model that computes the customer hub hashkey and one satellite hashdiff,
2. a customer hub, and
3. a standard satellite (v0) for the customer attributes.

## Grading criteria

| # | Criterion | Pass condition |
|---|-----------|----------------|
| 1 | Staging materialization | staging model uses `materialized='view'` |
| 2 | Hashkey defined in staging | `hashed_columns` defines `hk_customer_h` from `CUSTOMER_ID` |
| 3 | Hashdiff defined in staging | a hashdiff (e.g. `hd_customer_s`) with `is_hashdiff: true` and the payload columns |
| 4 | Static record source | `rsrc` is a static string prefixed with `!` (e.g. `!CRM.customers`) |
| 5 | Hub macro & materialization | hub calls `datavault4dbt.hub`, `materialized='incremental'`, `business_keys: [CUSTOMER_ID]` |
| 6 | Satellite payload matches hashdiff | `sat_v0` `src_payload` is exactly the columns fed into the hashdiff |
| 7 | YAML-metadata pattern | all three use a `{%- set yaml_metadata -%}` block passed to the macro |

A baseline run (no skill) typically misses #4, #1/#5 materializations, and #6.
