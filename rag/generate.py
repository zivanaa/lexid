"""Retrieved chunks + question → grounded answer via a free-tier LLM.

The prompt (prompts/rag_generation.md, versioned) enforces: cite every claim,
refuse when the context lacks the answer, always end with the disclaimer.
"""

import time

from pydantic import BaseModel

from prompts.loader import load
from rag import llm_client
from rag.retrieve import RetrievedChunk


class GenerationError(Exception):
    """Raised when the LLM call fails or returns nothing usable."""


class GeneratedAnswer(BaseModel):
    text: str
    provider: str
    model: str
    prompt_version: int
    latency_ms: int


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Chunks → context block. chunk_id + pages ride along so the model can
    ground citations and eval scripts can trace claims back to sources."""
    return "\n\n".join(
        f"[{c.chunk_id} | hlm. {c.page_start}-{c.page_end}]\n{c.text}" for c in chunks
    )


def generate(
    question: str,
    chunks: list[RetrievedChunk],
    provider: str = "gemini",
    model: str | None = None,
) -> GeneratedAnswer:
    if not chunks:
        raise GenerationError("no chunks to ground on — refuse upstream instead of calling the LLM")

    prompt_text, version = load("rag_generation")
    prompt = prompt_text.format(context=format_context(chunks), question=question)
    model = model or llm_client.default_model(provider)
    if model is None:
        raise GenerationError(f"provider '{provider}' has no default model — pass one explicitly")

    # timeout + 1 retry with backoff per CLAUDE.md error conventions
    client = llm_client.client(provider).with_options(timeout=60.0, max_retries=1)
    t0 = time.perf_counter()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # deterministic-ish: evals must measure the pipeline, not sampling noise
        )
    except Exception as e:
        raise GenerationError(f"{provider}/{model} call failed: {e}") from e
    latency_ms = int((time.perf_counter() - t0) * 1000)

    text = (resp.choices[0].message.content or "").strip()
    if not text:
        raise GenerationError(f"{provider}/{model} returned an empty answer")

    return GeneratedAnswer(
        text=text,
        provider=provider,
        model=model,
        prompt_version=version,
        latency_ms=latency_ms,
    )
