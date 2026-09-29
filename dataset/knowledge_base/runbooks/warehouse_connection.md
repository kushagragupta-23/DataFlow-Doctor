# Runbook: Warehouse Connection Exhaustion

Symptoms include timeout acquiring connection, pool exhausted, or too many sessions. Identify tasks holding connections, inspect recent deploys for missing close/finally blocks, and compare active sessions with pool max 20. Restarting workers may temporarily release leaked sessions but is not the permanent fix. Correct the leak and rerun failed idempotent tasks.
