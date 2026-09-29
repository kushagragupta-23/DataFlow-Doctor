import argparse
from rag_pipeline import DataFlowDoctorRAG

p = argparse.ArgumentParser(description="Ask DataFlow Doctor a pipeline debugging question")
p.add_argument("question")
p.add_argument("--pipeline", default="all", choices=["all", "orders", "customers", "clickstream", "inventory", "platform"])
p.add_argument("--method", default="hybrid", choices=["similarity", "mmr", "hybrid"])
a = p.parse_args()
rag = DataFlowDoctorRAG()
answer, docs = rag.ask(a.pipeline, a.question, a.method)
print(answer.model_dump_json(indent=2))
print("\nRetrieved sources:")
for d in docs:
    print("-", d.metadata.get("source"))
