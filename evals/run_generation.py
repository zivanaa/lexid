"""Generation eval: faithfulness + correctness (judge LLM) + scripted refusal/citation.

Costs free-tier requests → throttled, and judge results cached by
(item_id, answer_hash, judge_prompt_version) so re-runs don't re-spend quota.
Full suite only for merge candidates (docs/evals.md), never per-iteration.
Generator ≠ judge family: Gemini generates, Gemma judges (same API key).

    uv run python -m evals.run_generation                # reviewed items, real pipeline
    uv run python -m evals.run_generation --limit 5      # cheap smoke on a few items
    uv run python -m evals.run_generation --throttle 0   # no sleep (cache-only / testing)
"""

import argparse
import hashlib
import json
import re
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from prompts.loader import load
from rag import llm_client
from rag.generate import format_context

# reuse the retrieval harness's item loader — same dataset, same review gate
from evals.run_retrieval import DATASET_DEFAULT, RESULTS_DIR, load_items

JUDGE_PROMPTS_DIR = Path("evals/judge_prompts")
CACHE_PATH = Path("evals/.judge_cache.json")
JUDGE_THROTTLE_S = 4.0  # 15 RPM Gemma → ~1 call / 4 s

# The prompt tells the model to refuse with these when context lacks the answer.
REFUSAL_MARKERS = ("tidak menemukan", "tidak ditemukan", "tidak memuat", "tidak terdapat")


class GenerationEvalError(Exception):
    """Raised when the generation eval cannot run."""


# --- scripted checks (no LLM, no quota) ---


def is_refusal(answer: str) -> bool:
    a = answer.lower()
    return any(m in a for m in REFUSAL_MARKERS)


def has_citation(answer: str) -> bool:
    # citations are bracketed [nama_uu, pasal, ayat]; the disclaimer has no brackets
    return bool(re.search(r"\[[^\]]+\]", answer))


def answer_hash(answer: str) -> str:
    return hashlib.sha256(answer.encode("utf-8")).hexdigest()[:16]


# --- judge (LLM, cached, throttled) ---


