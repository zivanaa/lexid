"""finetuning.dataset.anonymize tests — SYNTHETIC PII only, never real data."""

import finetuning.dataset.anonymize as anon
from finetuning.dataset.anonymize import (
    anonymize,
    anonymize_auto,
    detect_person_names,
    redact_names,
)


def test_scrubs_nik():
    out = anonymize("Terdakwa dengan NIK 3327012345678901 hadir.")
    assert "3327012345678901" not in out.text
    assert "[NIK]" in out.text and out.redactions["[NIK]"] == 1


def test_scrubs_phone_variants():
    for phone in ["0812-3456-7890", "+62 812 3456 7890", "081234567890"]:
        out = anonymize(f"dapat dihubungi di {phone} untuk konfirmasi")
        assert phone.replace(" ", "") not in out.text.replace(" ", ""), phone
        assert "[TELEPON]" in out.text


def test_scrubs_plate():
    out = anonymize("mobil dengan nomor polisi B 1234 XYZ disita")
    assert "B 1234 XYZ" not in out.text and "[PLAT]" in out.text


def test_scrubs_address_after_beralamat_di():
    out = anonymize("Penggugat beralamat di Jl. Merdeka No. 5, Kota Jakarta; kemudian ...")
    assert "Jl. Merdeka No. 5, Kota Jakarta" not in out.text
    assert "beralamat di [ALAMAT]" in out.text
    assert "kemudian" in out.text  # only the address, not the rest, is redacted


def test_scrubs_multiline_tempat_tinggal_address():
    # real putusan label the identitas address "Tempat tinggal:", spanning lines
    text = (
        "Tempat tinggal\n: Jalan Daan Mogot No. 20 K, RT 10\nRW 03, Jakarta Barat;\nAgama : Kristen"
    )
    out = anonymize(text)
    assert "Jalan Daan Mogot" not in out.text and "Jakarta Barat" not in out.text
    assert "[ALAMAT]" in out.text
    assert "Agama" in out.text  # field after the ; survives


def test_name_not_redacted_inside_longer_word():
    # regression: "Agus" (a name) must not be redacted inside "Agustus" (August)
    out = redact_names("lahir 15 Agustus 1973, terdakwa Agus hadir", ["Agus"], {})
    assert "Agustus" in out  # the month is intact
    assert out.count("[NAMA_1]") == 1  # only the standalone name


def test_names_become_stable_role_tokens():
    text = "Budi Santoso bertemu Budi Santoso lalu Siti Aminah datang."
    out = anonymize(text, names=["Budi Santoso", "Siti Aminah"])
    assert "Budi Santoso" not in out.text and "Siti Aminah" not in out.text
    assert out.text.count("[NAMA_1]") == 2  # same person → same token, twice
    assert "[NAMA_2]" in out.text


def test_longest_name_first_avoids_partial_leak():
    # replacing "Budi" first would leave "[NAMA] Santoso" leaking the surname
    out = redact_names("Budi Santoso hadir.", ["Budi", "Budi Santoso"], {})
    assert "Santoso" not in out


def test_redact_names_drops_junk_and_never_corrupts_tokens():
    # 'A'/'x'/'di' are junk (too short / not name-like) → filtered; single-pass
    # replacement must not eat characters inside an inserted [NAMA_x] token
    out = redact_names("Budi Santoso dan Budi Santoso", ["Budi Santoso", "A", "x", "di"], {})
    assert out == "[NAMA_1] dan [NAMA_1]"  # clean, no nesting, junk ignored


def test_institutional_names_kept():
    # institutions are simply not in the person-name list → they survive
    out = anonymize("Pengadilan Negeri Jakarta Pusat memutus perkara.", names=["Budi"])
    assert "Pengadilan Negeri Jakarta Pusat" in out.text


