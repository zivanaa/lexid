"""Texts → normalized dense vectors via a local sentence-transformers model.

Model + device come from config (default BAAI/bge-m3 on CPU — $0). BGE-M3
needs no query/passage instruction prefixes, so one embed function serves
both sides; the eval matrix compares alternatives later.
"""

from functools import lru_cache

import numpy as np

from config import settings


class EmbedError(Exception):
    """Raised when the embedding model cannot be loaded or used."""


@lru_cache(maxsize=1)
def _model():
    # Lazy: importing sentence_transformers pulls in torch (~seconds, ~GBs),
    # which must not happen for retrieval-free work or plain test runs.
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise EmbedError("sentence-transformers not installed — run: uv sync --extra embed") from e
    try:
        return SentenceTransformer(settings.embedding_model, device=settings.embedding_device)
    except Exception as e:
        raise EmbedError(f"cannot load embedding model '{settings.embedding_model}': {e}") from e


def embed_texts(texts: list[str], batch_size: int = 16) -> np.ndarray:
    """Return a (len(texts), dim) float32 array of L2-normalized vectors."""
    if not texts:
        raise EmbedError("nothing to embed: empty text list")
    if any(not t.strip() for t in texts):
        raise EmbedError("blank text in batch — upstream chunking should never produce this")
    vecs = _model().encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,  # cosine == dot product; Qdrant collection uses COSINE
        show_progress_bar=False,
    )
    return np.asarray(vecs, dtype=np.float32)
