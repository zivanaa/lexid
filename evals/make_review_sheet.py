"""Generate a human-review sheet (markdown) for a retrieval eval dataset.

    uv run python -m evals.make_review_sheet

Puts each draft item next to the FULL text of the chunks it references, so the
reviewer can verify question/chunks/answer without opening the source PDFs.
Output lands beside the dataset as <dataset-stem>.review.md. Review verdicts
still go into the dataset JSON (reviewed_by_human) — the sheet is read-only.
"""

import argparse
import json
import sys
from pathlib import Path

from evals.run_retrieval import DATASET_DEFAULT

_CHECKLIST = (
    "- [ ] pertanyaan wajar & tidak ambigu\n"
    "- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya\n"
    "- [ ] jawaban referensi akurat (angka, pasal, ayat)\n"
)


def build_chunk_map() -> dict[str, tuple[str, str]]:
    """chunk_id -> (pages, text), rebuilt deterministically from the corpus."""
    import ingestion.run as ingestion_run
    from ingestion.chunk import chunk_document
    from ingestion.parse import parse_pdf

    manifest = json.loads((ingestion_run.RAW_DIR / "MANIFEST.json").read_text(encoding="utf-8"))
    out: dict[str, tuple[str, str]] = {}
    for entry in manifest["documents"]:
        doc = parse_pdf(ingestion_run.RAW_DIR / entry["file"], doc_id=entry["id"])
        for c in chunk_document(doc):
            out[c.chunk_id] = (f"{c.page_start}-{c.page_end}", c.text)
    return out


def render_sheet(data: dict, chunk_map: dict[str, tuple[str, str]]) -> str:
    lines = [
        f"# Lembar Review — {data['name']} v{data['version']}",
        "",
        "Untuk TIAP item: baca pertanyaan, baca teks chunk di bawahnya, lalu putuskan.",
        "Kalau lolos → set `reviewed_by_human: true` di JSON dataset.",
        "Kalau salah → perbaiki itemnya dulu + tambah baris changelog, baru set true.",
        "Item unanswerable: pastikan jawabannya MEMANG tidak ada di korpus.",
        "",
    ]
    for it in data["items"]:
        status = "✅ reviewed" if it["reviewed_by_human"] else "⬜ BELUM"
        lines += [
            "---",
            f"## {it['id']} · {it['difficulty']} · {status}",
            f"**Pertanyaan:** {it['question']}",
            "",
            f"**Jawaban referensi:** {it['reference_answer']}",
            "",
        ]
        if not it["relevant_chunk_groups"]:
            lines += [
                "_(unanswerable — tidak ada chunk; cek bahwa korpus memang tak menjawab)_",
                "",
            ]
        for gi, group in enumerate(it["relevant_chunk_groups"], start=1):
            alt = " **ATAU** ".join(f"`{c}`" for c in group)
            lines += [f"**Fakta {gi}:** cukup salah satu dari {alt}", ""]
            for cid in group:
                pages, text = chunk_map.get(
                    cid, ("?", "⚠️ CHUNK_ID TIDAK DITEMUKAN — chunking berubah?")
                )
                lines += [
                    "<details>",
                    f"<summary>{cid} (hlm. {pages})</summary>",
                    "",
                    text,
                    "",
                    "</details>",
                    "",
                ]
        lines += [_CHECKLIST]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Buat lembar review markdown utk dataset eval")
    ap.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    args = ap.parse_args(argv)

    data = json.loads(args.dataset.read_text(encoding="utf-8"))
    sheet = render_sheet(data, build_chunk_map())
    out = args.dataset.parent / f"{args.dataset.stem}.review.md"
    out.write_text(sheet, encoding="utf-8")
    n = len(data["items"])
    done = sum(1 for i in data["items"] if i["reviewed_by_human"])
    print(f"{out} — {n} item ({done} sudah direview, {n - done} belum)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
