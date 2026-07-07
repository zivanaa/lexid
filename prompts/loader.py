"""Load versioned prompts from prompts/*.md (YAML frontmatter: id, version)."""
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load(prompt_id: str) -> tuple[str, int]:
    """Return (prompt_text, version) for the given id. Raises if not found."""
    for f in PROMPTS_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        head, _, body = text[3:].partition("---")
        meta = dict(
            line.split(":", 1) for line in head.strip().splitlines() if ":" in line
        )
        if meta.get("id", "").strip() == prompt_id:
            return body.strip(), int(meta.get("version", "1").strip())
    raise KeyError(f"prompt id '{prompt_id}' not found in {PROMPTS_DIR}")
