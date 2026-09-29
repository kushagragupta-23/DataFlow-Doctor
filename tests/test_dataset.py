from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_dataset_manifest_and_files_exist():
    df = pd.read_csv(ROOT / "dataset" / "source_manifest.csv")
    assert len(df) == 41
    assert {"source_path", "title", "category", "pipeline", "incident_id"}.issubset(df.columns)
    for rel in df.source_path:
        assert (ROOT / "dataset" / "knowledge_base" / rel).exists(), rel

def test_eval_cases():
    df = pd.read_csv(ROOT / "evaluation" / "evaluation_questions.csv")
    assert len(df) == 26
    assert {"question_id", "pipeline", "question", "expected_source", "expected_category"}.issubset(df.columns)

def test_lineage_dataset():
    df = pd.read_csv(ROOT / "dataset" / "lineage.csv")
    assert len(df) >= 10
    assert {"upstream_asset", "downstream_asset", "job"}.issubset(df.columns)
