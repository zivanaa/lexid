"""rag.hybrid tests — BM25 index stubbed; no Qdrant, no models."""

import pytest

import rag.hybrid as hybrid
from rag.hybrid import rrf_fuse, tokenize
from rag.retrieve import RetrievedChunk


def _c(cid, score=0.0):
    return RetrievedChunk(
        chunk_id=cid, doc_id="d", page_start=1, page_end=1, text=f"text {cid}", score=score
    )


def test_tokenize_lowercases_and_splits():
    assert tokenize("Pasal 17 ayat (2b)!") == ["pasal", "17", "ayat", "2b"]
    assert tokenize("22% (dua-puluh)") == ["22", "dua", "puluh"]


def test_rrf_fuse_orders_by_reciprocal_rank():
    dense = [_c("a"), _c("b"), _c("c")]  # ranks 1,2,3
    sparse = [_c("c"), _c("a"), _c("b")]  # ranks 1,2,3
    out = rrf_fuse(dense, sparse, k=3, rrf_k=1)
    # a: 1/2+1/3=.833 · c: 1/4+1/2=.75 · b: 1/3+1/4=.583  -> a, c, b
    assert [c.chunk_id for c in out] == ["a", "c", "b"]
    assert out[0].score == pytest.approx(1 / 2 + 1 / 3)


def test_rrf_fuse_rewards_agreement():
    # a chunk both lists rank #1 should win over chunks only one list has
    dense = [_c("x"), _c("a")]
    sparse = [_c("x"), _c("b")]
    out = rrf_fuse(dense, sparse, k=3, rrf_k=1)
    assert out[0].chunk_id == "x"


def test_rrf_fuse_truncates_to_k():
    dense = [_c("a"), _c("b"), _c("c")]
    sparse = [_c("d"), _c("e"), _c("f")]
    assert len(rrf_fuse(dense, sparse, k=2)) == 2


def test_bm25_search_ranks_by_score(monkeypatch):
    chunks = (_c("a"), _c("b"), _c("c"))

    class _StubBM25:
        def get_scores(self, toks):
            return [0.1, 0.9, 0.5]  # b best, then c, then a

    monkeypatch.setattr(hybrid, "_bm25_index", lambda: (_StubBM25(), chunks))
    out = hybrid.bm25_search("q", k=2)
    assert [c.chunk_id for c in out] == ["b", "c"]
    assert out[0].score == pytest.approx(0.9)


def test_retrieve_hybrid_fuses_dense_and_sparse(monkeypatch):
    monkeypatch.setattr(hybrid, "retrieve", lambda q, k, client=None: [_c("a"), _c("b")])
    monkeypatch.setattr(hybrid, "bm25_search", lambda q, k: [_c("b"), _c("c")])
    out = hybrid.retrieve_hybrid("q", k=3, rrf_k=1)
    # b appears in both (1/3+1/2) -> top; a (1/2) ; c (1/3)
    assert out[0].chunk_id == "b"
    assert {c.chunk_id for c in out} == {"a", "b", "c"}
