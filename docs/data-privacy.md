# Data Privacy & Anonymization (blocking gate for Phase 2)

Why: Indonesian court decisions contain personal data (names, addresses, NIK,
plate numbers). UU PDP (UU 27/2022) applies to processing personal data;
publishing a model or dataset derived from it without anonymization is the one
real legal/ethical risk in this project. Treat this doc as a blocking gate.

Pipeline (finetuning/dataset/anonymize.py) — runs BEFORE any labeling:
1. Regex pass for structured PII: NIK (16 digits), phone numbers, plate
   patterns, addresses following "beralamat di" patterns.
2. Off-the-shelf multilingual NER (free, local) to detect person names →
   replace with role tokens (TERDAKWA_1, SAKSI_2, PENGGUGAT_1). Institutional
   names (courts, agencies, companies acting as institutions) are kept.
   NOTE the chicken-and-egg: we use a generic NER to anonymize BEFORE training
   our own — imperfect by design, hence step 3.
3. Manual review: 100% of items entering the test split; ≥20% random sample of
   train; ANY leak found → widen review sample.
4. Record: anonymization version + review coverage in the dataset card.

Publishing checklist (all required before the model/dataset goes on HF Hub):
[ ] anonymization run + review coverage documented
[ ] spot-audit of 30 random training items finds zero direct identifiers
[ ] model card states data source, anonymization method, and limitations
[ ] decision recorded: public vs gated access (default: gated until confident)

Also: scrape politely (rate limit, honest User-Agent), record source URLs +
dates in data/raw/MANIFEST.json, and never commit non-anonymized decision text.

## Validated on 1 real decision (2026-07-10)

Ran `anonymize_auto` on a real PK/PID.SUS putusan (145K chars). This is exactly
why real-data validation matters — it surfaced 4 bugs synthetic tests missed,
now fixed + regression-tested: (1) the uncased NER returns lowercased names that
didn't match mixed-case source (fix: offsets + IGNORECASE); (2) BERT's 512-token
cap crashed on the long doc (fix: overlapping char-window chunking); (3) junk
NER spans (single chars) were replaced globally and corrupted the whole document
(fix: score≥0.9 + name-like filter + single combined-regex pass); (4) a name was
redacted INSIDE a longer word ("Agus" inside "Agustus") and addresses were missed
because they use "Tempat tinggal:" not "beralamat di" (fix: \b word boundaries +
broader address labels).

CONFIRMED working: defendant name, the identitas address, and a phone were
redacted; case numbers, rupiah amounts, courts/agencies, and legal terms were
correctly preserved. KNOWN residual gaps for the manual reviewer to watch:
birthplace / DOB / age are not yet scrubbed (out of the current regex scope);
a second, label-less alternative address can slip through; deep witness names
depend on NER recall. This confirms the design: the regex+NER gate is a FIRST
PASS — manual review (steps above) remains mandatory, not optional.
