# Airflow Connections

`ecommerce_mysql` uses a secret-managed password and TLS. `analytics_warehouse` uses service account `svc_airflow_etl`. Connection pool maximum is 20. Tasks should close connections after each batch.
