# DataFlow Doctor RAG Dataset

This bundled corpus is a synthetic but realistic data-engineering operations dataset designed for the DataFlow Doctor RAG project. It can be used immediately without downloading external data.

## Contents

- **41 source files** across Airflow DAGs, logs, schemas, SQL transformations, runbooks, incident postmortems, data-quality rules, configs and platform docs.
- `source_manifest.csv` provides metadata used during RAG ingestion.
- `lineage.csv` provides a small structured dependency graph for blast-radius tracing.
- `evaluation/evaluation_questions.csv` contains **26 labelled retrieval questions**.

## Main incident scenarios

1. Orders schema drift after v3 adds `discount_code`.
2. Duplicate orders caused by an overlapping incremental watermark and non-idempotent INSERT.
3. Malformed CRM CSV rows causing null customer keys.
4. Spark OOM due to a highly skewed bot user.
5. Inventory parse failure caused by a wrong delimiter.
6. Warehouse connection-pool exhaustion caused by leaked connections.

The data is intentionally fictional and safe for an academic/portfolio demo.
