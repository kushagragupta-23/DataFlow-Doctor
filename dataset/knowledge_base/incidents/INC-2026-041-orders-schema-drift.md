# INC-2026-041 Orders Schema Drift

Date: 2026-04-11
Pipeline: orders_daily_pipeline
Impact: `validate_orders_schema` failed and prevented `fct_orders` and `mart_daily_revenue` publication.

Root cause: ecommerce producer deployed schema v3 adding nullable `discount_code`, while the pipeline still validated against v2. No rows were lost because loading stopped before raw ingestion.

Resolution: approve v3 contract, update manifest, rerun from validation using the same extract.
