"""CLI for the naive RAG baseline.

    uv run python -m rag "Berapa tarif PPh badan?"          # full RAG (needs API key)
    uv run python -m rag --retrieve-only "tarif PPh badan"  # no LLM, just chunks

Falls back to retrieve-only with a notice when no API key is configured,
so the pipeline is inspectable before the owner creates keys.
"""

import argparse
import sys

from rag.pipeline import DISCLAIMER, ask
from rag.retrieve import retrieve


def _print_chunks(chunks) -> None:
    for c in chunks:
        print(f"  [{c.chunk_id}] hlm. {c.page_start}-{c.page_end}  skor {c.score:.3f}")
        print(f"    {c.text[:200]}{'…' if len(c.text) > 200 else ''}")


def main() -> int:
    ap = argparse.ArgumentParser(prog="rag", description="LexID naive RAG baseline")
    ap.add_argument("question")
    ap.add_argument("--k", type=int, default=5, help="jumlah chunk yang diambil (default 5)")
    ap.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openrouter"])
    ap.add_argument("--retrieve-only", action="store_true", help="tanpa LLM: tampilkan chunk saja")
    args = ap.parse_args()

    if args.retrieve_only:
        chunks = retrieve(args.question, k=args.k)
        _print_chunks(chunks)
        print(f"\n{DISCLAIMER}")
        return 0

    try:
        resp = ask(args.question, k=args.k, provider=args.provider)
    except RuntimeError as e:  # no API key for the provider (rag/llm_client.py)
        print(f"[info] {e}")
        print("[info] jatuh ke mode retrieve-only:\n")
        _print_chunks(retrieve(args.question, k=args.k))
        print(f"\n{DISCLAIMER}")
        return 0

    print(resp.answer)
    print(f"\nSumber ({len(resp.chunks)} chunk):")
    _print_chunks(resp.chunks)
    print(
        f"\n[{resp.generation.provider}/{resp.generation.model}"
        f" | prompt v{resp.generation.prompt_version}"
        f" | LLM {resp.generation.latency_ms} ms | total {resp.total_latency_ms} ms]"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
