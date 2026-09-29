# 6-8 Minute Demo Script

1. Open `dataset/source_manifest.csv`; explain the 41 evidence sources and the pipeline/category metadata.
2. Show `dataset/lineage.csv`; explain that RAG handles unstructured evidence while lineage handles explicit dependencies.
3. Run `python ingest.py --reset` before the presentation.
4. Ask: **The orders schema validation says discount_code is unexpected. What happened?**
   - Show the schema-drift incident and orders schema evidence.
5. Ask: **Why were Spark executors OOMKilled during the traffic spike?**
   - Show incident + Spark log + config evidence.
6. Ask: **Why did inventory parsing see only one column?**
   - Show delimiter incident, contract and runbook.
7. In the UI, trace downstream impact from `raw.orders` and explain blast radius.
8. Open the notebook and briefly show similarity, MMR and BM25+Chroma hybrid retrieval.
9. Show LangGraph `START -> retrieve -> generate -> END`.
10. Ask an unsupported question such as a cricket result and show the controlled information-gap behavior.
11. Finish with `python evaluate.py` and explain source hit/category hit/reciprocal rank.
