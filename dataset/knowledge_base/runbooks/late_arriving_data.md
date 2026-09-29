# Runbook: Late Arriving Data

For clickstream, events up to two hours late are included by the watermark. Events later than two hours are quarantined and reconciled by the daily job. Do not expand the hourly watermark without checking cost and duplicate-handling implications.
