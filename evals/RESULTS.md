# Experiment Log (append-only, newest on top)

Template:
```
## YYYY-MM-DD — exp-NNN: <short name>
config: <one line> | commit: <hash> | eval set: <name> vN (<items> items)
<primary metrics> | p50 <ms> | cost/query $0 (free tier: <provider>, <requests used>)
per-difficulty: direct X / paraphrase X / multi_hop X / unanswerable X
takeaway: <one line>
```

## 2026-07-09 — exp-004: hybrid + rerank stacked (best config so far)
config: hybrid (BM25+dense RRF, fetch-20) candidate pool → BGE-reranker-v2-m3 cross-encoder → top-k | commit: a44f968 | eval set: v1.1 (50 scoreable + 6 unanswerable)
recall@3 0.81 · recall@5 0.86 · recall@10 0.96 · MRR 0.748 · NDCG@10 0.791 (1 run; determinism established exp-001/002/003, all std 0) | p50 ~13 s/query | cost/query $0 (fully local)
vs dense v1.1 (gate PASS): recall@5 +0.17 · recall@10 +0.14 · MRR +0.176 · NDCG@10 +0.175
vs rerank v1.1 (gate PASS): recall@5 +0.02 · recall@10 +0.04 · MRR +0.012 · NDCG@10 +0.018
per-difficulty (recall@5): direct 0.893 / paraphrase 0.786 / multi_hop 0.875
takeaway: best on EVERY metric — recall@10 0.96 (almost all relevant chunks reach top-10) because hybrid feeds the reranker a richer pool than dense alone, and paraphrase 0.786 is the best yet (dense 0.50 → hybrid 0.643 → rerank 0.714 → stack 0.786). Edge over rerank-alone is modest: recall@5 +0.02 = 1 item at the n=50 resolution floor, but recall@10 +0.04 and paraphrase +0.07 are clearer. Latency ~13 s = same as rerank (BM25 adds ~ms; cross-encoder dominates) → if you're paying for rerank, stacking hybrid is a free upgrade. Final retrieval ranking (recall@5): dense 0.69 < hybrid 0.77 < rerank 0.84 < hybrid+rerank 0.86. Demo pick = hybrid (0.77 @ 90 ms); quality pick = hybrid+rerank (0.86 @ 13 s). Retrieval axis well-explored; next Phase-1 piece is generation eval (run_generation.py).

## 2026-07-09 — exp-003: hybrid BM25 + dense (RRF fusion)
config: BM25 (rank-bm25, over Qdrant payloads) + dense BGE-M3, Reciprocal Rank Fusion rrf_k=60, fetch-20 each → top-k | commit: 16e65f9 | eval set: v1.1 (50 scoreable + 6 unanswerable)
recall@3 0.69 · recall@5 0.77 · recall@10 0.88 · MRR 0.616 · NDCG@10 0.671 (mean of 3 runs, std-dev 0.000) | p50 ~90 ms/query | cost/query $0 (fully local)
vs dense v1.1 (gate PASS): recall@5 +0.08 · recall@3 +0.03 · recall@10 +0.06 · MRR +0.045 · NDCG@10 +0.056
per-difficulty (recall@5): direct 0.786→0.857 / paraphrase 0.50→0.643 / multi_hop 0.688→0.688 / unanswerable n/a
takeaway: hybrid beats dense (+0.08 recall@5) at ~zero latency cost (90 ms vs 87 ms). My stated hypothesis — "BM25 won't help paraphrase" — was WRONG: paraphrase 0.50→0.643 (+0.14), because colloquial queries still share surface keywords with the legal text ("dividen", "warisan", "zakat"). multi_hop unchanged (0.688) → RRF didn't help the 2-fact items. Ranking vs rerank (both v1.1): rerank recall@5 0.84 > hybrid 0.77, BUT rerank costs ~13 s/query vs hybrid's 90 ms → hybrid is the demo-friendly win; rerank is the quality ceiling. Candidate exp-004: stack them (hybrid fuse → rerank top-N) for best-of-both when a latency budget allows.

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
