# LexID — Agentic Legal Research Assistant for Indonesian Regulations

A retrieval-augmented question-answering system over Indonesian tax law, built
as a portfolio capstone to show an **evaluation-first** RAG workflow end to end:
measured baselines → single-variable experiments → a calibrated LLM judge.

> ⚠️ **LexID adalah alat riset, bukan nasihat hukum.** (This is a research tool,
> not legal advice.)

**Zero-budget build** — every component is free-tier or local, total cost **$0**:
free-tier LLM APIs (Gemini / Gemma), local CPU embeddings + reranker, an embedded
vector DB (no server), and a plan for free deployment.

**Status:** Phase 1 complete — RAG foundation + evaluation pipeline. Phases 2–4
(fine-tuned NER · agent + guardrails · deploy + monitoring) are on the roadmap.

---

## Results (reproducible)

Every number below is measured on a **human-reviewed eval set** and logged in
[`evals/RESULTS.md`](evals/RESULTS.md) with its commit + config + eval-set version.
Corpus: UU 7/2021 (Harmonisasi Peraturan Perpajakan), 218 chunks. Eval set: v1.1,
56 items (50 answerable + 6 unanswerable), 100% human-reviewed.

### Retrieval — 4 single-variable experiments (eval v1.1, 50 items)

| config | recall@5 | recall@10 | MRR | p50 latency |
|---|---|---|---|---|
| dense (BGE-M3, baseline) | 0.69 | 0.82 | 0.57 | 87 ms |
| **+ hybrid** (BM25 + dense, RRF) ← *live default* | **0.77** | 0.88 | 0.62 | 90 ms |
| + rerank (cross-encoder) | 0.84 | 0.92 | 0.74 | ~13 s |
| + hybrid & rerank | **0.86** | **0.96** | 0.75 | ~13 s |

Hybrid is the shipped default: **+0.08 recall@5 over dense at essentially zero
latency cost.** Reranking gets the best quality (0.86) but costs ~13 s/query on
CPU — a trade-off documented rather than hidden.

### Generation — grounded-or-refuse (gen-001, eval v1.1)

| metric | value | how measured |
|---|---|---|
| faithfulness | 0.99 | LLM judge (Gemma), **calibrated** |
| answer correctness | 0.95 | LLM judge (Gemma), **calibrated** |
| citation presence | 1.00 | scripted |
| refusal accuracy (unanswerable) | 1.00 | scripted |
| false-refusal rate (answerable) | 0.12 | scripted |

The system shows **near-zero hallucination** (faithfulness 0.99) and **never
answered an unanswerable question** (0 missed refusals). The cost of that
discipline is a 12% false-refusal rate:
when retrieval misses the relevant chunk, the model refuses instead of guessing —
a downstream symptom of retrieval, not a generation flaw.

**Judge calibration:** the faithfulness/correctness numbers are trustworthy
because the judge was blind-validated against human re-scoring — **0.94
judge–human agreement** (≥0.8 gate), so these are reported metrics, not vibes.

---

## How it works

```
PDF → parse → chunk → embed (BGE-M3) → Qdrant
                                          │
query ─────────────────────────────────► retrieve (hybrid: BM25 + dense, RRF)
                                          │
                                          ▼
                          generate (Gemini, temperature 0)
                          → grounded answer + article citations + disclaimer
```

Full module-dependency graph (auto-generated from imports on every commit):
[`ARCHITECTURE.md`](ARCHITECTURE.md).

**Stack (all free / local):** BGE-M3 embeddings + BGE-reranker-v2-m3 (local CPU) ·
`rank-bm25` for sparse retrieval · Qdrant embedded (no Docker) · Gemini 3.1 Flash
Lite as generator · Gemma 4 26B as judge (different model family). No LangChain /
LlamaIndex — the core is plain Python, explainable line by line.

---

## Quickstart

```bash
uv sync --extra embed         # embedding deps incl. torch (~2GB, once)
cp .env.example .env          # set GEMINI_API_KEY for generation; empty = retrieve-only
uv run python -m scripts.healthcheck
uv run pytest                 # offline: no network, no paid APIs, no model downloads
git config core.hooksPath .githooks   # once: auto-regenerate ARCHITECTURE.md on commit
```

**Prepare the corpus (once).** Corpus PDFs are gitignored; download the two files
listed in [`data/raw/MANIFEST.json`](data/raw/MANIFEST.json) (`download_url`) into
`data/raw/` using their `file` names, then:

```bash
uv run python -m ingestion.run   # parse → chunk → embed (CPU ~12 min) → Qdrant
```

**Ask:**

```bash
uv run python -m rag "Berapa tarif PPh badan dalam negeri?"
uv run python -m rag --retrieve-only "tarif PPh badan"     # chunks only, no LLM
uv run python -m rag --retriever hybrid_rerank "..."       # best quality (~13 s)
```
Without an API key the first command degrades to retrieve-only automatically.

---

## Evaluation methodology (the interesting part)

- **Evals before features** — no experiment merges without a number in
  [`evals/RESULTS.md`](evals/RESULTS.md); one variable changes at a time.
- **Retrieval eval** ([`evals/run_retrieval.py`](evals/run_retrieval.py)) — fully
  local, $0: fact-group recall@k / MRR / NDCG with per-difficulty breakdown.
  Retrieval is deterministic (std-dev 0.000 across runs) → gates measure real signal.
- **Regression gate** ([`evals/gate_check.py`](evals/gate_check.py)) — fails a
  merge on a recall@5 drop > 0.02; refuses to judge on non-citable or
  version-mismatched comparisons.
- **Generation eval** ([`evals/run_generation.py`](evals/run_generation.py)) —
  scripted refusal/citation checks (no quota) + faithfulness/correctness via an
  LLM judge, cached by `(item_id, answer_hash, prompt_version)` and throttled.
- **Judge calibration** ([`evals/calibrate_judge.py`](evals/calibrate_judge.py)) —
  a blind human re-scoring sheet (judge verdict hidden) gates the judge's
  trustworthiness at ≥0.8 agreement before its numbers count.
- **Sacred test set** — eval items never leak into prompts or training data;
  the eval set is frozen + versioned, and reproducibility = commit + config + version.

CI (GitHub Actions): ruff + pytest on every push/PR (offline, no model downloads).

---

## Roadmap

- [x] **Phase 1** — RAG foundation + evaluation pipeline *(complete)*
- [ ] Phase 2 — fine-tuned NER on court decisions (QLoRA, free GPU), gated by a
  data-anonymization pipeline (UU PDP)
- [ ] Phase 3 — agent loop + guardrails (tool use, prompt-injection testing)
- [ ] Phase 4 — deploy + monitoring (HF Spaces free CPU)

See [`CLAUDE.md`](CLAUDE.md) for working rules and [`docs/`](docs/) for per-phase specs.

---

> ⚠️ LexID surfaces and cites source regulations to assist research. It is **not
> legal advice**; always verify against the primary sources it cites and consult a
> qualified professional.
