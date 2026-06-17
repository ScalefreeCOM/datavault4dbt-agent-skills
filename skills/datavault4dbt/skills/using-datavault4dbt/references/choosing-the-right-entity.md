# Choosing the right Data Vault entity

Use this to map a source table to datavault4dbt entities. The package generates the SQL; your job is
the modeling decision.

## Hubs — the business keys

Create a **hub** for each distinct business concept identified by a stable business key (customer,
contract, product, account). The hub stores only the hashkey, business key(s), `ldts`, and `rsrc`.

- One business key → one hub.
- The same hub can be loaded from multiple sources (each must supply the same number of BK columns and
  a `rsrc_static`).
- Ask "is this key stable and meaningful to the business?" If yes → hub. If it only exists to relate
  other keys, it belongs in a link, not a hub.

## Links — the relationships

Create a **link** to connect two or more hubs (or a hub to itself). The link hashkey is hashed from all
the connected business keys.

- **Standard `link`** — historized relationship; every new combination is appended. Use for
  associations that can change over time and that you want a full audit trail of.
- **Non-historized `nh_link`** — a link that also carries descriptive `payload` columns inline (the
  former "transactional link"). Use for immutable events/transactions: payments, clicks, sensor
  readings. The payload lives on the link; no separate satellite is needed.

Decision: does the relationship carry event attributes that never change after the fact (amount,
timestamp, channel)? → `nh_link`. Is it a pure association whose descriptive context lives elsewhere
and may change? → `link` (+ satellites if needed).

## Satellites — the descriptive context

Attach a **satellite** to a hub or link to store descriptive attributes over time. Split satellites by
**source system** and often by **rate of change** or **sensitivity** (e.g. a PII satellite separate
from a non-PII one). datavault4dbt offers several variants:

| Variant | Macro | Use when |
|---------|-------|----------|
| Standard | `sat_v0` (+ `sat_v1`) | The normal case: track attribute history with a hashdiff. `sat_v1` adds a virtual load-end-date for PITs. |
| Multi-active | `ma_sat_v0` / `ma_sat_v1` | Multiple active rows per key at once (e.g. several phone numbers). |
| Effectivity | `eff_sat_v0` | Track when a relationship is active/inactive over time. |
| Record-tracking | `rec_track_sat` | Only record *that* and *when* a key appeared in a source, across sources. |
| Non-historized | `nh_sat` | Immutable payload attached to a hub/link where history isn't tracked. |

See [satellites.md](satellites.md) for parameters.

## Reference data

For code/lookup tables (currencies, country codes), the package has a parallel set: `ref_hub`,
`ref_sat_v0`/`ref_sat_v1`, and `ref_table`. Read
`dbt_packages/datavault4dbt/docs/01_macro-instructions/17_reference-data/` before using them.

## Worked decisions (from a banking/insurance source set)

- `CUSTOMER_ID`, `CONTRACT_ID`, `PRODUCT_ID`, `AGENT_ID` → four hubs.
- A contract that references a customer, product, and agent → one historized `link` across those hubs.
- Customer attributes split: a non-PII satellite (segment, risk band) and a PII satellite (name,
  email) off the customer hub — both `sat_v0` + `sat_v1`.
- Transactions (immutable financial events with amount/type/date) → an `nh_link` between contract and
  customer hubs, with the transaction attributes as payload. No satellite needed.

When a column like `CUSTOMER_ID` appears denormalized on a transaction source, decide whether to load
it as a third foreign key on the link or derive it via the contract relationship — both are valid; pick
based on whether the business treats it as part of the event's grain.
