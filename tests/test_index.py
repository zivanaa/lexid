"""ingestion.index tests — tmp Qdrant path, random vectors, no models."""

import numpy as np
import pytest
from qdrant_client import QdrantClient

from ingestion.chunk import Chunk
from ingestion.index import IndexingError, build_index, point_id


def _chunks(n: int) -> list[Chunk]:
    return [
        Chunk(
            chunk_id=f"doc:{i:04d}",
            doc_id="doc",
            seq=i,
            text=f"isi chunk {i}",
            page_start=i + 1,
            page_end=i + 1,
            n_words=3,
        )
        for i in range(n)
    ]


@pytest.fixture
def client(tmp_path):
    return QdrantClient(path=str(tmp_path / "q"))


def test_roundtrip_payload(client):
    rng = np.random.default_rng(0)
    vecs = rng.random((3, 8), dtype=np.float32)
    written = build_index(client, _chunks(3), vecs, collection="t")
    assert written == 3
    hit = client.query_points("t", query=vecs[1].tolist(), limit=1).points[0]
    assert hit.payload["chunk_id"] == "doc:0001"
    assert hit.payload["text"] == "isi chunk 1"


def test_recreate_drops_stale_points(client):
    rng = np.random.default_rng(0)
    build_index(client, _chunks(5), rng.random((5, 8), dtype=np.float32), collection="t")
    build_index(
        client, _chunks(2), rng.random((2, 8), dtype=np.float32), collection="t", recreate=True
    )
    assert client.count("t").count == 2


def test_dim_change_rejected(client):
    rng = np.random.default_rng(0)
    build_index(client, _chunks(2), rng.random((2, 8), dtype=np.float32), collection="t")
    with pytest.raises(IndexingError, match="dim"):
        build_index(client, _chunks(2), rng.random((2, 16), dtype=np.float32), collection="t")


def test_length_mismatch_rejected(client):
    with pytest.raises(IndexingError, match="chunks but"):
        build_index(client, _chunks(2), np.ones((3, 8), dtype=np.float32), collection="t")


def test_point_id_deterministic():
    assert point_id("a:0001") == point_id("a:0001")
    assert point_id("a:0001") != point_id("a:0002")
