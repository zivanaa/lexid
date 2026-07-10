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
# address after "beralamat di" up to end of line / semicolon (addresses contain
# their own periods, so we can't stop at the first ".")
_ADDRESS = re.compile(r"(beralamat di\s+)([^;\n]+)", re.IGNORECASE)


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


def redact_names(text: str, names: list[str], counts: dict[str, int]) -> str:
    """Replace each distinct person name with a stable role token [NAMA_i].

    `names` comes from an off-the-shelf NER (persons only; institutions omitted so
    they survive). Longest names first so a full name is replaced before a partial.
    """
    seen: dict[str, str] = {}
    for name in sorted(set(names), key=len, reverse=True):
        if not name.strip():
            continue
        token = seen.setdefault(name, f"[NAMA_{len(seen) + 1}]")
        # IGNORECASE: the NER is uncased and court headers ALL-CAPS defendant
        # names, so match case-insensitively or those variants leak.
        redacted, n = re.subn(re.escape(name), token, text, flags=re.IGNORECASE)
        if n:
            text = redacted
            counts[token] = counts.get(token, 0) + n
    return text


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


def detect_person_names(text: str) -> list[str]:
    """Distinct PERSON names in the text, via the off-the-shelf NER. ORG/GPE etc.
    are intentionally NOT returned, so institutions survive anonymization.

    Uses char offsets (start/end) to recover the ORIGINAL-CASE surface form: the
    model is uncased and returns a lowercased 'word', which would not match the
    mixed-case source text at redaction time.
    """
    names = []
    for e in _ner()(text):
        if e.get("entity_group") != "PER":
            continue
        name = text[e["start"] : e["end"]] if "start" in e else e.get("word", "")
        name = name.strip()
        if name:
            names.append(name)
    return list(dict.fromkeys(names))  # dedupe, keep order


def anonymize_auto(text: str) -> AnonymizationResult:
    """Full gate: detect person names via NER, then scrub names + structured PII.
    Still imperfect by design — manual review remains the backstop."""
    return anonymize(text, names=detect_person_names(text))
