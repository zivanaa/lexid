"""End-to-end naive RAG: retrieve top-k → generate grounded answer.

This is the Phase 1 baseline whose numbers go into evals/RESULTS.md first;
every later experiment changes exactly one variable relative to this.
"""

import time

from pydantic import BaseModel

from rag.generate import GeneratedAnswer, generate
from rag.retrieve import RetrievedChunk, retrieve

# Appended verbatim if the model forgets rule 5 of the prompt — the disclaimer
# is mandatory on every user-facing surface, so it cannot depend on the LLM.
DISCLAIMER = "Catatan: ini alat riset, bukan nasihat hukum."


class RAGResponse(BaseModel):
    question: str
    answer: str
    chunks: list[RetrievedChunk]
    generation: GeneratedAnswer
    total_latency_ms: int


def ask(
    question: str,
    k: int = 5,
    provider: str = "gemini",
    model: str | None = None,
) -> RAGResponse:
    t0 = time.perf_counter()
    chunks = retrieve(question, k=k)
    gen = generate(question, chunks, provider=provider, model=model)

    answer = gen.text
    if DISCLAIMER not in answer:
        answer = f"{answer}\n\n{DISCLAIMER}"

    return RAGResponse(
        question=question,
        answer=answer,
        chunks=chunks,
        generation=gen,
        total_latency_ms=int((time.perf_counter() - t0) * 1000),
    )
