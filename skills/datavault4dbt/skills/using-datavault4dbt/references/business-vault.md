# Business vault: PITs & snapshot control

PIT (Point-in-Time) tables pre-assemble, for each snapshot date, which satellite rows are active for
each hub key — collapsing many joins into one fast lookup for the delivery layer. They are driven by a
**snapshot control** table.

## Snapshot control (`control_snap_v0` / `control_snap_v1`)

The control table defines the set of snapshot dates and which are "active" (via a trigger column,
default `is_active`). PITs read this to know which snapshots to materialize.

- `control_snap_v0` — the base control table (incremental).
- `control_snap_v1` — a view layer on top.

Read `dbt_packages/datavault4dbt/docs/01_macro-instructions/22_business-vault/24_snapshot-control/`
for parameters; `first_day_of_week` (global var) is adapter-specific.

## PIT (`datavault4dbt.pit`) — incremental

| Parameter | Required | Meaning |
|-----------|----------|---------|
| `tracked_entity` | yes | The hub model this PIT tracks |
| `hashkey` | yes | The hub's hashkey column |
| `sat_names` | yes | The satellites to include — refer to the **v1** satellites (they carry the load-end-date). Supports standard and nh satellites. |
| `snapshot_relation` | yes | The snapshot control model |
| `dimension_key` | yes | Name of the PIT dimension key; convention is `<hashkey>_d` |
| `snapshot_trigger_column` | important | The boolean column in the snapshot relation selecting active snapshots (e.g. `is_active`) |
| `pit_type` | optional | Literal label for the `pit_type` column (prefix with `!`, e.g. `!Regular PIT`) |
| `custom_rsrc` | optional | Literal record source for the PIT (business-vault entities don't use the technical rsrc) |
| `ldts` / `ledts` / `sdts` | optional | Override the alias names if needed |
| `snapshot_optimization` | optional | Snowflake-only; incremental speedup, requires a `unique_key` config |

Always attach the **cleanup post-hook** so superseded PIT rows are removed:

```sql
{{ config(materialized='incremental',
          post_hook="{{ datavault4dbt.clean_up_pit('control_snap_v1') }}") }}

{%- set yaml_metadata -%}
pit_type: '!Regular PIT'
tracked_entity: 'account_h'
hashkey: 'hk_account_h'
sat_names:
    - account_n_s_v1
    - account_p_s_v1
snapshot_relation: 'control_snap_v1'
snapshot_trigger_column: 'is_active'
dimension_key: 'hk_account_d'
{%- endset -%}

{{ datavault4dbt.pit(yaml_metadata=yaml_metadata) }}
```

See `docs/.../22_business-vault/22_pit/23_hook-cleanup-pits.md` for the hook.

## Dimensions & facts

datavault4dbt stops at the raw + business vault; the delivery layer (dims, facts, marts) is plain dbt
SQL you write yourself, querying the hubs/links/satellites (often through PITs for performance).
Materialize these as `table`. This is where harmonization and business rules live — not in staging.

## Out of common scope

PITs and snapshot control are the business-vault entities the package generates. Bridges, full
multi-active business logic, and reference-vault delivery are project-specific; consult the package
docs and the client's standards before building them.
