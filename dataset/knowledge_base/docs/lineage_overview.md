# Lineage Overview

`orders_ingestion` writes raw.orders. `orders_transform` reads raw.orders and writes analytics.stg_orders and analytics.fct_orders. `daily_revenue_mart` reads analytics.fct_orders and writes analytics.mart_daily_revenue.

`customer_ingestion` writes raw.customers. `customer_transform` writes analytics.dim_customers. `customer_360` joins analytics.dim_customers with analytics.fct_orders.

`clickstream_ingestion` writes raw.events. `sessionize_events` writes analytics.fct_sessions. `funnel_mart` reads analytics.fct_sessions and analytics.fct_orders.
