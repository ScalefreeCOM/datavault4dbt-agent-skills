# Evals

A/B harness for measuring whether the datavault4dbt skills actually improve agent output.

Each scenario describes a task, the context files the agent may read, and a grading rubric. You run the
same task with different **skill sets** (e.g. baseline = no skills, vs. with `using-datavault4dbt`) and
compare the results.

```
evals/
├── scenarios/
│   └── <scenario-name>/
│       ├── scenario.md       # task description + grading criteria
│       ├── skill-sets.yaml   # the skill/tool combinations to compare
│       └── context/          # files the agent is given (e.g. a source CSV, a dbt_project.yml)
├── runs/                     # outputs (gitignored)
└── reports/                  # generated comparisons (gitignored)
```

## Writing a scenario

- `scenario.md` — state the task and concrete, checkable grading criteria (e.g. "the hub uses
  `materialized='incremental'`", "the satellite `src_payload` matches the staging hashdiff inputs").
- `skill-sets.yaml` — define a `baseline` set (no skills) and one or more sets that load the skill(s)
  under test, with the `allowed_tools` each may use.

The strongest grading criteria are the ones the agent gets wrong without the skill: the static-`!`
record source, the per-layer materializations, `rsrc_static` on multi-source entities, and keeping a
satellite's payload in sync with its hashdiff.

> A tool to execute these scenarios is not bundled yet. Until then, scenarios double as a manual test
> checklist: run the task in a fresh agent session with and without the skill and grade by hand.
