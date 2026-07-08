# Experiment Log (append-only, newest on top)

Template:
```
## YYYY-MM-DD — exp-NNN: <short name>
config: <one line> | commit: <hash> | eval set: <name> vN (<items> items)
<primary metrics> | p50 <ms> | cost/query $0 (free tier: <provider>, <requests used>)
per-difficulty: direct X / paraphrase X / multi_hop X / unanswerable X
takeaway: <one line>
```

## 2026-07-08 — exp-001: naive dense retrieval baseline
config: BGE-M3 local CPU (1024-dim) · fixed 250-word/50-overlap chunks · Qdrant embedded exact-cosine · dense top-k, NO rerank/hybrid | commit: 417aa85 | eval set: lexid-retrieval-eval v1.0 (28 scoreable + 4 unanswerable)
recall@3 0.625 · recall@5 0.679 · recall@10 0.839 · MRR 0.588 · NDCG@10 0.615 | p50 ~87 ms/query | cost/query $0 (fully local, 0 free-tier requests)
noise: 3 identical runs → std-dev 0.000 on every metric (exact search is deterministic; only latency jitters). Gates measure real signal, not noise → the [INITIAL] recall@5 −0.02 gate is conservative; any drop >0 is a true regression.
per-difficulty (recall@5): direct 0.75 / paraphrase 0.50 / multi_hop 0.75 / unanswerable n/a (refusal path — measured in generation eval, not retrieval)
takeaway: paraphrase is the weak axis (0.50 vs 0.75 direct) — the live p01 failure ("laba 2023" pulled PPS-deadline chunks) is the archetype. Hybrid BM25+RRF and reranking experiments should target paraphrase first. recall@10 0.84 >> recall@5 0.68 means relevant chunks are often retrieved but ranked 6–10 → reranking is the higher-leverage lever than pure recall widening.

(Older entries below. Never edit past entries — append only.)
