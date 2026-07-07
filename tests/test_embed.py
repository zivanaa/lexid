"""ingestion.embed tests — model is stubbed; no downloads, no torch import."""

import numpy as np
import pytest

import ingestion.embed as embed
from ingestion.embed import EmbedError, embed_texts


class _StubModel:
    def encode(self, texts, batch_size, normalize_embeddings, show_progress_bar):
        assert normalize_embeddings is True
        out = np.ones((len(texts), 4)) / 2.0
        return out


@pytest.fixture
def stub_model(monkeypatch):
    monkeypatch.setattr(embed, "_model", lambda: _StubModel())


def test_embed_shape_and_dtype(stub_model):
    vecs = embed_texts(["pasal 17", "pasal 31E"])
    assert vecs.shape == (2, 4)
    assert vecs.dtype == np.float32


def test_empty_batch_rejected(stub_model):
    with pytest.raises(EmbedError, match="empty"):
        embed_texts([])


def test_blank_text_rejected(stub_model):
    with pytest.raises(EmbedError, match="blank"):
        embed_texts(["ok", "   "])
