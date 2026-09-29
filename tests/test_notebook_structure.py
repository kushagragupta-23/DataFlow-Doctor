from pathlib import Path
import json
import ast

ROOT = Path(__file__).resolve().parents[1]

def test_notebook_code_parses_and_has_lab_markers():
    nb = json.loads((ROOT / "DataFlow_Doctor_Sir_Style_RAG.ipynb").read_text(encoding="utf-8"))
    code = "\n".join("".join(c.get("source", [])) for c in nb["cells"] if c["cell_type"] == "code")
    ast.parse(code)
    for token in [
        "RecursiveCharacterTextSplitter",
        "Chroma",
        "BM25Retriever",
        "EnsembleRetriever",
        "with_structured_output",
        "MultiQueryRetriever",
        "StateGraph",
    ]:
        assert token in code
