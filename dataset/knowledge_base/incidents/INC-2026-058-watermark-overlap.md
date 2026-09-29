# INC-2026-058 Duplicate Orders

Pipeline: orders_daily_pipeline
Impact: 18,422 duplicate order rows appeared in raw.orders and inflated downstream revenue.

Root cause: retry logic reset the incremental watermark to midnight instead of the last successful `updated_at`, while raw load used INSERT rather than MERGE.

Resolution: corrected watermark persistence, changed raw load to idempotent MERGE on order_id, rebuilt affected partition and validated totals against source.
