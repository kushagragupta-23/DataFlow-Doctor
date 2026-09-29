# Data Platform Architecture

The analytics platform ingests ecommerce, payments, CRM, and marketing data into the `raw` layer. Airflow orchestrates batch jobs. dbt transforms raw tables into staging and marts. Spark handles large clickstream jobs. Great Expectations checks data quality before publishing business tables.

Critical lineage: `raw.orders` -> `stg_orders` -> `fct_orders` -> `mart_daily_revenue`. `raw.customers` -> `stg_customers` -> `dim_customers`. `raw.events` -> Spark sessionization -> `fct_sessions` -> `mart_funnel`.

Production jobs use UTC. Source extracts may arrive in local time and must be normalized before joins.
