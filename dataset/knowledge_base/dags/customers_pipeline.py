# DAG: customers_daily_pipeline
# tasks: extract_customers -> validate_customer_schema -> load_raw_customers -> build_dim_customers
# primary key: customer_id
# source: crm_postgres
