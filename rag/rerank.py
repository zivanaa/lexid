"""Cross-encoder reranking over dense-retrieved candidates (exp-002).

Dense bi-encoder retrieval ranks by vector similarity; a cross-encoder scores
each (query, chunk) pair jointly and reorders. Baseline exp-001 showed
recall@10 (0.84) >> recall@5 (0.68) — relevant chunks are retrieved but ranked
6-10 — so reranking is the targeted lever. Model + device from config; local
CPU, $0. rag.retrieve stays pure dense so its baseline tests remain valid.
"""

from functools import lru_cache

from config import settings
from rag.retrieve import RetrievedChunk, retrieve


class RerankError(Exception):
    """Raised when the reranker cannot be loaded or used."""


@lru_cache(maxsize=1)
def _model():
    # Lazy: importing sentence_transformers pulls torch; must not happen for
    # dense-only work or plain test runs.
    try:
        from sentence_transformers import CrossEncoder
    except ImportError as e:
        raise RerankError("sentence-transformers not installed — run: uv sync --extra embed") from e
    try:
        return CrossEncoder(settings.reranker_model, device=settings.embedding_device)
    except Exception as e:
        raise RerankError(f"cannot load reranker '{settings.reranker_model}': {e}") from e


def rerank_chunks(query: str, chunks: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
    """Reorder chunks by cross-encoder relevance to the query; return top_k.

    The returned chunks carry the cross-encoder score (not the dense cosine) so
    downstream sees what actually decided the ranking.
    """
    if not chunks:
        return []
    scores = _model().predict([(query, c.text) for c in chunks])
    ranked = sorted(
        (c.model_copy(update={"score": float(s)}) for c, s in zip(chunks, scores)),
        key=lambda c: c.score,
        reverse=True,
    )
    return ranked[:top_k]


def retrieve_rerank(query: str, k: int = 5, fetch_n: int = 20, client=None) -> list[RetrievedChunk]:
    """Dense-retrieve fetch_n candidates, then cross-encoder rerank to top-k.

    fetch_n > k so the reranker can promote chunks the bi-encoder buried; a
    relevant chunk still has to be in the fetched pool, so fetch_n caps recall.
    """
    if fetch_n < k:
        raise RerankError(f"fetch_n ({fetch_n}) must be >= k ({k})")
    candidates = retrieve(query, k=fetch_n, client=client)
    return rerank_chunks(query, candidates, top_k=k)


def retrieve_hybrid_rerank(
    query: str, k: int = 5, fetch_n: int = 20, client=None
) -> list[RetrievedChunk]:
    """exp-004: hybrid (BM25+dense RRF) candidate pool -> cross-encoder rerank -> top-k.

    Stacks the two winning levers: hybrid pulls keyword matches dense buries into
    the pool, then the cross-encoder reranks that better pool. lazy hybrid import
    keeps dense-only/rerank-only paths free of rank-bm25.
    """
    if fetch_n < k:
        raise RerankError(f"fetch_n ({fetch_n}) must be >= k ({k})")
    from rag.hybrid import retrieve_hybrid

    candidates = retrieve_hybrid(query, k=fetch_n, fetch_n=fetch_n, client=client)
    return rerank_chunks(query, candidates, top_k=k)
