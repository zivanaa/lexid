# Evaluation Framework (Phase 1 spec)

## Eval set (target ≥120 items [INITIAL], 100% human-reviewed before counting)
Difficulty mix: ~50% direct, ~25% paraphrase (colloquial, no keyword overlap),
~15% multi_hop (needs ≥2 chunks), ~10% unanswerable (tests refusal path).
Item schema: question, relevant_chunk_ids, reference_answer, difficulty,
reviewed_by_human. Frozen after review; corrections require a changelog line.
Versioning: bump minor (v1.1→v1.2) on item fixes, major on composition changes;
changelog lives at the top of the dataset JSON. Old RESULTS entries stay tagged
with the version they ran on.

## Retrieval metrics ($0 — fully local, run as often as you like)
Recall@k (primary; k=3,5,10), Precision@k, MRR, NDCG. ALWAYS report the
per-difficulty breakdown — aggregates hide multi_hop failures.

## Noise protocol (do before setting any gate)
Run the baseline retrieval eval 3×. Record mean ± std-dev in RESULTS.md.
Gates are meaningful only relative to this noise. Re-measure noise when the
eval set version changes.

## Generation metrics (costs free-tier requests — budget them)
- Faithfulness (every claim supported by cited chunks) — LLM-as-judge, primary
- Answer correctness vs reference — LLM-as-judge
- Citation accuracy — scripted check (cited article contains supporting text)
- Refusal accuracy on unanswerable items + false-refusal rate on answerable ones

Judge rules: judge provider != generation provider (default: generate Gemini,
judge Groq — different family, both free). Judge prompt versioned in
evals/judge_prompts/. Judge outputs strict JSON {verdict, score, reasoning}.
Calibration: manually re-score ≥30 judge decisions; report agreement in
RESULTS.md; agreement <0.8 [INITIAL] → fix the judge prompt before trusting it.
Cache judge results by (item_id, answer_hash, judge_prompt_version) — a full
120-item judge pass ≈ 120–240 requests; Gemini free ≈ 1.5K/day, Groq ≈ 14.4K/day
[UNVERIFIED] → run full judge suites only for merge candidates.

## gate_check.py (manual from Phase 1; CI later)
Compares a results JSON vs current best: fails on Recall@5 drop >0.02 or
faithfulness drop >0.03 or false-refusal rise >0.02 [INITIAL — recalibrate vs
noise]. Run before EVERY merge to main. A conscious re-baseline requires a
written rationale in RESULTS.md.

## Phase 1 experiment matrix (change ONE variable at a time from current best)
chunking {fixed-512, recursive, pasal/ayat structure-aware} × context-prefix
{on, off} × embedding {bge-m3, one lighter alternative} × retrieval
{dense-only, hybrid BM25+RRF} × rerank {on, off}. Full grid not required —
follow promising branches; every run gets a RESULTS.md entry.

## Judge quota math (measured from owner console, 2026-07-07)
Primary judge = **Gemma 4 26B via Gemini API**: 1,500 RPD, unlimited TPM →
a full 120-item pass uses ~120-240 requests (~10-16% of daily quota). Run it
freely for merge candidates; caching by (item_id, answer_hash,
judge_prompt_version) still applies. 15 RPM → throttle to ~1 call/4s.
Fallback judge = Groq Llama-3.3-70B (JSON mode confirmed): 100K tokens/DAY
binds — lean prompts, one pass/day max. Never mix judges within one
comparison row; log which judge scored what.
Generator quotas: Gemini 3.1 Flash Lite 500 RPD (daily dev); Groq 70B for
final-quality runs (~30-50 RAG answers/day within 100K TPD at 2-4K
tokens/answer). The 20-RPD Flash models are dev-test toys only.
