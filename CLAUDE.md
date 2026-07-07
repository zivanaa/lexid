# CLAUDE.md — LexID

Agentic legal research assistant for Indonesian regulations. Portfolio capstone:
RAG + evals → fine-tuned NER → agent + guardrails → deploy + monitoring.
Solo developer, ~10 hrs/week. **Not legal advice — disclaimer mandatory in every
user-facing surface.**

Detailed specs live in `docs/` — read the doc for the CURRENT phase only:
`docs/evals.md` · `docs/finetuning.md` · `docs/agent.md` · `docs/deployment.md` ·
`docs/data-privacy.md`

## Budget: Rp 0 (hard constraint)

No paid APIs, no paid GPUs, no paid hosting. Concretely:
- **Generation LLM:** Gemini 3.1 Flash Lite for daily dev iteration (500 RPD);
  Groq Llama-3.3-70B for final-quality runs & the demo (stronger model, but
  ~100K tokens/day binds → use sparingly).
  **Judge LLM:** Gemma 4 26B via the same Gemini API key (1.5K RPD, unlimited
  TPM — highest free volume; different family from both generators ✓).
  **Fallback:** OpenRouter `:free` models. See `rag/llm_client.py`.
- **Embeddings & reranker:** local models on CPU. **Vector DB:** Qdrant embedded
  local mode (`path=`, no Docker, no server). **Fine-tuning:** Kaggle/Colab free GPU.
  **Deploy:** HF Spaces free CPU tier.
- Free tiers have daily caps → design around them: retrieval evals are fully local
  ($0, unlimited); generation/judge evals are throttled + judge results cached by
  `(item_id, answer_hash, judge_prompt_version)`; full judge suite only for merge
  candidates, never per-iteration.
- If something truly needs money, STOP and present the trade-off — never assume
  spending is acceptable.

## Current Phase

- [ ] **Phase 1: RAG foundation + evaluation pipeline** ← CURRENT
- [ ] Phase 2: NER fine-tuning · [ ] Phase 3: Agent + guardrails · [ ] Phase 4: Deploy

Never build ahead of the current phase. Within Phase 1 the order is fixed:
naive end-to-end baseline → eval set + harness → measured baseline → only then
experiments. Never optimize before the baseline is measured.

## What EXISTS vs PLANNED

This file must never describe a repo that doesn't exist. Current truth:

EXISTS (tested): `config.py`, `scripts/healthcheck.py`, `rag/llm_client.py`,
`prompts/loader.py` + `prompts/rag_generation.md`, `tests/test_skeleton.py`,
`evals/RESULTS.md` (template), package folders.

PLANNED (build in this order): `ingestion/parse.py` → `ingestion/chunk.py` →
`ingestion/embed.py` → `ingestion/index.py` → `ingestion/run.py` →
`rag/retrieve.py` → `rag/generate.py` → `rag/pipeline.py` →
`evals/run_retrieval.py` → `evals/gate_check.py` → `evals/run_generation.py`.
When you create a PLANNED file, move it to EXISTS in the same commit.

## VERIFIED 2026-07-07 (web check) + remaining manual steps

Resolved by verification:
- **Groq free tier confirmed:** no credit card; `llama-3.3-70b-versatile` at
  ~30 RPM / 1,000 RPD / 12K TPM / **100K TPD** — TPD binds. Console confirms:
  context window 131,072, max output 32,768, Tool Use + **JSON Object Mode**
  (use JSON mode for judge/extraction outputs).
- **Gemini free tier — MEASURED from the owner's own project console
  (2026-07-07); articles claiming "1,500 RPD Flash" did NOT apply:**
  Gemini 2.5/3/3.5 Flash: 5 RPM / 250K TPM / **only 20 RPD** (trap — dev-test only).
  **Gemini 3.1 Flash Lite: 15 RPM / 250K TPM / 500 RPD** ← daily-dev generator.
  **Gemma 4 26B & 31B: 15 RPM / unlimited TPM / 1,500 RPD** ← primary judge.
  Pro models: 0/0/0 on free tier (paid only).
  **Gemini Embedding 1 & 2: 100 RPM / 30K TPM / 1K RPD** ← free API embedding
  comparison target vs local BGE-M3 (same model must embed corpus AND queries).
  Lesson recorded: per-project console numbers override any published figures.
- **BGE-M3 confirmed** as the standard self-hosted multilingual default in 2026
  ("most production RAG stacks default to BGE-M3 + BGE-reranker-v2"). Bonus: it
  natively supports SPARSE retrieval → hybrid experiment can compare BM25
  (`rank_bm25`) vs BGE-M3 sparse. Lighter CPU option: nomic-embed (137M).
  Higher-accuracy open option if GPU available: Qwen3-Embedding.
