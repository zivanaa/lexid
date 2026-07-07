"""Full ingestion: MANIFEST.json → parse → chunk → embed → Qdrant.

Run: uv run python -m ingestion.run
First run downloads BGE-M3 (~2GB) to the HF cache and embeds on CPU —
minutes, not seconds; fine for a corpus this size.
"""

import json
import sys
import time
from pathlib import Path

from ingestion.chunk import chunk_document
from ingestion.embed import embed_texts
from ingestion.index import COLLECTION, build_index, get_client
from ingestion.parse import parse_pdf

RAW_DIR = Path("data/raw")


def ingest(raw_dir: Path = RAW_DIR) -> dict:
    manifest = json.loads((raw_dir / "MANIFEST.json").read_text(encoding="utf-8"))
    stats: dict = {"documents": {}, "total_chunks": 0}

    all_chunks = []
    for entry in manifest["documents"]:
        pdf_path = raw_dir / entry["file"]
        if not pdf_path.exists():
            raise FileNotFoundError(
                f"{pdf_path} missing — re-download it (see MANIFEST download_url)"
            )
        doc = parse_pdf(pdf_path, doc_id=entry["id"])
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
        stats["documents"][entry["id"]] = {"pages": len(doc.pages), "chunks": len(chunks)}

    t0 = time.perf_counter()
    vectors = embed_texts([c.text for c in all_chunks])
    stats["embed_seconds"] = round(time.perf_counter() - t0, 1)

    client = get_client()
    # recreate=True: chunk_ids shift whenever chunking config changes, so
    # stale points from a previous config must never linger in the collection
    stats["total_chunks"] = build_index(client, all_chunks, vectors, recreate=True)
    stats["collection"] = COLLECTION
    stats["vector_dim"] = int(vectors.shape[1])
    return stats


def main() -> int:
    stats = ingest()
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
