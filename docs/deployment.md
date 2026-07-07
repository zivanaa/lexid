# Deployment & Monitoring (Phase 4) — zero-budget edition

Serve: FastAPI + minimal Streamlit UI on Hugging Face Spaces FREE CPU tier.
Qdrant stays embedded (local path) — no server to pay for. NER model for the
demo: GGUF 4-bit on CPU via llama-cpp (7B Q4 ≈ 5GB RAM; free Space has ~16GB;
slow ~ tokens/sec — acceptable for a demo, say so in the UI). If too slow,
fallback: demo the NER via a Kaggle notebook link instead of live serving.

Public-demo protection (a free demo backed by free-tier API keys can still be
griefed into quota exhaustion): per-IP rate limit, daily global cap that
disables generation (retrieval-only mode) when hit, and no raw key exposure.

Log persistence: HF Spaces storage is EPHEMERAL — JSONL logs vanish on restart.
Free fix: append logs to a private HF Dataset repo (free) in batches; dashboard
reads from it. Decide + implement before claiming "monitoring" in the README.

Monitoring dashboard (Streamlit page): p50/p95 latency, requests/day vs free-tier
caps, refusal rate, tool mix, guardrail triggers. Grafana NOT required.

CI (GitHub Actions free tier): ruff + pytest on PR. Eval-regression job runs
retrieval evals ONLY with a tiny CPU embedding model on data/samples (no 2GB
model downloads in CI); generation-eval regression stays a manual pre-merge
step (free-tier quota is not for CI). Document this trade-off in README.
