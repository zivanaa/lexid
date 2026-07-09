"""End-to-end RAG: retrieve top-k → generate grounded answer.

Default retriever is HYBRID (BM25+dense RRF), chosen on the evidence: exp-003
showed it beats pure dense by +0.08 recall@5 at ~zero latency cost (90 ms vs
87 ms) — the demo pick. rerank / hybrid_rerank are opt-in for higher quality at
~13 s/query (exp-002/004). Pure dense stays available as the measured baseline.
See evals/RESULTS.md.
"""

import time
from typing import Literal

from pydantic import BaseModel

from rag.generate import GeneratedAnswer, generate
from rag.retrieve import RetrievedChunk

Retriever = Literal["dense", "hybrid", "rerank", "hybrid_rerank"]
DEFAULT_RETRIEVER: Retriever = "hybrid"

# Appended verbatim if the model forgets rule 5 of the prompt — the disclaimer
# is mandatory on every user-facing surface, so it cannot depend on the LLM.
DISCLAIMER = "Catatan: ini alat riset, bukan nasihat hukum."


class RAGResponse(BaseModel):
    question: str
    answer: str
    chunks: list[RetrievedChunk]
    retriever: str
    generation: GeneratedAnswer
    total_latency_ms: int


def retrieve_chunks(
    question: str, k: int = 5, retriever: Retriever = DEFAULT_RETRIEVER
) -> list[RetrievedChunk]:
    """Dispatch to the selected retriever. Lazy imports keep the dense path free
    of rank-bm25 and the cross-encoder unless actually requested."""
    if retriever == "dense":
        from rag.retrieve import retrieve

        return retrieve(question, k=k)
    if retriever == "hybrid":
        from rag.hybrid import retrieve_hybrid

        return retrieve_hybrid(question, k=k)
    if retriever == "rerank":
        from rag.rerank import retrieve_rerank

        return retrieve_rerank(question, k=k)
    if retriever == "hybrid_rerank":
        from rag.rerank import retrieve_hybrid_rerank

        return retrieve_hybrid_rerank(question, k=k)
    raise ValueError(f"unknown retriever '{retriever}'")


def ask(
    question: str,
    k: int = 5,
    retriever: Retriever = DEFAULT_RETRIEVER,
    provider: str = "gemini",
    model: str | None = None,
) -> RAGResponse:
    t0 = time.perf_counter()
    chunks = retrieve_chunks(question, k=k, retriever=retriever)
    gen = generate(question, chunks, provider=provider, model=model)

    answer = gen.text
    if DISCLAIMER not in answer:
        answer = f"{answer}\n\n{DISCLAIMER}"

    return RAGResponse(
        question=question,
        answer=answer,
        chunks=chunks,
        retriever=retriever,
        generation=gen,
        total_latency_ms=int((time.perf_counter() - t0) * 1000),
    )
