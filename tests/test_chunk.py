"""ingestion.chunk tests — pure logic + the committed 4-page sample."""

from pathlib import Path

import pytest

from ingestion.chunk import Chunk, ChunkError, chunk_document
from ingestion.parse import Page, ParsedDocument, parse_pdf

SAMPLE = Path(__file__).parent.parent / "data" / "samples" / "uu-7-2021-hpp-excerpt.pdf"


def _doc(n_words: int, words_per_page: int = 100) -> ParsedDocument:
    pages = []
    for p in range(0, n_words, words_per_page):
        words = [f"w{i}" for i in range(p, min(p + words_per_page, n_words))]
        pages.append(Page(number=len(pages) + 1, text=" ".join(words)))
    return ParsedDocument(doc_id="d", source_file="d.pdf", pages=pages)


def test_covers_all_words_in_order():
    chunks = chunk_document(_doc(1000), words_per_chunk=250, overlap_words=50)
    # every word appears; first/last words are at the extremes
    assert chunks[0].text.startswith("w0 ")
    assert chunks[-1].text.endswith("w999")
    seen = {w for c in chunks for w in c.text.split()}
    assert len(seen) == 1000


def test_overlap_is_exact():
    chunks = chunk_document(_doc(600), words_per_chunk=200, overlap_words=40)
    for a, b in zip(chunks, chunks[1:]):
        assert a.text.split()[-40:] == b.text.split()[:40]


def test_ids_deterministic_and_unique():
    c1 = chunk_document(_doc(500))
    c2 = chunk_document(_doc(500))
    assert [c.chunk_id for c in c1] == [c.chunk_id for c in c2]
    assert len({c.chunk_id for c in c1}) == len(c1)
    assert c1[0].chunk_id == "d:0000"


def test_page_spans_monotonic():
    chunks = chunk_document(_doc(1000), words_per_chunk=250, overlap_words=50)
    for c in chunks:
        assert 1 <= c.page_start <= c.page_end
    assert [c.page_start for c in chunks] == sorted(c.page_start for c in chunks)


def test_short_doc_single_chunk():
    chunks = chunk_document(_doc(30))
    assert len(chunks) == 1
    assert chunks[0].n_words == 30


def test_invalid_window_rejected():
    with pytest.raises(ChunkError):
        chunk_document(_doc(100), words_per_chunk=100, overlap_words=100)
    with pytest.raises(ChunkError):
        chunk_document(_doc(100), words_per_chunk=0)


def test_empty_doc_rejected():
    doc = ParsedDocument(doc_id="e", source_file="e.pdf", pages=[Page(number=1, text="")])
    with pytest.raises(ChunkError, match="no words"):
        chunk_document(doc)


def test_real_sample_end_to_end():
    doc = parse_pdf(SAMPLE, doc_id="uu-hpp-2021-bt")
    chunks = chunk_document(doc)
    assert all(isinstance(c, Chunk) and c.n_words <= 250 for c in chunks)
    # the anchor eval fact must land inside at least one chunk
    assert any("22% (dua puluh dua" in c.text for c in chunks)
