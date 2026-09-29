import argparse
import shutil
from pathlib import Path
from rag_pipeline import DataFlowDoctorRAG, PERSIST_DIR

p = argparse.ArgumentParser(description="Index the bundled DataFlow Doctor RAG corpus into Chroma")
p.add_argument("--reset", action="store_true", help="Delete the local Chroma directory before indexing")
args = p.parse_args()
if args.reset and Path(PERSIST_DIR).exists():
    shutil.rmtree(PERSIST_DIR)
rag = DataFlowDoctorRAG()
print(f"Indexed {rag.index(reset=False)} chunks into Chroma at {PERSIST_DIR}")
