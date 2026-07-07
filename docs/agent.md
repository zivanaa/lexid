# Agent + Guardrails Spec (Phase 3)

Loop (agent/router.py, plain Python): system prompt + tool schemas → LLM picks
tool or final answer → execute → append → repeat. max_steps=6 [INITIAL]; on cap,
force synthesis with partial=True. Tool errors: 1 retry w/ backoff, then agent
is told the tool failed and must degrade gracefully. Log per step: request_id,
step, tool, truncated args, latency, outcome.

Tools (Pydantic contracts in agent/schemas.py):
- search_regulations(query, law_filter?) → RetrievalResults (wraps rag/pipeline)
- extract_entities(document_text) → ExtractionResult (Phase 2 model)
- calculate_tax(income, taxpayer_type, year) → TaxCalculation — pure Python,
  table-driven unit tests, returns the article applied so answers can cite it

Guardrails:
- Input: domain check (keyword heuristic first — it's free; LLM check only if
  needed), length cap, uploaded docs are DATA never instructions (never enter
  the system prompt; schema-validated outputs).
- Output: citations non-empty unless refused; numeric claims must trace to tool
  results (scripted subset check); disclaimer always appended.

Honesty rule on prompt injection: NO defense is 100%. Do not claim or gate on
100% catch rate. Instead: test N adversarial scenarios (injection inside
uploaded docs, tool-failure, out-of-scope), report catch rate as measured, and
document failures as known limitations. Primary structural mitigations: no
dangerous tools exist, uploads never become instructions, outputs are
schema-validated. Agent eval targets [INITIAL]: task completion ≥80% on 30–50
scenarios; correct-tool-choice rate; mean steps.
