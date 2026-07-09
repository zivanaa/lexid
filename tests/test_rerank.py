"""rag.rerank tests — cross-encoder stubbed; no model download, no torch."""

import pytest

import rag.rerank as rerank
from rag.rerank import RerankError, rerank_chunks, retrieve_rerank
from rag.retrieve import RetrievedChunk


def _chunks(scores_by_id):
    # dense order deliberately NOT the relevance order, so rerank must change it
    return [
        RetrievedChunk(
            chunk_id=cid, doc_id="d", page_start=1, page_end=1, text=f"text {cid}", score=dense
        )
        for cid, dense in scores_by_id
    ]


class _StubCE:
    """Cross-encoder that scores by a lookup on the passage text."""

    def __init__(self, text_to_score):
        self._m = text_to_score

    def predict(self, pairs):
        return [self._m[passage] for _query, passage in pairs]


@pytest.fixture
def stub_ce(monkeypatch):
    def _install(mapping):
        monkeypatch.setattr(rerank, "_model", lambda: _StubCE(mapping))

    return _install


def test_rerank_reorders_by_cross_encoder(stub_ce):
    chunks = _chunks([("a", 0.9), ("b", 0.8), ("c", 0.7)])  # dense: a,b,c
    stub_ce({"text a": 0.1, "text b": 0.2, "text c": 0.99})  # CE says c best, a worst
    out = rerank_chunks("q", chunks, top_k=3)
    assert [c.chunk_id for c in out] == ["c", "b", "a"]
    assert out[0].score == pytest.approx(0.99)  # carries CE score, not dense


def test_rerank_truncates_to_top_k(stub_ce):
    chunks = _chunks([("a", 0.9), ("b", 0.8), ("c", 0.7)])
    stub_ce({"text a": 0.1, "text b": 0.9, "text c": 0.5})
    out = rerank_chunks("q", chunks, top_k=2)
    assert [c.chunk_id for c in out] == ["b", "c"]


def test_rerank_empty_returns_empty(stub_ce):
    stub_ce({})
    assert rerank_chunks("q", [], top_k=5) == []


def test_retrieve_rerank_fetches_more_then_cuts(monkeypatch, stub_ce):
    fetched = _chunks([(c, 0.5) for c in ["a", "b", "c", "d", "e"]])
    seen = {}

    def _fake_retrieve(query, k, client=None):
        seen["k"] = k
        return fetched

    monkeypatch.setattr(rerank, "retrieve", _fake_retrieve)
    stub_ce({f"text {c}": i for i, c in enumerate(["a", "b", "c", "d", "e"])})  # e best
    out = retrieve_rerank("q", k=2, fetch_n=5)
    assert seen["k"] == 5  # fetched the wider pool
    assert [c.chunk_id for c in out] == ["e", "d"]  # top-2 after rerank


def test_retrieve_rerank_rejects_fetch_smaller_than_k():
    with pytest.raises(RerankError, match="must be >="):
        retrieve_rerank("q", k=10, fetch_n=5)


def test_retrieve_hybrid_rerank_reranks_hybrid_pool(monkeypatch, stub_ce):
    from rag.rerank import retrieve_hybrid_rerank

    pool = _chunks([(c, 0.5) for c in ["a", "b", "c", "d"]])
    seen = {}

    def _fake_hybrid(query, k, fetch_n, client=None):
        seen["k"], seen["fetch_n"] = k, fetch_n
        return pool

    monkeypatch.setattr("rag.hybrid.retrieve_hybrid", _fake_hybrid)
    stub_ce({f"text {c}": i for i, c in enumerate(["a", "b", "c", "d"])})  # d best
    out = retrieve_hybrid_rerank("q", k=2, fetch_n=4)
    assert seen == {"k": 4, "fetch_n": 4}  # hybrid asked for the full pool
    assert [c.chunk_id for c in out] == ["d", "c"]  # cross-encoder order, top-2
