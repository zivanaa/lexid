"""Anonymization gate for Indonesian court decisions (Phase 2 blocking gate).

UU PDP (UU 27/2022) applies to the personal data in putusan (names, NIK, phones,
plate numbers, addresses). This module MUST run before any labeling, training,
publishing, or committing of decision text (docs/data-privacy.md).

Two layers:
  1. STRUCTURED PII — regex-scrubbed here: NIK, phone, plate, `beralamat di ...`
     addresses. Deterministic, testable, no model.
  2. PERSON NAMES — replaced with role tokens ([NAMA_1], ...) from a list an
     off-the-shelf multilingual NER produces (chosen later; the NER is the one
     new dependency). `redact_names` is the seam; institutional names are kept
     by simply not being in the list.

Regexes are deliberately conservative and IMPERFECT by design — the real
backstop is manual review (docs/data-privacy.md step 3). Everything here is
developed/tested on SYNTHETIC data only; never on real decision text.
"""

import re

from pydantic import BaseModel

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
        redacted, n = re.subn(re.escape(name), token, text)
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
