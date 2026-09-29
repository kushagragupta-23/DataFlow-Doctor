from __future__ import annotations
from pathlib import Path
import pandas as pd
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


def load_dataflow_dataset(dataset_dir: str | Path) -> list[Document]:
    """Load the bundled RAG corpus and attach metadata from source_manifest.csv."""
    dataset_dir = Path(dataset_dir)
    manifest = pd.read_csv(dataset_dir / "source_manifest.csv").fillna("")
    docs: list[Document] = []
    for _, row in manifest.iterrows():
        path = dataset_dir / "knowledge_base" / row["source_path"]
        loaded = TextLoader(str(path), encoding="utf-8").load()
        for doc in loaded:
            doc.metadata.update({
                "source": row["source_path"],
                "title": row["title"],
                "category": row["category"],
                "pipeline": row["pipeline"],
                "incident_id": row["incident_id"],
            })
        docs.extend(loaded)
    return docs
