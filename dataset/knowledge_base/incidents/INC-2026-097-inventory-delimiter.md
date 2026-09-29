# INC-2026-097 Inventory Parse Failure

Pipeline: inventory_snapshot
Impact: parse_csv failed with one-column records.
Root cause: vendor delivered semicolon-delimited file although contract requires comma.
Resolution: quarantined file, vendor resent comma-delimited version, checksum verified, pipeline rerun.
