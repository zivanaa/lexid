"""Retrieval eval harness — fully local, $0, run as often as you like.

    uv run python -m evals.run_retrieval                       # reviewed items only
    uv run python -m evals.run_retrieval --include-unreviewed  # sanity runs on drafts

Metrics are computed over relevant_chunk_groups: each group is one FACT and
lists the interchangeable chunks that contain it (word-window overlap means a
fact can live in two adjacent chunks). Recall counts covered facts, so an
item isn't punished for retrieving chunk 0056 instead of its twin 0057.
Unanswerable items are skipped here (they eval the refusal path, not retrieval).
"""

import argparse
import json
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

DATASET_DEFAULT = Path("evals/datasets/retrieval_v1.json")
RESULTS_DIR = Path("evals/results")
K_VALUES = (3, 5, 10)


class EvalItem(BaseModel):
    id: str
    question: str
    difficulty: Literal["direct", "paraphrase", "multi_hop", "unanswerable"]
    relevant_chunk_groups: list[list[str]]
    reference_answer: str
    reviewed_by_human: bool


# --- pure metric functions (unit-tested; no I/O) ---


def group_recall_at_k(retrieved: list[str], groups: list[list[str]], k: int) -> float:
    """Fraction of fact-groups with at least one of their chunks in the top-k."""
    top = set(retrieved[:k])
    return sum(1 for g in groups if top & set(g)) / len(groups)


def precision_at_k(retrieved: list[str], groups: list[list[str]], k: int) -> float:
    relevant = {c for g in groups for c in g}
    return sum(1 for c in retrieved[:k] if c in relevant) / k


def mrr(retrieved: list[str], groups: list[list[str]]) -> float:
    relevant = {c for g in groups for c in g}
    for rank, c in enumerate(retrieved, start=1):
        if c in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: list[str], groups: list[list[str]], k: int) -> float:
    """Binary-relevance NDCG; ideal ranking = all relevant chunks first."""
    import math

    relevant = {c for g in groups for c in g}
    dcg = sum(1.0 / math.log2(i + 2) for i, c in enumerate(retrieved[:k]) if c in relevant)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    return dcg / idcg if idcg else 0.0


def evaluate_item(retrieved: list[str], item: EvalItem) -> dict:
    out = {"item_id": item.id, "difficulty": item.difficulty}
    for k in K_VALUES:
        out[f"recall@{k}"] = group_recall_at_k(retrieved, item.relevant_chunk_groups, k)
        out[f"precision@{k}"] = precision_at_k(retrieved, item.relevant_chunk_groups, k)
    out["mrr"] = mrr(retrieved, item.relevant_chunk_groups)
    out["ndcg@10"] = ndcg_at_k(retrieved, item.relevant_chunk_groups, 10)
    return out


def aggregate(rows: list[dict]) -> dict:
    metrics = [k for k in rows[0] if k not in ("item_id", "difficulty")]
    agg = {m: round(statistics.mean(r[m] for r in rows), 4) for m in metrics}
    per_diff = {}
    for d in sorted({r["difficulty"] for r in rows}):
        sub = [r for r in rows if r["difficulty"] == d]
        per_diff[d] = {
            "n": len(sub),
            **{m: round(statistics.mean(r[m] for r in sub), 4) for m in metrics},
        }
    return {"overall": {"n": len(rows), **agg}, "per_difficulty": per_diff}


# --- runner ---


def load_items(path: Path, include_unreviewed: bool) -> tuple[dict, list[EvalItem], dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = [EvalItem(**it) for it in data["items"]]
    skipped = {
        "unanswerable": sum(1 for i in items if i.difficulty == "unanswerable"),
        "unreviewed": 0,
    }
    items = [i for i in items if i.difficulty != "unanswerable"]
    if not include_unreviewed:
        skipped["unreviewed"] = sum(1 for i in items if not i.reviewed_by_human)
        items = [i for i in items if i.reviewed_by_human]
    return data, items, skipped


def git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return "unknown"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LexID retrieval eval ($0, local)")
    ap.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    ap.add_argument(
        "--include-unreviewed",
        action="store_true",
        help="sanity-check drafts; results are marked NOT-CITABLE and must not enter RESULTS.md",
    )
    args = ap.parse_args(argv)

    from rag.retrieve import retrieve  # deferred: pulls torch

    data, items, skipped = load_items(args.dataset, args.include_unreviewed)
    if not items:
        print(
            f"No scoreable items ({skipped['unreviewed']} unreviewed were skipped). "
            "Review items first, or use --include-unreviewed for a sanity run."
        )
        return 1

    rows, latencies = [], []
    for item in items:
        t0 = time.perf_counter()
        retrieved = [c.chunk_id for c in retrieve(item.question, k=max(K_VALUES))]
        latencies.append((time.perf_counter() - t0) * 1000)
        rows.append(evaluate_item(retrieved, item))

    result = {
        "citable": not args.include_unreviewed,
        "dataset": {"name": data["name"], "version": data["version"], "path": str(args.dataset)},
        "config": {
            "commit": git_commit(),
            "k_values": list(K_VALUES),
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "skipped": skipped,
        "latency_ms": {
            "p50": round(statistics.median(latencies), 1),
            "mean": round(statistics.mean(latencies), 1),
        },
        **aggregate(rows),
        "per_item": rows,
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"retrieval_{stamp}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== retrieval eval — {data['name']} v{data['version']} ===")
    if not result["citable"]:
        print("!!! includes UNREVIEWED items — sanity run only, NOT citable in RESULTS.md !!!")
    print(f"items: {result['overall']['n']} scored | skipped: {skipped}")
    o = result["overall"]
    print(
        f"recall@3 {o['recall@3']} | recall@5 {o['recall@5']} | recall@10 {o['recall@10']}"
        f" | mrr {o['mrr']} | ndcg@10 {o['ndcg@10']}"
    )
    for d, m in result["per_difficulty"].items():
        print(f"  {d:<12} n={m['n']:<3} recall@5 {m['recall@5']}  mrr {m['mrr']}")
    print(f"latency p50 {result['latency_ms']['p50']} ms | saved -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
