"""Anonymization gate for Indonesian court decisions (Phase 2 blocking gate).

UU PDP (UU 27/2022) applies to the personal data in putusan (names, NIK, phones,
plate numbers, addresses). This module MUST run before any labeling, training,
publishing, or committing of decision text (docs/data-privacy.md).

Two layers:
  1. STRUCTURED PII — regex-scrubbed here: NIK, phone, plate, `beralamat di ...`
     addresses. Deterministic, testable, no model.
  2. PERSON NAMES — `detect_person_names` runs an off-the-shelf Indonesian NER
     (config.ner_model = cahya/bert-base-indonesian-NER; BIO scheme with B-PER/
     I-PER, verified) and keeps only PER entities, so ORG/GPE (courts, agencies)
     survive. Names become stable role tokens [NAMA_1], ... NOT a new pip dep —
     reuses the transformers stack from `uv sync --extra embed`, CPU-only.

Regexes are deliberately conservative and IMPERFECT by design — the real
backstop is manual review (docs/data-privacy.md step 3). Everything here is
developed/tested on SYNTHETIC data only; never on real decision text.
"""

import re
from functools import lru_cache

from pydantic import BaseModel

from config import settings


class AnonymizeError(Exception):
    """Raised when the NER model cannot be loaded or used."""


# --- structured-PII patterns → placeholder tokens ---
# order matters: NIK (16 digits) before phone so a bare 16-digit run isn't
# partially eaten by the phone rule.
_PII_RULES: list[tuple[str, re.Pattern]] = [
    ("[NIK]", re.compile(r"(?<!\d)\d{16}(?!\d)")),
    # Indonesian mobile/landline: +62/62/0 prefix, optional separators
    ("[TELEPON]", re.compile(r"(?<![\w+])(?:\+?62|0)[\s.-]?8[1-9][\d\s.-]{6,12}\d(?!\d)")),
    # vehicle plate: 1-2 letters · 1-4 digits · 1-3 letters (e.g. "B 1234 XYZ")
    ("[PLAT]", re.compile(r"\b[A-Z]{1,2}\s?\d{1,4}\s?[A-Z]{1,3}\b")),
]
# address after a label up to the next ";" (identitas fields are ;-terminated;
# addresses span multiple lines and contain their own periods). Real putusan use
# "Tempat tinggal:" far more than "beralamat di" — validated on a real decision.
# Capped at 300 chars so a mislabelled match can't run away.
_ADDRESS = re.compile(
    r"((?:beralamat di|bertempat tinggal di|tempat tinggal)\s*:?\s*)([^;]{1,300})",
    re.IGNORECASE,
)


class AnonymizationResult(BaseModel):
    text: str
    redactions: dict[str, int]  # token -> count, e.g. {"[NIK]": 2, "[NAMA]": 5}


def _scrub_structured(text: str, counts: dict[str, int]) -> str:
    text = _ADDRESS.sub(
        lambda m: (
            counts.__setitem__("[ALAMAT]", counts.get("[ALAMAT]", 0) + 1),
            m.group(1) + "[ALAMAT]",
        )[1],
        text,
    )
    for token, pat in _PII_RULES:

        def _repl(_m, _t=token):
            counts[_t] = counts.get(_t, 0) + 1
            return _t

        text = pat.sub(_repl, text)
    return text


# a real name: starts/ends with a letter; letters/space/.'- inside; >= 3 chars.
# Kills the NER's single-char / fragment garbage that otherwise gets replaced
# GLOBALLY (even inside inserted [NAMA_x] tokens) and corrupts the whole document.
_NAME_LIKE = re.compile(r"[^\W\d_][\w.'\- ]*[^\W\d_]", re.UNICODE)


def _looks_like_name(s: str) -> bool:
    s = s.strip()
    return len(s) >= 3 and _NAME_LIKE.fullmatch(s) is not None


