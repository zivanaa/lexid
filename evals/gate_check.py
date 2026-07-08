"""Regression gate: does a candidate retrieval run regress vs the baseline?

    uv run python -m evals.gate_check --baseline <best.json>              # candidate = newest result
    uv run python -m evals.gate_check --baseline <best.json> --candidate <new.json>

Run manually before EVERY merge to main (docs/evals.md). Exit codes:
  0 = PASS · 1 = gate FAILED (real regression) · 2 = precondition error (can't judge).

Only retrieval metrics are wired up (Phase 1). Faithfulness / false-refusal
gates arrive WITH evals/run_generation.py — do not add them before that exists.

Baseline persistence: retrieval result JSONs live in evals/results/ (gitignored),
so keep the current-best file around (e.g. copy it to evals/results/baseline.json).
A conscious re-baseline needs a written rationale in RESULTS.md.
"""

import argparse
import json
import sys
from pathlib import Path

from pydantic import BaseModel

RESULTS_DIR = Path("evals/results")
RECALL5_MAX_DROP = 0.02  # [INITIAL] — recalibrate vs measured noise (exp-001 std 0.000)
REPORT_METRICS = ("recall@3", "recall@5", "recall@10", "mrr", "ndcg@10")


class GateResult(BaseModel):
    passed: bool
    errors: list[str]  # preconditions that make the comparison invalid → exit 2
    failures: list[str]  # real gate violations → exit 1
    warnings: list[str]  # informational, do not change the verdict
    deltas: dict[str, float]  # candidate − baseline, per metric


def compare(
    baseline: dict, candidate: dict, max_recall5_drop: float = RECALL5_MAX_DROP
) -> GateResult:
    errors: list[str] = []
    failures: list[str] = []
    warnings: list[str] = []

    # --- preconditions: if these fail, the comparison is meaningless ---
    for label, r in (("baseline", baseline), ("candidate", candidate)):
        if not r.get("citable", False):
            errors.append(f"{label} is NOT citable (ran with --include-unreviewed)")
    bv, cv = baseline["dataset"]["version"], candidate["dataset"]["version"]
    if bv != cv:
        errors.append(
            f"eval-set version mismatch: baseline v{bv} vs candidate v{cv} - not comparable"
        )

    b, c = baseline["overall"], candidate["overall"]
    deltas = {m: round(c[m] - b[m], 4) for m in REPORT_METRICS if m in b and m in c}

    if errors:  # don't pretend to judge on an invalid comparison
        return GateResult(
            passed=False, errors=errors, failures=failures, warnings=warnings, deltas=deltas
        )

    # --- the gate itself ---
    drop = round(b["recall@5"] - c["recall@5"], 4)
    if drop > max_recall5_drop:
        failures.append(
            f"recall@5 dropped {drop} (> {max_recall5_drop}): {b['recall@5']} -> {c['recall@5']}"
        )

    # --- honesty warning: can the eval set even resolve the threshold? ---
    n = c.get("n") or 0
    if n and (1.0 / n) > max_recall5_drop:
        warnings.append(
            f"eval set n={n}: one item = {1 / n:.3f} of recall@5, coarser than the gate "
            f"{max_recall5_drop} - a {max_recall5_drop} regression is unmeasurable; grow the eval set"
        )

    return GateResult(
        passed=not failures, errors=errors, failures=failures, warnings=warnings, deltas=deltas
    )


def newest_result(results_dir: Path = RESULTS_DIR) -> Path | None:
    files = sorted(results_dir.glob("retrieval_*.json"))
    return files[-1] if files else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Retrieval regression gate ($0, local)")
    ap.add_argument("--baseline", type=Path, required=True, help="current-best result JSON")
    ap.add_argument(
        "--candidate", type=Path, help="new result JSON (default: newest in evals/results/)"
    )
    ap.add_argument("--max-recall5-drop", type=float, default=RECALL5_MAX_DROP)
    args = ap.parse_args(argv)

    candidate_path = args.candidate or newest_result()
    if candidate_path is None:
        print("[error] no candidate given and no result files in evals/results/", file=sys.stderr)
        return 2
    for p in (args.baseline, candidate_path):
        if not p.exists():
            print(f"[error] not found: {p}", file=sys.stderr)
            return 2

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    res = compare(baseline, candidate, max_recall5_drop=args.max_recall5_drop)

    print(
        f"baseline : {args.baseline}  (v{baseline['dataset']['version']}, commit {baseline['config']['commit']})"
    )
    print(
        f"candidate: {candidate_path}  (v{candidate['dataset']['version']}, commit {candidate['config']['commit']})"
    )
    print("deltas (candidate - baseline):")
    for m, d in res.deltas.items():
        marker = "up" if d > 0 else ("down" if d < 0 else "flat")
        print(f"  {m:<10} {d:+.4f} {marker}")
    for w in res.warnings:
        print(f"[warn] {w}")

    if res.errors:
        for e in res.errors:
            print(f"[error] {e}")
        print("VERDICT: CANNOT JUDGE (fix preconditions)")
        return 2
    if res.failures:
        for f in res.failures:
            print(f"[FAIL] {f}")
        print("VERDICT: GATE FAILED - do not merge")
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