def _parse_judge_json(text: str) -> dict:
    """Extract the JSON object from the judge reply (tolerate ```json fences)."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise GenerationEvalError(f"judge returned no JSON: {text[:200]!r}")
    return json.loads(m.group(0))


class JudgeCache:
    """Persist judge verdicts by (item_id, answer_hash, judge_prompt_version)."""

    def __init__(self, path: Path = CACHE_PATH):
        self.path = path
        self.data: dict = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

    @staticmethod
    def key(item_id: str, answer: str, version: int) -> str:
        return f"{item_id}|{answer_hash(answer)}|v{version}"

    def get(self, item_id: str, answer: str, version: int) -> dict | None:
        return self.data.get(self.key(item_id, answer, version))

    def put(self, item_id: str, answer: str, version: int, verdict: dict) -> None:
        self.data[self.key(item_id, answer, version)] = verdict
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")


def judge_generation(
    question: str, context: str, answer: str, reference: str, provider: str = "gemini"
) -> tuple[dict, int]:
    """Judge faithfulness + correctness. Returns (verdict_dict, prompt_version)."""
    prompt_text, version = load("generation_judge", directory=JUDGE_PROMPTS_DIR)
    prompt = prompt_text.format(
        question=question, context=context, answer=answer, reference=reference
    )
    model = llm_client.judge_model(provider)
    if not model:
        raise GenerationEvalError(f"provider '{provider}' has no judge model")
    client = llm_client.client(provider).with_options(timeout=60.0, max_retries=1)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
    except Exception as e:
        raise GenerationEvalError(f"judge {provider}/{model} failed: {e}") from e
    return _parse_judge_json(resp.choices[0].message.content or ""), version


# --- aggregation ---


def aggregate(rows: list[dict]) -> dict:
    answerable = [r for r in rows if not r["expected_refusal"]]
    unanswerable = [r for r in rows if r["expected_refusal"]]
    judged = [r for r in rows if r.get("faithfulness") is not None]

    def _mean(xs: list[float]) -> float | None:
        return round(statistics.mean(xs), 4) if xs else None

    return {
        "n": len(rows),
        "faithfulness_mean": _mean([r["faithfulness"] for r in judged]),
        "correctness_mean": _mean([r["correctness"] for r in judged]),
        "citation_rate": _mean(
            [1.0 if r["has_citation"] else 0.0 for r in rows if not r["refused"]]
        ),
        "refusal_accuracy_unanswerable": _mean(
            [1.0 if r["refused"] else 0.0 for r in unanswerable]
        ),
        "false_refusal_rate_answerable": _mean([1.0 if r["refused"] else 0.0 for r in answerable]),
        "n_judged": len(judged),
    }


# --- runner ---


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LexID generation eval (judge LLM; costs quota)")
    ap.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    ap.add_argument("--limit", type=int, default=None, help="only the first N items (cheap smoke)")
    ap.add_argument("--retriever", default="hybrid", help="retriever the pipeline uses")
    ap.add_argument("--provider", default="gemini")
    ap.add_argument("--throttle", type=float, default=JUDGE_THROTTLE_S)
    ap.add_argument("--include-unreviewed", action="store_true")
    args = ap.parse_args(argv)

    # generation eval must include unanswerable items (they test the refusal path),
    # so load them back in alongside the scoreable ones
    data = json.loads(args.dataset.read_text(encoding="utf-8"))
    _, scoreable, _ = load_items(args.dataset, args.include_unreviewed)
    reviewed_ids = {i.id for i in scoreable}
    from evals.run_retrieval import EvalItem

    items = [
        EvalItem(**it)
        for it in data["items"]
        if (it["reviewed_by_human"] or args.include_unreviewed)
        and (it["id"] in reviewed_ids or it["difficulty"] == "unanswerable")
    ]
    if args.limit:
        items = items[: args.limit]
    if not items:
        print("No items to eval (review the dataset first).")
        return 1

    from rag.pipeline import ask

    cache = JudgeCache(CACHE_PATH)
    rows: list[dict] = []
    judge_calls = 0
    for item in items:
        resp = ask(item.question, retriever=args.retriever, provider=args.provider)
        answer = resp.answer
        refused = is_refusal(answer)
        expected_refusal = item.difficulty == "unanswerable"
        row = {
            "item_id": item.id,
            "difficulty": item.difficulty,
            "refused": refused,
            "expected_refusal": expected_refusal,
            "refusal_correct": refused == expected_refusal,
            "has_citation": has_citation(answer),
            "faithfulness": None,
            "correctness": None,
        }
        # judge only substantive answers to answerable items
        if not refused and not expected_refusal:
            context = format_context(resp.chunks)
            _, version = load("generation_judge", directory=JUDGE_PROMPTS_DIR)
            verdict = cache.get(item.id, answer, version)
            if verdict is None:
                if args.throttle:
                    time.sleep(args.throttle)
                verdict, version = judge_generation(
                    item.question, context, answer, item.reference_answer, provider=args.provider
                )
                cache.put(item.id, answer, version, verdict)
                judge_calls += 1
            row["faithfulness"] = float(verdict["faithfulness"]["score"])
            row["correctness"] = float(verdict["correctness"]["score"])
        rows.append(row)

    agg = aggregate(rows)
    result = {
        "citable": not args.include_unreviewed,
        "dataset": {"name": data["name"], "version": data["version"]},
        "config": {
            "retriever": args.retriever,
            "generator": llm_client.default_model(args.provider),
            "judge": llm_client.judge_model(args.provider),
            "judge_calls_spent": judge_calls,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "overall": agg,
        "per_item": rows,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"generation_{stamp}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== generation eval — {data['name']} v{data['version']} [{args.retriever}] ===")
    if not result["citable"]:
        print("!!! includes UNREVIEWED items — NOT citable in RESULTS.md !!!")
    print(f"items {agg['n']} | judged {agg['n_judged']} | judge calls spent {judge_calls}")
    print(
        f"faithfulness {agg['faithfulness_mean']} | correctness {agg['correctness_mean']}"
        f" | citation_rate {agg['citation_rate']}"
    )
    print(
        f"refusal_accuracy (unanswerable) {agg['refusal_accuracy_unanswerable']}"
        f" | false_refusal_rate (answerable) {agg['false_refusal_rate_answerable']}"
    )
    print(f"saved -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
