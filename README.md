# DataFlow Doctor - Data Pipeline & ETL Debugging RAG

A complete local-first RAG portfolio project for **Kushagra Gupta**. The main notebook intentionally follows the instructor's Generative AI **Labs 1-6** structure while the project-specific layer adds a realistic data-engineering corpus, metadata filtering, evaluation and lineage impact analysis.

## Problem

Data teams often spend time searching Airflow DAGs, logs, schemas, SQL transformations, quality rules, incident postmortems and runbooks before they can explain why a pipeline failed. DataFlow Doctor retrieves the most relevant evidence first and then generates a structured, source-backed diagnosis.

## Bundled RAG dataset

The ZIP includes everything needed for the demo. No external dataset download is required.

- **41 RAG source files**
- **26 labelled retrieval questions**
- Airflow-style DAG files
- SQL transformations
- schemas/contracts
- data-quality rules
- logs
- incident reports
- runbooks
- configuration files
- architecture/lineage documentation
- `lineage.csv` for structured blast-radius tracing
- `source_manifest.csv` for metadata-driven ingestion

Main incident scenarios:
1. Orders schema drift after `discount_code` is added.
2. Duplicate orders from overlapping watermarks/non-idempotent loads.
3. Null customer keys from malformed CRM records.
4. Spark executor OOM from partition skew.
5. Inventory parse failure from the wrong delimiter.
6. Warehouse connection-pool exhaustion from leaked connections.

## Sir's class-style RAG flow

`low-temperature LLM -> load -> split 1000/200 -> OllamaEmbeddings -> Chroma -> similarity/MMR/BM25+Chroma -> ChatPromptTemplate -> Pydantic -> LCEL -> MultiQuery -> LangGraph -> evaluation`

### Lab mapping

- **Lab 1:** low-temperature factual generation
- **Lab 2:** LangChain chat model + `ChatPromptTemplate` + runnable chain
- **Lab 3:** Pydantic structured output + `with_structured_output`
- **Lab 4:** loader, 1000/200 chunking, `OllamaEmbeddings`, Chroma, BM25, `EnsembleRetriever`
- **Lab 5:** MMR + `MultiQueryRetriever`
- **Lab 6:** `START -> retrieve -> generate -> END` using LangGraph

## Local models

Default local setup:
- Chat: `qwen3:8b`
- Embeddings: `nomic-embed-text`

Optional Groq generation is supported through `.env`.

## Windows setup

```powershell
ollama pull qwen3:8b
ollama pull nomic-embed-text
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python ingest.py --reset
streamlit run app.py
```

## Example questions

```powershell
python cli.py "The orders schema validation says discount_code is unexpected. What happened?" --pipeline orders
python cli.py "Why were Spark executors OOMKilled during the traffic spike?" --pipeline clickstream
python cli.py "Why did inventory parsing see only one column?" --pipeline inventory
python cli.py "What is the permanent fix for the warehouse connection leak?" --pipeline platform
```

## Streamlit UI

```powershell
streamlit run app.py
```

The UI includes both evidence-grounded RAG diagnosis and a lineage impact panel.

## FastAPI

```powershell
uvicorn api:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Retrieval evaluation

After indexing:

```powershell
python evaluate.py
```

The script compares similarity, MMR and hybrid retrieval using **source hit**, **category hit** and **reciprocal rank**.

## Why this is good for a resume

It connects GenAI/RAG with actual data-engineering concepts: schemas, Airflow-style workflows, SQL transformations, data quality, incident debugging, metadata filtering and lineage. It is much more defensible than a generic PDF chatbot.

## Important design note

DataFlow Doctor is decision support. It retrieves evidence and suggests safe diagnostic steps; it does not automatically modify production data, rerun pipelines or perform destructive backfills.
