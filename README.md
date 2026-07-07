# LexID — Asisten Riset Hukum & Pajak Indonesia (WIP)

Portfolio capstone: RAG + evaluation pipeline, fine-tuned NER, agentic tool use, MLOps.
**Zero-budget build**: free-tier LLM APIs, local embeddings, embedded vector DB, free deploy.

> ⚠️ LexID adalah alat riset, bukan nasihat hukum.

Status: Phase 1 (RAG foundation). See `CLAUDE.md` for working rules, `docs/` for specs.

## Quickstart
```bash
uv sync                       # fast — heavy embedding deps are optional
cp .env.example .env          # keys optional for retrieval-only work
uv run python -m scripts.healthcheck
uv run pytest
# later, when building the ingestion pipeline:
uv sync --extra embed         # pulls sentence-transformers + torch (~2GB)
```

CI: GitHub Actions runs ruff + pytest on every push/PR (lean install, no model downloads).
