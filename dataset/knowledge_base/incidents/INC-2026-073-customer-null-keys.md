# INC-2026-073 Customer Null Keys

Pipeline: customers_daily_pipeline
Impact: dim_customers test failed because 2.1% of rows had null customer_id.
Root cause: CRM export bug produced header-shifted rows after an embedded newline in address.
Resolution: quarantine malformed CSV records, fix producer escaping, rerun extract and validate primary-key completeness before publish.
