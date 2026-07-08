"""evals.make_review_sheet tests — pure rendering, no PDFs."""

from evals.make_review_sheet import render_sheet

DATA = {
    "name": "t",
    "version": "0.1",
    "items": [
        {
            "id": "d01",
            "question": "Berapa tarif?",
            "difficulty": "direct",
            "relevant_chunk_groups": [["doc:0001", "doc:0002"]],
            "reference_answer": "22%",
            "reviewed_by_human": False,
        },
        {
            "id": "u01",
            "question": "Hal di luar korpus?",
            "difficulty": "unanswerable",
            "relevant_chunk_groups": [],
            "reference_answer": "Tidak ditemukan.",
            "reviewed_by_human": True,
        },
    ],
}

CHUNKS = {"doc:0001": ("1-2", "teks chunk satu"), "doc:0002": ("2-3", "teks chunk dua")}


def test_renders_items_with_chunk_text():
    md = render_sheet(DATA, CHUNKS)
    assert "d01 · direct · ⬜ BELUM" in md
    assert "u01 · unanswerable · ✅ reviewed" in md
    assert "teks chunk satu" in md and "teks chunk dua" in md
    assert "`doc:0001` **ATAU** `doc:0002`" in md
    assert "unanswerable — tidak ada chunk" in md


def test_missing_chunk_id_flagged():
    md = render_sheet(DATA, {})
    assert "CHUNK_ID TIDAK DITEMUKAN" in md
