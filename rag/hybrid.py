"""Hybrid retrieval: BM25 (sparse keyword) + dense (BGE-M3), fused via RRF (exp-003).

Dense embeddings blur exact legal terms (pasal numbers, "natura", "royalti",
rupiah amounts); BM25 nails them. Reciprocal Rank Fusion combines the two
ranked lists without needing comparable score scales. Targets the exp-001/002
finding that dense mis-topics some queries (p01 "laba 2023" → PPS chunks).
Local CPU, $0; BM25 via rank-bm25 (already a dependency). rag.retrieve stays
pure dense so its baseline tests remain valid.
"""

import re
from functools import lru_cache

from rank_bm25 import BM25Okapi

from ingestion.index import COLLECTION, get_client
from rag.retrieve import RetrievedChunk, retrieve

RRF_K = 60  # standard RRF constant; damps the weight of deep ranks


class HybridError(Exception):
    """Raised when the BM25 side cannot be built or used."""


def tokenize(text: str) -> list[str]:
    # plain word tokens, lowercased — no stemming (keep it explainable; Indonesian
    # legal text matches well on surface forms like "pasal", "natura", "royalti")
    return re.findall(r"[a-z0-9]+", text.lower())


@lru_cache(maxsize=1)
def _bm25_index() -> tuple[BM25Okapi, tuple[RetrievedChunk, ...]]:
    """Build a BM25 index over ALL chunks in the Qdrant collection (payload has
    the text). Cached: the 218-chunk corpus builds in well under a second."""
    client = get_client()
    if not client.collection_exists(COLLECTION):
        raise HybridError(
            f"collection '{COLLECTION}' not found — run: uv run python -m ingestion.run"
        )
    chunks: list[RetrievedChunk] = []
    offset = None
    while True:
        batch, offset = client.scroll(COLLECTION, limit=256, with_payload=True, offset=offset)
        for p in batch:
            chunks.append(
                RetrievedChunk(
                    chunk_id=p.payload["chunk_id"],
                    doc_id=p.payload["doc_id"],
                    page_start=p.payload["page_start"],
                    page_end=p.payload["page_end"],
                    text=p.payload["text"],
                    score=0.0,
                )
            )
        if offset is None:
            break
    if not chunks:
        raise HybridError(f"collection '{COLLECTION}' is empty")
    bm25 = BM25Okapi([tokenize(c.text) for c in chunks])
    return bm25, tuple(chunks)


def bm25_search(query: str, k: int) -> list[RetrievedChunk]:
    bm25, chunks = _bm25_index()
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(zip(chunks, scores), key=lambda cs: cs[1], reverse=True)[:k]
    return [c.model_copy(update={"score": float(s)}) for c, s in ranked]


def rrf_fuse(
    dense: list[RetrievedChunk], sparse: list[RetrievedChunk], k: int, rrf_k: int = RRF_K
) -> list[RetrievedChunk]:
    """Reciprocal Rank Fusion: each list contributes 1/(rrf_k + rank) per chunk.
    Score scales differ (cosine vs BM25) so we fuse RANKS, not raw scores."""
    fused: dict[str, float] = {}
    meta: dict[str, RetrievedChunk] = {}
    for ranked in (dense, sparse):
        for rank, c in enumerate(ranked, start=1):
            fused[c.chunk_id] = fused.get(c.chunk_id, 0.0) + 1.0 / (rrf_k + rank)
            meta.setdefault(c.chunk_id, c)
    top = sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:k]
    return [meta[cid].model_copy(update={"score": score}) for cid, score in top]


def retrieve_hybrid(
    query: str, k: int = 5, fetch_n: int = 20, rrf_k: int = RRF_K, client=None
) -> list[RetrievedChunk]:
    """Dense top-N and BM25 top-N, fused with RRF to top-k."""
    dense = retrieve(query, k=fetch_n, client=client)
    sparse = bm25_search(query, k=fetch_n)
    return rrf_fuse(dense, sparse, k=k, rrf_k=rrf_k)
