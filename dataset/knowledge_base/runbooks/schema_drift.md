# Runbook: Schema Drift

Symptoms: validation reports missing/unexpected columns or type mismatch. Compare source schema to manifest, confirm whether producer deployed a new version, and inspect backward compatibility. For additive nullable columns, update the expected schema after owner approval. For breaking type changes, quarantine affected records and coordinate with producer. Do not bypass schema validation simply to make the DAG green.

After correction, rerun from the validation task if upstream extract is immutable and available.
