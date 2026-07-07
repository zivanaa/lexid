"""Sanity check: env, imports, embedded Qdrant roundtrip, provider keys.

Run: uv run python -m scripts.healthcheck
Exits 0 if the environment can support Phase 1 work.
"""
import sys
from pathlib import Path


def main() -> int:
    ok = True

    if not Path(".env").exists():
        print("[warn] .env not found — copy .env.example (keys optional for retrieval work)")

    try:
        from config import settings
        print(f"[ok] config loaded (embedding={settings.embedding_model}, device={settings.embedding_device})")
    except Exception as e:
        print(f"[FAIL] config: {e}")
        return 1

    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, PointStruct, VectorParams

        client = QdrantClient(path=settings.qdrant_path)  # embedded local mode, no Docker
        name = "_healthcheck"
        if client.collection_exists(name):
            client.delete_collection(name)
        client.create_collection(name, vectors_config=VectorParams(size=4, distance=Distance.COSINE))
        client.upsert(name, points=[PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"t": "x"})])
        hit = client.query_points(name, query=[0.1, 0.2, 0.3, 0.4], limit=1).points[0]
        assert hit.payload["t"] == "x"
        client.delete_collection(name)
        print(f"[ok] embedded qdrant roundtrip at {settings.qdrant_path}")
    except Exception as e:
        print(f"[FAIL] qdrant local mode: {e}")
        ok = False

    keys = {
        "gemini": settings.gemini_api_key,
        "groq": settings.groq_api_key,
        "openrouter": settings.openrouter_api_key,
    }
    configured = [k for k, v in keys.items() if v]
    if configured:
        print(f"[ok] LLM providers configured: {', '.join(configured)}")
    else:
        print("[warn] no LLM provider keys — fine for retrieval work; needed for generation/judge evals")

    print("[done] healthcheck", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
