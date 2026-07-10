"""Judge calibration — measure judge–human agreement before trusting judge metrics.

    uv run python -m evals.calibrate_judge           # 1. build the BLIND re-scoring sheet
    # 2. read evals/calibration/judge_calibration.md, fill evals/calibration/human_scores.json
    uv run python -m evals.calibrate_judge --score   # 3. agreement vs the judge

docs/evals.md gate: agreement >= 0.8 before faithfulness/correctness are citable.
The sheet HIDES the judge verdict (in judge_scores.json — do NOT open it while
scoring) so the human isn't anchored to it. Pure offline: reads a self-contained
generation results JSON (question/context/answer/reference/judge_verdict).
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

CALIB_DIR = Path("evals/calibration")
RESULTS_DIR = Path("evals/results")
AGREEMENT_TARGET = 0.8
DIMENSIONS = ("faithfulness", "correctness")
LABELS = {
    "faithfulness": ("supported", "partial", "unsupported"),
    "correctness": ("correct", "partial", "incorrect"),
}


class CalibrationError(Exception):
    """Raised when calibration inputs are missing or malformed."""


def latest_generation_result(results_dir: Path = RESULTS_DIR) -> Path | None:
    files = sorted(results_dir.glob("generation_*.json"))
    return files[-1] if files else None


def judged_rows(result: dict) -> list[dict]:
    return [r for r in result["per_item"] if r.get("judge_verdict") is not None]


def judge_labels(rows: list[dict]) -> dict[str, dict[str, str]]:
    """Extract the judge's verdict LABELS (not scores) per item."""
    return {r["item_id"]: {d: r["judge_verdict"][d]["verdict"] for d in DIMENSIONS} for r in rows}


def agreement(human: dict, judge: dict) -> dict:
    """Raw agreement (fraction of matching labels) per dimension + overall,
    over items the human actually scored with valid labels."""
    scored = [
        i for i in human if i in judge and all(human[i].get(d) in LABELS[d] for d in DIMENSIONS)
    ]
    per_dim = {}
    for d in DIMENSIONS:
        matches = [1.0 if human[i][d] == judge[i][d] else 0.0 for i in scored]
        per_dim[d] = round(statistics.mean(matches), 4) if matches else None
    vals = [v for v in per_dim.values() if v is not None]
    return {
        "n_scored": len(scored),
        "per_dimension": per_dim,
        "overall": round(statistics.mean(vals), 4) if vals else None,
        "meets_target": bool(vals) and min(vals) >= AGREEMENT_TARGET,
    }


def build_sheet(rows: list[dict]) -> str:
    lines = [
        "# Lembar Kalibrasi Judge (BUTA)",
        "",
        "Untuk TIAP item: baca konteks + jawaban model, lalu tulis penilaianMU",
        "di `human_scores.json` (JANGAN buka `judge_scores.json` dulu — itu bikin bias).",
        "",
        "Label yang boleh:",
        "- faithfulness: `supported` (semua klaim didukung konteks) / `partial` / `unsupported`",
        "- correctness: `correct` (cocok referensi) / `partial` / `incorrect`",
        "",
        f"Target: agreement >= {AGREEMENT_TARGET} di kedua dimensi → metrik judge jadi citable.",
        "",
    ]
    for r in rows:
        lines += [
            "---",
            f"## {r['item_id']} · {r['difficulty']}",
            f"**Pertanyaan:** {r['question']}",
            "",
            "<details><summary>Konteks yang dilihat model</summary>",
            "",
            "```",
            r.get("context") or "(tidak tersimpan)",
            "```",
            "",
            "</details>",
            "",
            f"**Jawaban model:** {r['answer']}",
            "",
            f"**Jawaban referensi:** {r['reference_answer']}",
            "",
            "Nilaimu → isi di human_scores.json: "
            f'`"{r["item_id"]}": {{"faithfulness": "...", "correctness": "..."}}`',
            "",
        ]
    return "\n".join(lines)


def make(argv_result: Path | None) -> int:
    result_path = argv_result or latest_generation_result(RESULTS_DIR)
    if result_path is None or not result_path.exists():
        raise CalibrationError(
            "no generation results found — run: uv run python -m evals.run_generation"
        )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    rows = judged_rows(result)
    if len(rows) < 30:
        print(f"[warn] only {len(rows)} judged items (<30) — calibration will be weak; grow first")

    CALIB_DIR.mkdir(parents=True, exist_ok=True)
    (CALIB_DIR / "judge_calibration.md").write_text(build_sheet(rows), encoding="utf-8")
    # human template: empty labels to fill
    human_template = {r["item_id"]: {"faithfulness": "", "correctness": ""} for r in rows}
    (CALIB_DIR / "human_scores.json").write_text(
        json.dumps(human_template, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # judge labels: DO NOT open while scoring
    (CALIB_DIR / "judge_scores.json").write_text(
        json.dumps(judge_labels(rows), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"source: {result_path.name} — {len(rows)} judged items")
    print(f"1. read {CALIB_DIR / 'judge_calibration.md'}")
    print(f'2. fill {CALIB_DIR / "human_scores.json"} — ganti tiap "" jadi label')
    print("   (do NOT open judge_scores.json — bikin bias)")
    print("3. HANYA setelah terisi, run: uv run python -m evals.calibrate_judge --score")
    print("   (jalankan --score sekarang = 0 skor; ini BUKAN vonis jelek, cuma belum diisi)")
    return 0


def score() -> int:
    human_path = CALIB_DIR / "human_scores.json"
    judge_path = CALIB_DIR / "judge_scores.json"
    if not human_path.exists() or not judge_path.exists():
        raise CalibrationError("run the make step first (missing human_scores/judge_scores)")
    human = json.loads(human_path.read_text(encoding="utf-8"))
    judge = json.loads(judge_path.read_text(encoding="utf-8"))
    res = agreement(human, judge)

    if res["n_scored"] == 0:
        print(
            "0 items scored — human_scores.json is still empty.\n"
            f"Isi dulu penilaianmu di {human_path} (baca {CALIB_DIR / 'judge_calibration.md'}),\n"
            'ganti tiap "" jadi label (mis. "supported"/"correct"), lalu jalankan --score lagi.'
        )
        return 2

    print(f"scored {res['n_scored']} items")
    for d, a in res["per_dimension"].items():
        print(f"  {d:<13} agreement {a}")
    print(f"  overall       {res['overall']}")
    if res["n_scored"] < 30:
        print(f"[warn] only {res['n_scored']} items scored (<30) — result is weak")
    if res["meets_target"]:
        print(
            f"VERDICT: judge TRUSTWORTHY (>= {AGREEMENT_TARGET}) — faithfulness/correctness now citable"
        )
        return 0
    print(
        f"VERDICT: judge NOT trustworthy (< {AGREEMENT_TARGET}) — fix the judge prompt (v2), re-run"
    )
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Judge calibration (offline, $0)")
    ap.add_argument(
        "--score", action="store_true", help="compute agreement (after filling human_scores.json)"
    )
    ap.add_argument(
        "--result", type=Path, default=None, help="generation results JSON (default: newest)"
    )
    args = ap.parse_args(argv)
    try:
        return score() if args.score else make(args.result)
    except CalibrationError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