def redact_names(text: str, names: list[str], counts: dict[str, int]) -> str:
    """Replace each distinct person name with a stable role token [NAMA_i].

    ONE combined-regex pass (not a loop of global replaces): re.sub never
    re-scans the text it already inserted, so tokens can't be corrupted or
    explode recursively. Longest name first (alternation order) so a full name
    wins over a partial; IGNORECASE because the NER is uncased and headers
    ALL-CAPS names. Junk spans (single chars/fragments) are filtered out.
    """
    clean = [n.strip() for n in names if _looks_like_name(n)]
    if not clean:
        return text
    token_of: dict[str, str] = {}
    for n in clean:  # stable token per distinct (case-folded) name, first-seen order
        token_of.setdefault(n.lower(), f"[NAMA_{len(token_of) + 1}]")
    ordered = sorted(set(clean), key=len, reverse=True)
    # \b so a name never matches INSIDE a longer word (real bug: "Agus" was
    # redacted inside "Agustus" → "[NAMA]tus"). Names start/end with letters.
    pattern = re.compile(r"\b(?:" + "|".join(re.escape(n) for n in ordered) + r")\b", re.IGNORECASE)

    def _repl(m: re.Match) -> str:
        token = token_of[m.group().lower()]
        counts[token] = counts.get(token, 0) + 1
        return token

    return pattern.sub(_repl, text)


def anonymize(text: str, names: list[str] | None = None) -> AnonymizationResult:
    """Apply structured-PII scrubbing, then (if names given) name→role redaction."""
    counts: dict[str, int] = {}
    text = _scrub_structured(text, counts)
    if names:
        text = redact_names(text, names, counts)
    return AnonymizationResult(text=text, redactions=counts)


# --- layer 2: person-name NER (off-the-shelf, local CPU) ---


@lru_cache(maxsize=1)
def _ner():
    # Lazy: importing transformers pulls torch; must not happen for the regex
    # layer or plain test runs.
    try:
        from transformers import pipeline
    except ImportError as e:
        raise AnonymizeError("transformers not installed — run: uv sync --extra embed") from e
    try:
        return pipeline(
            "token-classification",
            model=settings.ner_model,
            aggregation_strategy="simple",  # merge B-PER/I-PER into whole-name spans
            device=-1,  # CPU ($0, no GPU)
        )
    except Exception as e:
        raise AnonymizeError(f"cannot load NER model '{settings.ner_model}': {e}") from e


def detect_person_names(
    text: str, window: int = 1500, overlap: int = 200, min_score: float = 0.9
) -> list[str]:
    """Distinct PERSON names in the text, via the off-the-shelf NER. ORG/GPE etc.
    are intentionally NOT returned, so institutions survive anonymization.

    Court decisions run tens of thousands of tokens but BERT caps at 512, so the
    text is chunked into overlapping char windows (~1500 chars < 512 tokens);
    the overlap keeps a name split at a boundary recoverable. We only need the
    name STRINGS — redact_names then scrubs every occurrence globally — so
    per-window offsets (which recover ORIGINAL case; the model is uncased) are
    enough. Names are deduped across windows.
    """
    ner = _ner()
    names: list[str] = []
    step = max(1, window - overlap)
    for start in range(0, len(text), step):
        chunk = text[start : start + window]
        for e in ner(chunk):
            if e.get("entity_group") != "PER" or e.get("score", 1.0) < min_score:
                continue
            name = (chunk[e["start"] : e["end"]] if "start" in e else e.get("word", "")).strip()
            if _looks_like_name(name):  # drop the NER's single-char / fragment noise
                names.append(name)
    return list(dict.fromkeys(names))  # dedupe, keep order


def anonymize_auto(text: str) -> AnonymizationResult:
    """Full gate: detect person names via NER, then scrub names + structured PII.
    Still imperfect by design — manual review remains the backstop."""
    return anonymize(text, names=detect_person_names(text))
