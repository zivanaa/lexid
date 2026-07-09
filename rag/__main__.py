"""CLI for the RAG pipeline.

    uv run python -m rag "Berapa tarif PPh badan?"          # full RAG (needs API key)
    uv run python -m rag --retrieve-only "tarif PPh badan"  # no LLM, just chunks
    uv run python -m rag --retriever rerank "..."           # higher quality, ~13 s/query

Default retriever is hybrid (exp-003: best quality/latency trade-off). Falls
back to retrieve-only with a notice when no API key is configured, so the
pipeline is inspectable before the owner creates keys.
"""

import argparse
import sys

from rag.pipeline import DEFAULT_RETRIEVER, DISCLAIMER, ask, retrieve_chunks


def _print_chunks(chunks) -> None:
    for c in chunks:
        print(f"  [{c.chunk_id}] hlm. {c.page_start}-{c.page_end}  skor {c.score:.3f}")
        print(f"    {c.text[:200]}{'…' if len(c.text) > 200 else ''}")


def main() -> int:
    ap = argparse.ArgumentParser(prog="rag", description="LexID RAG CLI")
    ap.add_argument("question")
    ap.add_argument("--k", type=int, default=5, help="jumlah chunk yang diambil (default 5)")
    ap.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openrouter"])
    ap.add_argument(
        "--retriever",
        default=DEFAULT_RETRIEVER,
        choices=["dense", "hybrid", "rerank", "hybrid_rerank"],
        help=f"strategi retrieval (default {DEFAULT_RETRIEVER}; rerank/hybrid_rerank ~13 s/query)",
    )
    ap.add_argument("--retrieve-only", action="store_true", help="tanpa LLM: tampilkan chunk saja")
    args = ap.parse_args()

    if args.retrieve_only:
        _print_chunks(retrieve_chunks(args.question, k=args.k, retriever=args.retriever))
        print(f"\n[retriever: {args.retriever}]\n{DISCLAIMER}")
        return 0

    try:
        resp = ask(args.question, k=args.k, retriever=args.retriever, provider=args.provider)
    except RuntimeError as e:  # no API key for the provider (rag/llm_client.py)
        print(f"[info] {e}")
        print("[info] jatuh ke mode retrieve-only:\n")
        _print_chunks(retrieve_chunks(args.question, k=args.k, retriever=args.retriever))
        print(f"\n[retriever: {args.retriever}]\n{DISCLAIMER}")
        return 0

    print(resp.answer)
    print(f"\nSumber ({len(resp.chunks)} chunk, retriever: {resp.retriever}):")
    _print_chunks(resp.chunks)
    print(
        f"\n[{resp.generation.provider}/{resp.generation.model}"
        f" | prompt v{resp.generation.prompt_version}"
        f" | LLM {resp.generation.latency_ms} ms | total {resp.total_latency_ms} ms]"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
