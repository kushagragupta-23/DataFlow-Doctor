from pathlib import Path
import pandas as pd
from rag_pipeline import DataFlowDoctorRAG

ROOT = Path(__file__).resolve().parent
cases = pd.read_csv(ROOT / "evaluation" / "evaluation_questions.csv").fillna("")
rag = DataFlowDoctorRAG()


def reciprocal_rank(sources, expected):
    if not expected:
        return 0.0
    for i, source in enumerate(sources, 1):
        if expected == source:
            return 1.0 / i
    return 0.0


rows = []
for method in ["similarity", "mmr", "hybrid"]:
    for _, row in cases[cases.expected_source != ""].iterrows():
        if method == "similarity":
            retriever = rag.similarity_retriever(row.pipeline)
        elif method == "mmr":
            retriever = rag.mmr_retriever(row.pipeline)
        else:
            retriever = rag.hybrid_retriever(row.pipeline)
        docs = retriever.invoke(row.question)
        sources = [d.metadata.get("source", "") for d in docs]
        categories = [d.metadata.get("category", "") for d in docs]
        rows.append({
            "question_id": row.question_id,
            "method": method,
            "source_hit": int(row.expected_source in sources),
            "category_hit": int(row.expected_category in categories),
            "reciprocal_rank": reciprocal_rank(sources, row.expected_source),
            "sources": " | ".join(sources),
        })

out = pd.DataFrame(rows)
summary = out.groupby("method")[["source_hit", "category_hit", "reciprocal_rank"]].mean().round(3)

out.to_csv(ROOT / "evaluation" / "retrieval_results.csv", index=False)
summary.to_csv(ROOT / "evaluation" / "retrieval_summary.csv")

print()
print("SUMMARY")
print(summary)
print()
print("Saved evaluation/retrieval_results.csv and retrieval_summary.csv")
