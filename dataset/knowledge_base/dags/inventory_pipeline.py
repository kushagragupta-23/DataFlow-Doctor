# DAG: inventory_snapshot
# tasks: sftp_download -> checksum -> parse_csv -> load_raw_inventory -> merge_inventory_snapshot
# source file naming: inventory_YYYYMMDD.csv
# delimiter: comma
