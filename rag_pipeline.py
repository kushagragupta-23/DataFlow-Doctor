from __future__ import annotations
import os
from pathlib import Path
from uuid import uuid4
from typing import List
from typing_extensions import TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph, END
from dataflow_loader import load_dataflow_dataset

load_dotenv(override=True)
ROOT = Path(__file__).resolve().parent
DATASET_DIR = ROOT / "dataset"
PERSIST_DIR = ROOT / "chroma_dataflow_doctor_db"


def build_llm():
    provider = os.getenv("MODEL_PROVIDER", "ollama").lower()
    if provider == "groq":
        return init_chat_model(
            os.getenv("GROQ_CHAT_MODEL", "openai/gpt-oss-20b"),
            model_provider="groq",
            temperature=0.1,
        )
    return ChatOllama(model=os.getenv("OLLAMA_CHAT_MODEL", "qwen3:8b"), temperature=0.1)


llm = build_llm()
embeddings_model = OllamaEmbeddings(model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"))


class DataFlowDoctorResponse(BaseModel):
    issue_summary: str = Field(description="Short evidence-grounded summary of the pipeline problem")
    likely_root_causes: list[str] = Field(description="Likely root causes supported by retrieved evidence")
    affected_assets: list[str] = Field(description="Tables, jobs, pipelines or datasets implicated by the evidence")
    evidence: list[str] = Field(description="Concrete observations from logs, schemas, incidents or documentation")
    recommended_steps: list[str] = Field(description="Ordered safe diagnostic or remediation steps supported by context")
    source_documents: list[str] = Field(description="Titles or paths of retrieved sources used")
    data_quality_risk: str = Field(description="Short description of possible data-quality or downstream business impact")
    information_gap: bool = Field(description="True if context is insufficient for a reliable answer")


SYSTEM = """You are DataFlow Doctor, a data-pipeline and ETL debugging assistant.
Use ONLY the retrieved context. Do not invent schemas, row counts, configs, SQL behavior, incidents or fixes.
Separate observed evidence from hypotheses. Prefer reversible checks before reruns or backfills.
Never recommend deleting production data, bypassing validation, or modifying source data unless the retrieved runbook explicitly supports it.
If the context is insufficient, set information_gap=true and explain what evidence is missing.
Selected pipeline scope: {pipeline}

Retrieved context:
{context}
"""

prompt = ChatPromptTemplate([
    ("system", SYSTEM),
    ("human", "Pipeline question: {question}"),
])
structured_llm = llm.with_structured_output(DataFlowDoctorResponse)


def format_docs(docs: List[Document]) -> str:
    parts = []
    for d in docs:
        parts.append(
            f"SOURCE: {d.metadata.get('source')}\nTITLE: {d.metadata.get('title')}\n"
            f"CATEGORY: {d.metadata.get('category')}\nPIPELINE: {d.metadata.get('pipeline')}\n"
            f"INCIDENT: {d.metadata.get('incident_id')}\nCONTENT:\n{d.page_content}"
        )
    return "\n\n".join(parts)


class DataFlowDoctorRAG:
    def __init__(self):
        self.docs = load_dataflow_dataset(DATASET_DIR)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.splits = splitter.split_documents(self.docs)
        self.store = Chroma(
            collection_name="dataflow-doctor-rag",
            embedding_function=embeddings_model,
            persist_directory=str(PERSIST_DIR),
        )

    def index(self, reset=False):
        """Rebuild the local collection from the bundled corpus.

        The corpus is the source of truth. Rebuilding on every index call keeps
        repeated ingestion idempotent and prevents UUID-based duplicate chunks.
        """
        try:
            self.store.delete_collection()
        except Exception:
            pass
        self.store = Chroma(
            collection_name="dataflow-doctor-rag",
            embedding_function=embeddings_model,
            persist_directory=str(PERSIST_DIR),
        )
        ids = [str(uuid4()) for _ in range(len(self.splits))]
        self.store.add_documents(self.splits, ids=ids)
        return len(self.splits)

    def _selected(self, pipeline: str):
        if not pipeline or pipeline.lower() in {"all", "platform"}:
            return self.splits
        selected = [
            d for d in self.splits
            if d.metadata.get("pipeline") in {pipeline, "platform"}
        ]
        return selected or self.splits

    def similarity_retriever(self, pipeline="all", k=4):
        kwargs = {"k": k}
        if pipeline and pipeline.lower() not in {"all", "platform"}:
            # Search selected pipeline only in vector store; platform questions use all docs.
            kwargs["filter"] = {"pipeline": pipeline}
        return self.store.as_retriever(search_type="similarity", search_kwargs=kwargs)

    def mmr_retriever(self, pipeline="all", k=4):
        kwargs = {"k": k}
        if pipeline and pipeline.lower() not in {"all", "platform"}:
            kwargs["filter"] = {"pipeline": pipeline}
        return self.store.as_retriever(search_type="mmr", search_kwargs=kwargs)

    def hybrid_retriever(self, pipeline="all", k=4):
        selected = self._selected(pipeline)
        bm25 = BM25Retriever.from_documents(selected)
        bm25.k = k
        dense = self.similarity_retriever(pipeline, k)
        return EnsembleRetriever(
            retrievers=[bm25, dense],
            weights=[0.7, 0.3],
        )

    def ask(self, pipeline, question, method="hybrid"):
        if method == "similarity":
            retriever = self.similarity_retriever(pipeline)
        elif method == "mmr":
            retriever = self.mmr_retriever(pipeline)
        else:
            retriever = self.hybrid_retriever(pipeline)
        docs = retriever.invoke(question)
        answer = (prompt | structured_llm).invoke({
            "pipeline": pipeline,
            "question": question,
            "context": format_docs(docs),
        })
        return answer, docs

    def multiquery(self, pipeline, question):
        base = self.similarity_retriever(pipeline, k=2)
        mq = MultiQueryRetriever.from_llm(
            retriever=base,
            llm=llm,
            include_original=True,
        )
        return mq.invoke(question)

    def graph(self):
        outer = self

        class State(TypedDict):
            pipeline: str
            question: str
            context: List[Document]
            answer: DataFlowDoctorResponse

        def retrieve(state: State):
            docs = outer.hybrid_retriever(state["pipeline"]).invoke(state["question"])
            return {"context": docs}

        def generate(state: State):
            response = (prompt | structured_llm).invoke({
                "pipeline": state["pipeline"],
                "question": state["question"],
                "context": format_docs(state["context"]),
            })
            return {"answer": response}

        graph_builder = StateGraph(State)
        graph_builder.add_node("retrieve", retrieve)
        graph_builder.add_node("generate", generate)
        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "generate")
        graph_builder.add_edge("generate", END)
        return graph_builder.compile()
