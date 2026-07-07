"""Skeleton smoke tests — no paid APIs, no network, no model downloads."""

from prompts.loader import load


def test_config_loads():
    from config import settings

    assert settings.embedding_device in ("cpu", "cuda")


def test_prompt_loader_roundtrip():
    text, version = load("rag_generation")
    assert "{context}" in text and "{question}" in text
    assert version >= 1


def test_qdrant_local_mode(tmp_path):
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams

    c = QdrantClient(path=str(tmp_path / "q"))
    c.create_collection("t", vectors_config=VectorParams(size=3, distance=Distance.COSINE))
    c.upsert("t", points=[PointStruct(id=1, vector=[1.0, 0.0, 0.0], payload={"a": 1})])
    assert c.query_points("t", query=[1.0, 0.0, 0.0], limit=1).points[0].payload["a"] == 1
