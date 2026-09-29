# DAG: clickstream_hourly
# tasks: ingest_events -> validate_event_contract -> spark_sessionize -> publish_funnel_mart
# watermark: event_time minus 2 hours
# late data beyond 2 hours goes to quarantine and is included in daily reconciliation.
