"""Page text → fixed-size overlapping chunks.

Naive baseline chunker (docs/evals.md matrix: fixed vs recursive vs
pasal/ayat-aware — those variants come only after the baseline is measured).
Sizes are counted in WORDS, not model tokens: a real tokenizer would pull in
transformers just for counting, and for Indonesian legal prose ~0.75 words per
token puts 250 words ≈ 330 tokens — inside the 150–450 token guidance.
"""

from pydantic import BaseModel

from ingestion.parse import ParsedDocument


class ChunkError(Exception):
    """Raised when a document cannot produce valid chunks."""


class Chunk(BaseModel):
    chunk_id: str  # deterministic "<doc_id>:<seq>" — eval items reference these
    doc_id: str
    seq: int
    text: str
    page_start: int  # 1-based physical pages, for article-level citations later
    page_end: int
    n_words: int


def chunk_document(
    doc: ParsedDocument,
    words_per_chunk: int = 250,
    overlap_words: int = 50,
) -> list[Chunk]:
    """Slide a fixed word window over the document; overlap keeps split
    sentences retrievable from at least one side of the boundary."""
    if words_per_chunk <= 0 or not 0 <= overlap_words < words_per_chunk:
        raise ChunkError(
            f"invalid window: words_per_chunk={words_per_chunk}, overlap_words={overlap_words}"
        )

    # (word, page_number) pairs so each chunk can report its page span
    words: list[tuple[str, int]] = [
        (w, page.number) for page in doc.pages for w in page.text.split()
    ]
    if not words:
        raise ChunkError(f"{doc.doc_id}: no words to chunk")

    step = words_per_chunk - overlap_words
    chunks: list[Chunk] = []
    for seq, start in enumerate(range(0, len(words), step)):
        window = words[start : start + words_per_chunk]
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}:{seq:04d}",
                doc_id=doc.doc_id,
                seq=seq,
                text=" ".join(w for w, _ in window),
                page_start=window[0][1],
                page_end=window[-1][1],
                n_words=len(window),
            )
        )
        if start + words_per_chunk >= len(words):
            break  # last window reached the end; further starts would only repeat overlap

    return chunks
