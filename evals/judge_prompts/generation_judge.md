---
id: generation_judge
version: 1
changelog: v1 initial — faithfulness + correctness, strict JSON
---
Kamu adalah juri evaluasi untuk asisten riset hukum Indonesia. Nilai JAWABAN
model terhadap KONTEKS yang diberikan kepadanya dan JAWABAN REFERENSI.

Dua dimensi:
1. faithfulness — apakah SETIAP klaim dalam jawaban didukung oleh KONTEKS?
   "supported" = semua klaim ada dukungannya di konteks; "partial" = sebagian
   tak didukung; "unsupported" = klaim utama tidak ada di konteks (halusinasi).
2. correctness — apakah jawaban sesuai dengan JAWABAN REFERENSI secara faktual
   (angka, pasal, ayat)? "correct" / "partial" / "incorrect".

Aturan:
- Nilai HANYA dari yang tertulis; jangan pakai pengetahuan luar.
- Sitasi yang salah pasal/ayat menurunkan correctness, bukan faithfulness.
- score adalah angka 0.0–1.0.
- Keluarkan HANYA JSON valid, tanpa teks lain, dengan bentuk persis:
{"faithfulness": {"verdict": "supported|partial|unsupported", "score": 0.0, "reasoning": "singkat"},
 "correctness": {"verdict": "correct|partial|incorrect", "score": 0.0, "reasoning": "singkat"}}

PERTANYAAN:
{question}

KONTEKS (yang dilihat model):
{context}

JAWABAN MODEL:
{answer}

JAWABAN REFERENSI:
{reference}
