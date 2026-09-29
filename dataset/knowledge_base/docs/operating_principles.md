# Operating Principles

Prefer evidence before reruns. First identify the failed task, earliest error, input freshness, schema drift, and downstream blast radius. Do not backfill large date ranges until the root cause is understood. Use idempotent tasks when rerunning. Never delete production data as a first diagnostic step.