- **Direktori Putusan MA alive** at putusan3.mahkamahagung.go.id, actively
  uploading 2026 decisions incl. MA tax cases (PPh Badan) — ideal Phase 2 corpus.
  Listings show real defendant names → anonymization gate (docs/data-privacy.md)
  is confirmed necessary.
- **Legal example corrected & verified:** corporate income tax 22% (effective
  tax year 2022) sits in **Pasal 17 ayat (1) huruf b UU PPh (UU 7/1983) jo.
  UU HPP (UU 7/2021)** — cite the amended UU PPh, not "UU HPP" alone. Related
  eval-set material: 19% listed companies (Pasal 17 ayat (2b)), effective 11%
  small-turnover facility (Pasal 31E).

Remaining manual steps (owner, ~15 min, all free):
1. Create Gemini API key at aistudio.google.com (no card) → note YOUR project's
   limits from the AI Studio rate-limit page into this section.
2. Create Groq key at console.groq.com (no card) → confirm model id list.
3. (Optional) OpenRouter key as fallback.
4. Click-check jdih.kemenkeu.go.id + peraturan.go.id and pick the 2–3 source
   documents for Phase 1; record URLs in data/raw/MANIFEST.json.

## Core Principles (non-negotiable)

1. **No LangChain/LlamaIndex/agent frameworks.** Core logic is plain Python we
   can explain line-by-line in an interview. New deps need a one-line justification.
2. **Evals before features.** No numbers → no merge. Every experiment gets an
   append-only entry in `evals/RESULTS.md` (template inside).
3. **Test set is sacred.** Eval/test items never leak into training data or
   few-shot prompts. Flag loudly if code risks leakage.
4. **Grounded or refuse.** Answers cite article-level sources; if context lacks
   the answer, refuse explicitly. Never guess.
5. **Deterministic where possible.** Arithmetic/tax math = Python code, never LLM.
6. **Cost & latency are metrics** — every RESULTS.md row includes p50 latency and
   free-tier requests consumed.
7. **Reproducible:** result = commit hash + config + eval-set version.

## Numbers Are [INITIAL], Not Law

All thresholds below are starting points, NOT measured truths. Calibrate after
baseline: run the retrieval eval 3× on the same config, record the std-dev in
RESULTS.md, and set gates relative to that noise. Until then treat as guidance:
chunk size 150–450 tokens · eval set ≥120 items · gate: Recall@5 drop >0.02 or
faithfulness drop >0.03 fails (`evals/gate_check.py`, run manually before every
merge from Phase 1 — don't wait for CI) · judge–human agreement ≥0.8 before
trusting judge numbers.

## Conventions (solo-scale)

- `ruff format` + `ruff check` before commit; type hints + Pydantic models at
  module boundaries; no `os.environ` outside `config.py`; no prompt strings in
  Python (→ `prompts/` with version frontmatter, bump version = rerun evals).
- Commit messages: free-form but must say what + why. `exp/` branches merge only
  with their RESULTS.md entry. That's the whole process — no PR templates, no
  nightly jobs, no mypy-strict until Phase 4 (if ever).
- Ask before destructive ops (deleting data, rewriting files wholesale). For
  non-trivial technical decisions, add one sentence of rationale — this is a
  learning project; the owner must be able to defend every choice in interviews.
- Errors: typed exceptions per module; external calls get timeout + 1 retry with
  backoff. Logging: structured, log chunk_ids never full document text, never keys.

## Data Rules

- Corpus reproducible via `data/raw/MANIFEST.json` (source URL + retrieval date).
  `data/raw|processed` gitignored; only `data/samples/` committed.
- Court decisions contain personal data: **no labeling, training, or publishing
  before the anonymization pipeline in `docs/data-privacy.md` runs.** Non-negotiable.
- Scrape politely: rate-limit requests, identify User-Agent.

## Commands

```bash
uv run python -m scripts.healthcheck   # EXISTS — env/qdrant sanity
uv sync --extra embed                  # when ingestion needs sentence-transformers (torch ~2GB)
uv run pytest                          # EXISTS — no network, no paid APIs, no model downloads
uv run ruff check . && uv run ruff format --check .   # EXISTS
# PLANNED (add here as they become real):
# uv run python -m ingestion.run
# uv run python -m evals.run_retrieval
# uv run python -m evals.gate_check
```

## What NOT to Do

No features outside the current phase · no optimization before a measured
baseline · no spending money · no editing past RESULTS.md entries · no synthetic
eval items counted before human review · no UI polish beyond functional · no
README claims without a reproducible number · never skip the legal disclaimer.
