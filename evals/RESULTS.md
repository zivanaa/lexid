# Experiment Log (append-only, newest on top)

Template:
```
## YYYY-MM-DD — exp-NNN: <short name>
config: <one line> | commit: <hash> | eval set: <name> vN (<items> items)
<primary metrics> | p50 <ms> | cost/query $0 (free tier: <provider>, <requests used>)
per-difficulty: direct X / paraphrase X / multi_hop X / unanswerable X
takeaway: <one line>
```

## 2026-07-09 — v1.1 re-baseline (eval set grew 28→50 scoreable; these SUPERSEDE the v1.0 numbers as the reference for exp-003+)
Why: eval set v1.1 changed the item mix, so v1.0 numbers below are not comparable to future runs. Both current configs re-measured on v1.1. Same code as exp-001/002 (commits 417aa85 / 3af9f50); measured at commit 9787639.

exp-002b — dense+rerank on v1.1: recall@3 0.79 · recall@5 0.84 · recall@10 0.92 · MRR 0.736 · NDCG@10 0.773 (1 run; determinism established exp-002 3× std 0) | p50 ~12.9 s/query | $0
  vs dense v1.1 (gate PASS): recall@5 +0.15 · recall@3 +0.13 · recall@10 +0.10 · MRR +0.164 · NDCG@10 +0.158
  per-difficulty (recall@5): direct 0.893 / paraphrase 0.714 / multi_hop 0.875
exp-001b — dense baseline on v1.1: recall@3 0.66 · recall@5 0.69 · recall@10 0.82 · MRR 0.571 · NDCG@10 0.616 (mean of 3 runs, std-dev 0.000) | p50 ~87 ms/query | $0
  per-difficulty (recall@5): direct 0.786 / paraphrase 0.50 / multi_hop 0.688
takeaway: rerank win holds on the bigger set (recall@5 +0.15), and paraphrase 0.50→0.714 (+0.21) is now measured over 14 items (was 8) → more trustworthy. n=50 ⇒ resolution 1/50 = 0.020 = the gate exactly, so gate_check no longer warns (aggregate is resolvable); per-difficulty still coarse (multi_hop n=8, paraphrase n=14). Dense recall@5 0.69 ≈ v1.0's 0.679 → the growth batch didn't skew difficulty. **exp-003 (hybrid BM25) must beat dense v1.1 recall@5 0.69**, and its real target is paraphrase 0.50.

## 2026-07-09 — exp-002: + cross-encoder rerank (BGE-reranker-v2-m3)
config: dense fetch top-20 → BGE-reranker-v2-m3 cross-encoder → top-k · same BGE-M3 index/chunks as exp-001 | commit: 3af9f50 | eval set: lexid-retrieval-eval v1.0 (28 scoreable + 4 unanswerable)
recall@3 0.821 · recall@5 0.821 · recall@10 0.893 · MRR 0.734 · NDCG@10 0.766 (mean of 3 runs, std-dev 0.000 — deterministic like exp-001) | p50 ~13 s/query (12.9–13.8 s) | cost/query $0 (fully local, 0 free-tier requests)
vs exp-001 (gate PASS): recall@5 +0.143 · recall@3 +0.196 · MRR +0.146 · NDCG@10 +0.150 · recall@10 +0.054
per-difficulty (recall@5): direct 0.75→0.875 / paraphrase 0.50→0.625 / multi_hop 0.75→1.00 / unanswerable n/a
takeaway: hypothesis confirmed — reranking pulled the recall@10 headroom (0.84) into recall@5 (0.82); every metric up, biggest lift on ranking-sensitive MRR/NDCG. COST: latency 87 ms → ~13 s/query (cross-encoder scores 20 pairs on CPU) — likely too slow for the interactive HF-CPU demo as-is; follow-ups: smaller fetch_n, a lighter reranker, or rerank only when dense scores are low. paraphrase still the floor (0.625) even after rerank → the p01-style "wrong-topic dense recall" isn't fixed by reordering; needs hybrid BM25 or better query handling (candidate exp-003). NOTE: n=28 → aggregate resolution 0.036; this +0.143 is far above noise, but per-difficulty cells (esp. multi_hop n=4) are coarse — grow the eval set before trusting small deltas.

## 2026-07-08 — exp-001: naive dense retrieval baseline
config: BGE-M3 local CPU (1024-dim) · fixed 250-word/50-overlap chunks · Qdrant embedded exact-cosine · dense top-k, NO rerank/hybrid | commit: 417aa85 | eval set: lexid-retrieval-eval v1.0 (28 scoreable + 4 unanswerable)
recall@3 0.625 · recall@5 0.679 · recall@10 0.839 · MRR 0.588 · NDCG@10 0.615 | p50 ~87 ms/query | cost/query $0 (fully local, 0 free-tier requests)
noise: 3 identical runs → std-dev 0.000 on every metric (exact search is deterministic; only latency jitters). Gates measure real signal, not noise → the [INITIAL] recall@5 −0.02 gate is conservative; any drop >0 is a true regression.
per-difficulty (recall@5): direct 0.75 / paraphrase 0.50 / multi_hop 0.75 / unanswerable n/a (refusal path — measured in generation eval, not retrieval)
takeaway: paraphrase is the weak axis (0.50 vs 0.75 direct) — the live p01 failure ("laba 2023" pulled PPS-deadline chunks) is the archetype. Hybrid BM25+RRF and reranking experiments should target paraphrase first. recall@10 0.84 >> recall@5 0.68 means relevant chunks are often retrieved but ranked 6–10 → reranking is the higher-leverage lever than pure recall widening.

(Older entries below. Never edit past entries — append only.)
