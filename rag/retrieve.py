"""Dense top-k retrieval over the embedded Qdrant index.

Naive baseline: single dense query, no hybrid/rerank — those are
experiment-matrix variables (docs/evals.md) gated on the measured baseline.
"""

from pydantic import BaseModel
from qdrant_client import QdrantClient

from ingestion.embed import embed_texts
from ingestion.index import COLLECTION, get_client


class RetrievalError(Exception):
    """Raised when a query cannot be answered from the index."""


class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    page_start: int
    page_end: int
    text: str
    score: float  # cosine similarity (vectors are L2-normalized at index time)


def retrieve(
    query: str,
    k: int = 5,
    client: QdrantClient | None = None,
    collection: str = COLLECTION,
) -> list[RetrievedChunk]:
    """Return the k most similar chunks for a natural-language query."""
    if not query.strip():
        raise RetrievalError("empty query")
    client = client or get_client()
    if not client.collection_exists(collection):
        raise RetrievalError(
            f"collection '{collection}' not found — run: uv run python -m ingestion.run"
        )

    vector = embed_texts([query])[0]
    points = client.query_points(collection, query=vector.tolist(), limit=k).points
    return [
        RetrievedChunk(
            chunk_id=p.payload["chunk_id"],
            doc_id=p.payload["doc_id"],
            page_start=p.payload["page_start"],
            page_end=p.payload["page_end"],
            text=p.payload["text"],
            score=p.score,
        )
        for p in points
    ]
