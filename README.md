# LexID — Asisten Riset Hukum & Pajak Indonesia (WIP)

Portfolio capstone: RAG + evaluation pipeline, fine-tuned NER, agentic tool use, MLOps.
**Zero-budget build**: free-tier LLM APIs, local embeddings, embedded vector DB, free deploy.

> ⚠️ LexID adalah alat riset, bukan nasihat hukum.

Status: Phase 1 (RAG foundation). See `CLAUDE.md` for working rules, `docs/` for specs.

## Quickstart
```bash
uv sync --extra embed         # embedding deps incl. torch (~2GB, sekali saja)
cp .env.example .env          # isi GEMINI_API_KEY utk generation; kosong = retrieve-only
uv run python -m scripts.healthcheck
uv run pytest
```

## Menyiapkan korpus (sekali saja)

PDF korpus tidak di-commit (gitignored). Unduh kedua file di
`data/raw/MANIFEST.json` (field `download_url`) dan simpan ke `data/raw/`
dengan nama sesuai field `file`, lalu:

```bash
uv run python -m ingestion.run   # parse → chunk → embed (CPU ~12 mnt) → Qdrant lokal
```

## Bertanya

```bash
uv run python -m rag "Berapa tarif PPh badan dalam negeri?"
uv run python -m rag --retrieve-only "tarif PPh badan"   # tanpa LLM, lihat chunk saja
```
Tanpa API key, perintah pertama otomatis jatuh ke mode retrieve-only.

CI: GitHub Actions runs ruff + pytest on every push/PR (lean install, no model downloads).
