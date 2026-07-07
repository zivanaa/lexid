"""PDF → page-level text units.

Naive by design: the Phase 1 baseline chunker consumes plain page text.
Structure-aware pasal/ayat parsing is a separate experiment in the
docs/evals.md matrix and must NOT live here until the baseline is measured.
"""

import re
from pathlib import Path

import pymupdf
from pydantic import BaseModel

# Boilerplate on every Lembaran Negara page (site watermark, LN header,
# "-63-"-style page markers) would otherwise pollute chunks and embeddings.
_BOILERPLATE_LINE = re.compile(r"^\s*(www\.peraturan\.go\.id|\d{4},\s*No\.\s*\d+|-\s*\d+\s*-)\s*$")

# A real text layer yields far more than this per page on average; below it
# we're likely holding a pure scan and downstream results would be garbage.
_MIN_CHARS_PER_PAGE = 200


class ParseError(Exception):
    """Raised when a source PDF cannot yield usable text."""


class Page(BaseModel):
    number: int  # 1-based physical page number, kept for citations/debugging
    text: str


class ParsedDocument(BaseModel):
    doc_id: str
    source_file: str
    pages: list[Page]

    @property
    def full_text(self) -> str:
        return "\n".join(p.text for p in self.pages)


def _clean_page(raw: str) -> str:
    lines = [ln.rstrip() for ln in raw.splitlines()]
    kept = [ln for ln in lines if ln and not _BOILERPLATE_LINE.match(ln)]
    return "\n".join(kept)


def parse_pdf(path: str | Path, doc_id: str) -> ParsedDocument:
    """Extract cleaned per-page text. Raises ParseError on missing/scanned PDFs."""
    path = Path(path)
    if not path.exists():
        raise ParseError(f"file not found: {path}")
    try:
        pdf = pymupdf.open(path)
    except Exception as e:  # pymupdf raises various internal types
        raise ParseError(f"cannot open {path.name}: {e}") from e

    pages = [Page(number=i + 1, text=_clean_page(page.get_text())) for i, page in enumerate(pdf)]
    if not pages:
        raise ParseError(f"{path.name}: PDF has no pages")

    total_chars = sum(len(p.text) for p in pages)
    if total_chars < _MIN_CHARS_PER_PAGE * len(pages):
        raise ParseError(
            f"{path.name}: only {total_chars} chars across {len(pages)} pages — "
            "likely no text layer (scan); OCR is out of scope for Phase 1"
        )

    return ParsedDocument(doc_id=doc_id, source_file=path.name, pages=pages)
