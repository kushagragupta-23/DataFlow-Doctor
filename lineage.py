from __future__ import annotations
from pathlib import Path
from collections import deque
import pandas as pd

ROOT = Path(__file__).resolve().parent
LINEAGE_FILE = ROOT / "dataset" / "lineage.csv"


def load_lineage() -> pd.DataFrame:
    return pd.read_csv(LINEAGE_FILE)


def downstream_assets(asset: str) -> list[dict]:
    """Breadth-first traversal over the bundled lineage graph."""
    df = load_lineage()
    edges = {}
    for _, row in df.iterrows():
        edges.setdefault(row["upstream_asset"], []).append((row["downstream_asset"], row["job"]))
    seen = {asset}
    q = deque([(asset, 0)])
    out = []
    while q:
        current, depth = q.popleft()
        for downstream, job in edges.get(current, []):
            if downstream in seen:
                continue
            seen.add(downstream)
            out.append({"asset": downstream, "via_job": job, "depth": depth + 1})
            q.append((downstream, depth + 1))
    return out


def upstream_assets(asset: str) -> list[dict]:
    df = load_lineage()
    reverse = {}
    for _, row in df.iterrows():
        reverse.setdefault(row["downstream_asset"], []).append((row["upstream_asset"], row["job"]))
    seen = {asset}
    q = deque([(asset, 0)])
    out = []
    while q:
        current, depth = q.popleft()
        for upstream, job in reverse.get(current, []):
            if upstream in seen:
                continue
            seen.add(upstream)
            out.append({"asset": upstream, "via_job": job, "depth": depth + 1})
            q.append((upstream, depth + 1))
    return out
