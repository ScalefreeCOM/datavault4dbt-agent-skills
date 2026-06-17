# datavault4dbt global variables

These are the package defaults (from `dbt_packages/datavault4dbt/dbt_project.yml`, package v2.0.0). Copy
the whole block into your project's `dbt_project.yml` under `vars:` and adjust. Re-check against the
installed package version — defaults can change between releases.

```yaml
vars:
  # Column aliases
  datavault4dbt.ldts_alias: 'ldts'
  datavault4dbt.rsrc_alias: 'rsrc'
  datavault4dbt.ledts_alias: 'ledts'
  datavault4dbt.snapshot_trigger_column: 'is_active'
  datavault4dbt.sdts_alias: 'sdts'
  datavault4dbt.stg_alias: 'stg'
  datavault4dbt.is_current_col_alias: 'IS_CURRENT'
  datavault4dbt.deleted_flag_alias: 'deleted_flag'

  # Hash configuration
  datavault4dbt.hash: 'MD5'
  datavault4dbt.hash_datatype: 'STRING'
  datavault4dbt.hashkey_input_case_sensitive: FALSE
  datavault4dbt.hashdiff_input_case_sensitive: TRUE
  datavault4dbt.hashdiff_use_trim: TRUE

  # Stage configuration
  datavault4dbt.copy_rsrc_ldts_input_columns: false

  # General configuration
  datavault4dbt.include_business_objects_before_appearance: false
  datavault4dbt.enable_static_analysis_overwrite: true
  datavault4dbt.multi_source_models__execution_aware_loading: true
  datavault4dbt.show_debug_logs: false

  # Default start of the week (1 = Monday, 2 = Sunday), per adapter
  datavault4dbt.first_day_of_week: {"snowflake": "1", "exasol": "1", "postgres": "1", "databricks": "1", "bigquery": "2", "synapse": "2", "fabric": "2", "oracle": "2", "redshift": "1", "sqlserver": "2"}

  # Ghost record / zero key technical timestamps, per adapter
  datavault4dbt.beginning_of_all_times: {"bigquery":"0001-01-01T00-00-01","snowflake":"0001-01-01T00:00:01", "exasol": "0001-01-01 00:00:01", "postgres": "0001-01-01 00:00:01", "redshift": "0001-01-01 00:00:01", "synapse": "1901-01-01T00:00:01", "fabric": "0001-01-01T00:00:01", "oracle":"0001-01-01 00:00:01", databricks: "0001-01-01 00:00:01", trino: "0001-01-01 00:00:01", "sqlserver": "1901-01-01T00:00:01"}
  datavault4dbt.end_of_all_times: {"bigquery":"8888-12-31T23-59-59","snowflake":"8888-12-31T23:59:59", "exasol": "8888-12-31 23:59:59", "postgres": "8888-12-31 23:59:59", "redshift": "8888-12-31 23:59:59", "synapse": "8888-12-31T23:59:59", "fabric": "8888-12-31T23:59:59", "oracle":"8888-12-31 23:59:59", databricks: "8888-12-31 23:59:59", trino: "8888-12-31 23:59:59", "sqlserver": "8888-12-31T23:59:59"}
  datavault4dbt.timestamp_format: {"bigquery":"%Y-%m-%dT%H-%M-%S","snowflake":"YYYY-MM-DDTHH24:MI:SS", "exasol": "YYYY-mm-dd HH:MI:SS", "postgres": "YYYY-MM-DD HH24:MI:SS", "redshift": "YYYY-MM-DD HH24:MI:SS", "synapse": 126, "fabric": 126, "oracle":"YYYY-MM-DD HH24:MI:SS", databricks: "yyyy-MM-dd HH:mm:ss", trino: "%Y-%m-%d %H:%i:%s", "sqlserver": 126}
  datavault4dbt.beginning_of_all_times_date: {"bigquery":"0001-01-01","snowflake":"0001-01-01", "exasol": "0001-01-01", "postgres": "0001-01-01", "redshift": "0001-01-01", "synapse": "1901-01-01", "fabric": "0001-01-01", "oracle":"0001-01-01", databricks: "0001-01-01", trino: "0001-01-01", "sqlserver": "1901-01-01"}
  datavault4dbt.end_of_all_times_date: {"bigquery":"8888-12-31","snowflake":"8888-12-31", "exasol": "8888-12-31", "postgres": "8888-12-31", "redshift": "8888-12-31", "synapse": "8888-12-31", "fabric": "8888-12-31", "oracle":"8888-12-31", databricks: "8888-12-31", trino: "8888-12-31", "sqlserver": "8888-12-31"}
  datavault4dbt.date_format: {"bigquery":"%Y-%m-%d","snowflake":"YYYY-MM-DD", "exasol": "YYYY-mm-dd", "postgres": "YYYY-MM-DD", "redshift": "YYYY-MM-DD", "synapse": "yyyy-MM-dd", "fabric": "yyyy-mm-dd", "oracle":"YYYY-MM-DD", databricks: "yyyy-mm-dd", trino: "%Y-%m-%d", "sqlserver": "yyyy-MM-dd"}
  datavault4dbt.default_unknown_rsrc: 'SYSTEM'
  datavault4dbt.default_error_rsrc: 'ERROR'

  # Datatype defaults, per adapter
  datavault4dbt.rsrc_default_dtype: {"bigquery":"STRING","snowflake":"VARCHAR", "exasol": "VARCHAR (2000000) UTF8", "postgres": "VARCHAR", "redshift": "VARCHAR", "synapse": "VARCHAR", "fabric": "VARCHAR(255)", "oracle":"VARCHAR2(40)", databricks: "STRING", trino: "VARCHAR", "sqlserver": "VARCHAR(255)"}
  datavault4dbt.timestamp_default_dtype: {"bigquery":"TIMESTAMP","snowflake":"TIMESTAMP_TZ", "exasol": "TIMESTAMP(3) WITH LOCAL TIME ZONE", "postgres": "TIMESTAMPTZ", "redshift": "TIMESTAMPTZ", "synapse": "datetimeoffset", "fabric": "datetime2(6)", "oracle":"TIMESTAMP WITH TIME ZONE", databricks: "TIMESTAMP", trino: "TIMESTAMP(6)", "sqlserver": "datetime2(7)"}
  datavault4dbt.stg_default_dtype: {"bigquery":"STRING","snowflake":"VARCHAR", "exasol": "VARCHAR (2000000) UTF8", "postgres": "VARCHAR", "redshift": "VARCHAR", "synapse": "VARCHAR", "fabric": "VARCHAR(255)", "oracle":"VARCHAR2(40)", databricks: "STRING", trino: "VARCHAR", "sqlserver": "VARCHAR(255)"}
  datavault4dbt.derived_columns_default_dtype: {"bigquery":"STRING","snowflake":"VARCHAR", "exasol": "VARCHAR (2000000) UTF8", "postgres": "VARCHAR", "redshift": "VARCHAR", "synapse": "VARCHAR", "fabric": "VARCHAR(255)", "oracle":"VARCHAR2(40)", databricks: "STRING", trino: "VARCHAR", "sqlserver": "VARCHAR(255)"}

  # Datatype-specific error / unknown values (ghost records)
  datavault4dbt.error_value__STRING: '(error)'
  datavault4dbt.error_value_alt__STRING: 'e'
  datavault4dbt.unknown_value__STRING: '(unknown)'
  datavault4dbt.unknown_value_alt__STRING: 'u'
  datavault4dbt.unknown_value__numeric: '-1'
  datavault4dbt.error_value__numeric: '-2'

  datavault4dbt.oracle_varchar_size: '32767'

  # Premium package
  datavault4dbt.use_premium_package: False
```

## Notes

- **Column aliases** set the names of the technical columns the package generates (`ldts`, `rsrc`,
  `ledts`, `sdts`, current-row flag, etc.). Change these to match a house standard, project-wide.
- **Hash configuration** governs hashkey/hashdiff generation. `hashkey_input_case_sensitive` defaults
  to `FALSE` (business keys compared case-insensitively); `hashdiff_input_case_sensitive` defaults to
  `TRUE`. `hashdiff_use_trim` wraps hashdiff inputs in `TRIM()`.
- **Ghost-record / zero-key** vars define the technical date range (`0001-01-01` … `8888-12-31`, with
  `1901-01-01` lower bound on Synapse/SQL Server) and the unknown/error placeholder values used for
  referential-safety ghost records. Don't hard-code these in models — rely on the vars.
- To change a per-datatype error/unknown value, set `datavault4dbt.<error|unknown>_value[_alt]__<TYPE>`
  (e.g. `datavault4dbt.error_value_alt__STRING`).
- For the authoritative, version-matched explanations, read
  `dbt_packages/datavault4dbt/docs/26_general-usage-notes/29_global-variables`.
