"""Load versioned prompts from *.md files (YAML frontmatter: id, version)."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load(prompt_id: str, directory: Path | None = None) -> tuple[str, int]:
    """Return (prompt_text, version) for the given id. Raises if not found.

    directory defaults to prompts/; judge prompts live in evals/judge_prompts/.
    """
    search_dir = directory or PROMPTS_DIR
    for f in search_dir.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        head, _, body = text[3:].partition("---")
        meta = dict(line.split(":", 1) for line in head.strip().splitlines() if ":" in line)
        if meta.get("id", "").strip() == prompt_id:
            return body.strip(), int(meta.get("version", "1").strip())
    raise KeyError(f"prompt id '{prompt_id}' not found in {search_dir}")
