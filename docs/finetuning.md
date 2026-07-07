# Fine-tuning Spec (Phase 2 — do not start before Phase 1 DoD)

Task: NER/structured extraction from Indonesian court decisions → strict JSON:
parties (anonymized), case_number, cited_articles, decision_date, amounts,
verdict_type.

Zero-budget compute: Kaggle free GPU (~30 h/week quota) primary, Colab free T4
fallback. QLoRA 4-bit fits 7B on both. Checkpoints saved to HF Hub (free) so
session disconnects don't lose runs.

Dataset: 1,000–2,000 examples [INITIAL]. Anonymization (docs/data-privacy.md)
runs BEFORE labeling. Labels drafted by a free-tier large model (distillation),
then human review: 100% of test split, ≥20% random sample of train. Splits
80/10/10 stratified, frozen + checksummed in finetuning/dataset/splits/.

Training start point [INITIAL]: r=16, alpha=32, lr=2e-4, cosine, 2 epochs,
effective batch 8–16, max_seq 2048. Log train AND val loss; early-stop on val
rise. 3–5 runs minimum; every run → RESULTS.md.

Deliverable: 4-way comparison on the frozen test set — (a) base zero-shot,
(b) base few-shot (exemplars from TRAIN only), (c) free-tier large-model
few-shot, (d) fine-tuned. Report micro/macro F1, per-entity F1, JSON-validity
rate, p50 latency, and cost/1k requests (free-tier = 0 but REPORT the requests
consumed + what it would cost paid — that's the interview-ready number).
Error analysis: categorize ≥30 errors of (d) → table in README.
Publishing the model: gated by the privacy checklist in docs/data-privacy.md.
