from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import DataFlowDoctorRAG
from lineage import downstream_assets, upstream_assets

app = FastAPI(title="DataFlow Doctor API", version="1.0.0")
rag = DataFlowDoctorRAG()

class AskRequest(BaseModel):
    pipeline: str = "all"
    question: str
    method: str = "hybrid"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    answer, docs = rag.ask(req.pipeline, req.question, req.method)
    return {"answer": answer.model_dump(), "sources": [d.metadata for d in docs]}

@app.get("/lineage/downstream")
def downstream(asset: str):
    return {"asset": asset, "downstream": downstream_assets(asset)}

@app.get("/lineage/upstream")
def upstream(asset: str):
    return {"asset": asset, "upstream": upstream_assets(asset)}
