"""ingestion.parse tests — run on the committed 4-page sample, no network."""

from pathlib import Path

import pymupdf
import pytest

from ingestion.parse import ParseError, parse_pdf

SAMPLE = Path(__file__).parent.parent / "data" / "samples" / "uu-7-2021-hpp-excerpt.pdf"


def test_parses_sample_excerpt():
    doc = parse_pdf(SAMPLE, doc_id="uu-hpp-2021-bt")
    assert doc.doc_id == "uu-hpp-2021-bt"
    assert len(doc.pages) == 4
    assert doc.pages[0].number == 1
    # anchor eval fact must survive parsing verbatim
    assert "22% (dua puluh dua" in doc.full_text


def test_boilerplate_stripped():
    doc = parse_pdf(SAMPLE, doc_id="x")
    assert "www.peraturan.go.id" not in doc.full_text
    for line in doc.full_text.splitlines():
        assert not line.strip().startswith("2021, No.")


def test_missing_file_raises():
    with pytest.raises(ParseError, match="not found"):
        parse_pdf("data/raw/nope.pdf", doc_id="x")


def test_scanned_pdf_rejected(tmp_path):
    # a text-free PDF must be refused, not silently indexed as empty chunks
    p = tmp_path / "scan.pdf"
    pdf = pymupdf.open()
    pdf.new_page()
    pdf.save(p)
    with pytest.raises(ParseError, match="text layer"):
        parse_pdf(p, doc_id="x")
