# Runbook: Inventory SFTP Failure

Verify remote file exists with expected name, checksum matches, and delimiter is comma. If a vendor sends semicolon-delimited data, do not silently parse it as comma-separated; quarantine the file and request corrected delivery or explicitly version the parser after approval.
