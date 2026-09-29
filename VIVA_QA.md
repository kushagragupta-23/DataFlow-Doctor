# Viva Questions and Answers

**Why RAG for data engineering?**  
The answer should depend on the current schemas, logs, runbooks, DAGs and incident history. An LLM's general knowledge does not know this private or project-specific evidence.

**Why hybrid retrieval?**  
BM25 is strong for exact terms such as `discount_code`, `OOMKilled`, table names and incident IDs. Dense retrieval is strong when users paraphrase the problem.

**Why Chroma?**  
It keeps the project close to the class RAG implementation and is simple to run locally for a portfolio demo.

**Why 1000/200 chunking?**  
It intentionally follows Sir's RAG notebook baseline, giving enough local context while preserving overlap at boundaries.

**Why Ollama?**  
Kushagra can run the chat model and embeddings locally on his GPU. It also gives a strong privacy/local-inference discussion point.

**Why structured output?**  
A debugging assistant should return predictable fields such as root causes, evidence, affected assets and next steps instead of an uncontrolled paragraph.

**What does MultiQuery do?**  
It asks the model to create alternative formulations of the user's question so retrieval can find evidence even when document terminology differs from user wording.

**Why LangGraph if there are only two nodes?**  
The simple graph mirrors Sir's Lab 6 and makes the state/data flow explicit without overengineering. More nodes can later be added for approval, lineage checks or SQL validation.

**Why is lineage separate from RAG?**  
Lineage is explicit structured graph data. Deterministic traversal is more reliable than asking an LLM to infer every downstream dependency from prose.

**How is hallucination reduced?**  
Context-only prompt, structured output, source display, information-gap flag and retrieval evaluation.

**Can DataFlow Doctor rerun or backfill pipelines automatically?**  
No. The portfolio version is decision support. Production actions remain human-approved.

**How do you evaluate the project?**  
The labelled question bank measures whether the expected source and category are retrieved and how highly the expected source ranks. Generation can then be evaluated separately.
