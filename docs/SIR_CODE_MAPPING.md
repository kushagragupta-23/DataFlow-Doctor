# Sir Code Mapping

| Instructor lab | DataFlow Doctor implementation |
|---|---|
| Lab 1 - LLM Generation Parameters | `temperature=0.1` for consistent evidence-grounded answers |
| Lab 2 - Introduction to LangChain | chat model, `ChatPromptTemplate`, runnable `prompt | structured_llm` |
| Lab 3 - Structured Output | `DataFlowDoctorResponse` Pydantic schema + `with_structured_output` |
| Lab 4 - RAG | `TextLoader`, `RecursiveCharacterTextSplitter(1000,200)`, `OllamaEmbeddings`, Chroma, BM25, `EnsembleRetriever` |
| Lab 5 - Advanced RAG | MMR and `MultiQueryRetriever` experiment |
| Lab 6 - RAG With LangGraph | `State` + `START -> retrieve -> generate -> END` |

Project-specific additions are deliberately small: pipeline/category metadata, the synthetic data-engineering corpus, labelled retrieval evaluation, lineage traversal, and UI/API wrappers.
