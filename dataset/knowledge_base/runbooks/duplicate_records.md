# Runbook: Duplicate Records

Check whether the extraction watermark overlapped a previous window, whether retries reinserted rows, and whether the destination merge key is correct. Compute duplicates by business key before deleting anything. Preferred remediation is an idempotent MERGE keyed by the source primary key.
