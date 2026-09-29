# INC-2026-104 Warehouse Connection Pool Exhaustion

Pipeline: multiple dbt publish tasks
Impact: tasks timed out acquiring warehouse connections.
Root cause: a PythonOperator introduced in deployment 2026.09.14 opened a connection per batch without closing it. Active sessions reached pool maximum 20.
Resolution: added context manager/finally close, restarted affected workers to release leaked sessions, reran failed idempotent tasks.