def test_report_counts_and_clean_text_untouched():
    clean = "Perkara Nomor 123/Pid.B/2024/PN.Jkt diputus dengan denda Rp1.000.000.000,00."
    out = anonymize(clean)
    # case number and rupiah amount are NOT PII → must survive untouched
    assert out.text == clean
    assert out.redactions == {}


# --- layer 2: NER name detection (pipeline stubbed; no model download) ---


def _uncased_ner(text, mentions):
    """Mimic the real (uncased) pipeline: lowercased 'word' + char offsets."""
    ents = []
    for sub, group in mentions:
        i = text.find(sub)
        ents.append({"entity_group": group, "word": sub.lower(), "start": i, "end": i + len(sub)})

    class _Pipe:
        def __call__(self, _t):
            return ents

    return lambda: _Pipe()


def test_detect_person_names_recovers_original_case_and_drops_org(monkeypatch):
    text = "Budi Santoso menghadap Pengadilan Negeri, lalu Siti Aminah datang."
    monkeypatch.setattr(
        anon,
        "_ner",
        _uncased_ner(
            text, [("Budi Santoso", "PER"), ("Pengadilan Negeri", "ORG"), ("Siti Aminah", "PER")]
        ),
    )
    # original case recovered via offsets (not the lowercased word); ORG dropped
    assert detect_person_names(text) == ["Budi Santoso", "Siti Aminah"]


def test_redact_names_case_insensitive_catches_allcaps_header():
    # court headers ALL-CAPS the defendant; case-sensitive match would leak it
    out = redact_names("Terdakwa BUDI SANTOSO diputus", ["Budi Santoso"], {})
    assert "BUDI SANTOSO" not in out and "[NAMA_1]" in out


def _content_ner():
    """Position-aware stub: returns PER spans for any known name found IN the
    chunk it's given, so window-chunking behavior is actually exercised."""
    import re as _re

    known = ("Budi Santoso", "Siti Aminah")

    class _Pipe:
        def __call__(self, chunk):
            out = []
            for name in known:
                for m in _re.finditer(_re.escape(name), chunk, _re.I):
                    out.append(
                        {
                            "entity_group": "PER",
                            "word": m.group().lower(),
                            "start": m.start(),
                            "end": m.end(),
                        }
                    )
            return out

    return lambda: _Pipe()


def test_detect_names_chunks_long_text(monkeypatch):
    # a name that only appears PAST the first window must still be found
    monkeypatch.setattr(anon, "_ner", _content_ner())
    text = "awal " + "x" * 2000 + " Siti Aminah menutup sidang."
    assert detect_person_names(text, window=1500, overlap=200) == ["Siti Aminah"]


def test_detect_filters_low_score_and_fragments(monkeypatch):
    text = "Budi Santoso xx"

    class _Pipe:
        def __call__(self, chunk):
            return [
                {
                    "entity_group": "PER",
                    "word": "budi santoso",
                    "start": 0,
                    "end": 12,
                    "score": 0.99,
                },
                {
                    "entity_group": "PER",
                    "word": "x",
                    "start": 13,
                    "end": 14,
                    "score": 0.99,
                },  # fragment
                {
                    "entity_group": "PER",
                    "word": "budi",
                    "start": 0,
                    "end": 4,
                    "score": 0.3,
                },  # low score
            ]

    monkeypatch.setattr(anon, "_ner", lambda: _Pipe())
    assert detect_person_names(text) == ["Budi Santoso"]  # junk + low-score dropped


def test_anonymize_auto_scrubs_uncased_names_and_pii(monkeypatch):
    text = "Terdakwa Budi Santoso, NIK 3327012345678901, hadir di persidangan."
    monkeypatch.setattr(anon, "_ner", _uncased_ner(text, [("Budi Santoso", "PER")]))
    out = anonymize_auto(text)
    assert "Budi Santoso" not in out.text and "3327012345678901" not in out.text
    assert "[NAMA_1]" in out.text and "[NIK]" in out.text
