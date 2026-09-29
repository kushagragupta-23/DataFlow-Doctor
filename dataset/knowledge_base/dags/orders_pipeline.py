from airflow import DAG
# DAG: orders_daily_pipeline
# schedule: 02:00 UTC daily
# tasks: extract_orders -> validate_orders_schema -> load_raw_orders -> transform_orders -> publish_revenue_mart
# retry_delay_minutes: 10
# owner: data-platform

EXPECTED_COLUMNS = ["order_id", "customer_id", "order_ts", "amount", "currency", "status"]
