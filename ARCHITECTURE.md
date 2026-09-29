# DataFlow Doctor Architecture

## 1. Offline/indexing path

`source_manifest.csv -> TextLoader -> metadata -> RecursiveCharacterTextSplitter(1000/200) -> OllamaEmbeddings -> Chroma`

Metadata attached to every document:
- `source`
- `title`
- `category`
- `pipeline`
- `incident_id`

## 2. Online RAG path

`question + pipeline scope -> BM25 + Chroma hybrid retrieval -> evidence context -> ChatPromptTemplate -> structured LLM -> DataFlowDoctorResponse`

## 3. Advanced RAG

- MMR improves diversity.
- MultiQuery creates alternative phrasings.
- Hybrid retrieval combines exact data-engineering terms with semantic matching.

## 4. LangGraph

`START -> retrieve -> generate -> END`

This deliberately mirrors Sir's Lab 6 instead of introducing unnecessary agent complexity.

## 5. Lineage impact path

`lineage.csv -> graph traversal -> upstream/downstream affected assets`

This structured helper complements RAG. It is not used to replace retrieval or generation.
