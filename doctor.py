import shutil
import subprocess
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
print("Python:", sys.version.split()[0])
print("Ollama executable:", shutil.which("ollama") or "NOT FOUND")
manifest = pd.read_csv(ROOT / "dataset" / "source_manifest.csv")
print("Dataset files in manifest:", len(manifest))
print("Evaluation questions:", len(pd.read_csv(ROOT / "evaluation" / "evaluation_questions.csv")))
if shutil.which("ollama"):
    try:
        print(subprocess.check_output(["ollama", "list"], text=True, timeout=10))
    except Exception as e:
        print("Could not query Ollama:", e)
