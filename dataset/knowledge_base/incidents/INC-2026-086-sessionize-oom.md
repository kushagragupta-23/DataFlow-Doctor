# INC-2026-086 Spark Sessionization OOM

Pipeline: clickstream_hourly
Impact: spark_sessionize executors were OOMKilled during a traffic spike.
Root cause: a single bot user generated 31 million events, causing a skewed partition on user_id. Increasing memory alone was insufficient.
Resolution: filter known bots, salt skewed keys, increase shuffle partitions from 200 to 600 for spike windows, then rerun the affected hour.
