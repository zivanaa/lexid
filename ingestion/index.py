"""Chunks + vectors → embedded Qdrant collection (local path, no server).

Point ids are UUID5 of chunk_id (Qdrant rejects arbitrary strings as ids);
the payload keeps chunk_id/doc_id/pages/text so retrieval needs no side store.
"""

import uuid

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Filter, FilterSelector, PointStruct, VectorParams

from config import settings
from ingestion.chunk import Chunk

COLLECTION = "lexid_chunks"


class IndexingError(Exception):
    """Raised when chunks/vectors cannot be written to the index."""


def get_client() -> QdrantClient:
    return QdrantClient(path=settings.qdrant_path)


def point_id(chunk_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_id))


def build_index(
    client: QdrantClient,
    chunks: list[Chunk],
    vectors: np.ndarray,
    collection: str = COLLECTION,
    recreate: bool = False,
) -> int:
    """Upsert chunks with their vectors; returns number of points written."""
    if len(chunks) != len(vectors):
        raise IndexingError(f"{len(chunks)} chunks but {len(vectors)} vectors")
    if not chunks:
        raise IndexingError("nothing to index")

    dim = int(vectors.shape[1])
    if client.collection_exists(collection):
        existing_dim = client.get_collection(collection).config.params.vectors.size
        if existing_dim != dim:
            raise IndexingError(
                f"collection '{collection}' holds {existing_dim}-dim vectors, got {dim} — "
                f"embedding model changed; delete {settings.qdrant_path} and re-ingest"
            )
        if recreate:
            # NOT delete_collection: qdrant-client local mode on Windows keeps the
            # sqlite file locked, so a deleted collection resurrects its old points
            # on re-create. Clearing points via empty filter actually persists.
            client.delete(collection, points_selector=FilterSelector(filter=Filter()))
    else:
        client.create_collection(
            collection,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

    points = [
        PointStruct(
            id=point_id(c.chunk_id),
            vector=v.tolist(),
            payload={
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "page_start": c.page_start,
                "page_end": c.page_end,
                "text": c.text,
            },
        )
        for c, v in zip(chunks, vectors)
    ]
    client.upsert(collection, points=points)
    return len(points)
