"""finetuning.dataset.anonymize tests — SYNTHETIC PII only, never real data."""

from finetuning.dataset.anonymize import anonymize, redact_names


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
