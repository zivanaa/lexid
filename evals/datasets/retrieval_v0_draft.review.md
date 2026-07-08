# Lembar Review — lexid-retrieval-eval v0.2-draft

Untuk TIAP item: baca pertanyaan, baca teks chunk di bawahnya, lalu putuskan.
Kalau lolos → set `reviewed_by_human: true` di JSON dataset.
Kalau salah → perbaiki itemnya dulu + tambah baris changelog, baru set true.
Item unanswerable: pastikan jawabannya MEMANG tidak ada di korpus.

---
## d01 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tarif Pajak Penghasilan untuk Wajib Pajak badan dalam negeri dan bentuk usaha tetap?

**Jawaban referensi:** 22% (dua puluh dua persen), mulai berlaku pada tahun pajak 2022 [Pasal 17 ayat (1) huruf b UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0056` **ATAU** `uu-hpp-2021-bt:0057`

<details>
<summary>uu-hpp-2021-bt:0056 (hlm. 61-63)</summary>

kerugian dan jumlah yang diterima sebagai penggantian merupakan penghasilan pada tahun terjadinya pengalihan tersebut. (8) Apabila terjadi pengalihan harta yang memenuhi syarat sebagaimana dimaksud dalam Pasal 4 ayat (3) huruf a dan huruf b, yang berupa harta tak berwujud, maka jumlah nilai sisa buku harta tersebut tidak boleh dibebankan sebagai kerugian bagi pihak yang mengalihkan. 7. Ketentuan ayat (1), ayat (2), ayat (2b), dan ayat (3) Pasal 17 diubah, Pasal 17 ayat (2a) dihapus, di antara ayat (2d) dan ayat (3) Pasal 17 disisipkan 1 (satu) ayat, yakni ayat (2e), serta penjelasan ayat (5) dan ayat (6) Pasal 17 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 17 berbunyi sebagai berikut: Pasal 17 (1) Tarif pajak yang diterapkan atas Penghasilan Kena Pajak bagi: a. Wajib Pajak orang pribadi dalam negeri sebagai berikut: Lapisan Penghasilan Kena Pajak Tarif Pajak sampai dengan Rp60.000.000,00 (enam puluh juta rupiah) 5% (lima persen) di atas Rp60.000.000,00 (enam puluh juta rupiah) sampai dengan Rp250.000.000,00 (dua ratus lima puluh juta rupiah) 15% (lima belas persen) di atas Rp250.000.000,00 (dua ratus lima puluh juta rupiah) sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) 25% (dua puluh lima persen) di atas Rp500.000.000,00 (lima ratus juta rupiah) sampai dengan Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf

</details>

<details>
<summary>uu-hpp-2021-bt:0057 (hlm. 62-64)</summary>

Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Pemerintah setelah disampaikan oleh pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. (2a) Dihapus. (2b) Wajib Pajak badan dalam negeri: a. berbentuk perseroan terbuka; b. dengan jumlah keseluruhan saham yang disetor diperdagangkan pada bursa efek di Indonesia paling sedikit 40% (empat puluh persen); dan c. memenuhi persyaratan tertentu, dapat memperoleh tarif sebesar 3% (tiga persen) lebih rendah dari tarif sebagaimana dimaksud pada ayat (1) huruf b. (2c) Tarif yang dikenakan atas penghasilan berupa dividen yang dibagikan kepada Wajib Pajak orang pribadi dalam negeri adalah paling tinggi sebesar 10% (sepuluh persen) dan bersifat final. (2d) Ketentuan lebih lanjut mengenai besarnya tarif sebagaimana dimaksud pada ayat (2c) diatur dengan Peraturan Pemerintah. (2e) Ketentuan lebih lanjut mengenai persyaratan tertentu sebagaimana dimaksud pada ayat (2b) huruf c diatur dengan atau berdasarkan Peraturan Pemerintah. (3) Besarnya lapisan Penghasilan Kena Pajak sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Menteri Keuangan. (4) Untuk keperluan penerapan tarif pajak sebagaimana dimaksud pada ayat (1), jumlah Penghasilan Kena Pajak dibulatkan ke bawah dalam ribuan rupiah penuh. (5) Besarnya pajak yang terutang bagi Wajib Pajak orang pribadi dalam negeri yang terutang

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d02 · direct · ⬜ BELUM
**Pertanyaan:** Berapa pengurangan tarif PPh bagi Wajib Pajak badan berbentuk perseroan terbuka yang minimal 40% sahamnya diperdagangkan di bursa efek Indonesia?

**Jawaban referensi:** Tarif 3% (tiga persen) lebih rendah dari tarif umum 22%, dengan syarat tertentu [Pasal 17 ayat (2b) UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0057`

<details>
<summary>uu-hpp-2021-bt:0057 (hlm. 62-64)</summary>

Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Pemerintah setelah disampaikan oleh pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. (2a) Dihapus. (2b) Wajib Pajak badan dalam negeri: a. berbentuk perseroan terbuka; b. dengan jumlah keseluruhan saham yang disetor diperdagangkan pada bursa efek di Indonesia paling sedikit 40% (empat puluh persen); dan c. memenuhi persyaratan tertentu, dapat memperoleh tarif sebesar 3% (tiga persen) lebih rendah dari tarif sebagaimana dimaksud pada ayat (1) huruf b. (2c) Tarif yang dikenakan atas penghasilan berupa dividen yang dibagikan kepada Wajib Pajak orang pribadi dalam negeri adalah paling tinggi sebesar 10% (sepuluh persen) dan bersifat final. (2d) Ketentuan lebih lanjut mengenai besarnya tarif sebagaimana dimaksud pada ayat (2c) diatur dengan Peraturan Pemerintah. (2e) Ketentuan lebih lanjut mengenai persyaratan tertentu sebagaimana dimaksud pada ayat (2b) huruf c diatur dengan atau berdasarkan Peraturan Pemerintah. (3) Besarnya lapisan Penghasilan Kena Pajak sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Menteri Keuangan. (4) Untuk keperluan penerapan tarif pajak sebagaimana dimaksud pada ayat (1), jumlah Penghasilan Kena Pajak dibulatkan ke bawah dalam ribuan rupiah penuh. (5) Besarnya pajak yang terutang bagi Wajib Pajak orang pribadi dalam negeri yang terutang

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d03 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tarif PPh orang pribadi untuk lapisan penghasilan kena pajak sampai dengan Rp60.000.000?

**Jawaban referensi:** 5% (lima persen) [Pasal 17 ayat (1) huruf a UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0056`

<details>
<summary>uu-hpp-2021-bt:0056 (hlm. 61-63)</summary>

kerugian dan jumlah yang diterima sebagai penggantian merupakan penghasilan pada tahun terjadinya pengalihan tersebut. (8) Apabila terjadi pengalihan harta yang memenuhi syarat sebagaimana dimaksud dalam Pasal 4 ayat (3) huruf a dan huruf b, yang berupa harta tak berwujud, maka jumlah nilai sisa buku harta tersebut tidak boleh dibebankan sebagai kerugian bagi pihak yang mengalihkan. 7. Ketentuan ayat (1), ayat (2), ayat (2b), dan ayat (3) Pasal 17 diubah, Pasal 17 ayat (2a) dihapus, di antara ayat (2d) dan ayat (3) Pasal 17 disisipkan 1 (satu) ayat, yakni ayat (2e), serta penjelasan ayat (5) dan ayat (6) Pasal 17 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 17 berbunyi sebagai berikut: Pasal 17 (1) Tarif pajak yang diterapkan atas Penghasilan Kena Pajak bagi: a. Wajib Pajak orang pribadi dalam negeri sebagai berikut: Lapisan Penghasilan Kena Pajak Tarif Pajak sampai dengan Rp60.000.000,00 (enam puluh juta rupiah) 5% (lima persen) di atas Rp60.000.000,00 (enam puluh juta rupiah) sampai dengan Rp250.000.000,00 (dua ratus lima puluh juta rupiah) 15% (lima belas persen) di atas Rp250.000.000,00 (dua ratus lima puluh juta rupiah) sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) 25% (dua puluh lima persen) di atas Rp500.000.000,00 (lima ratus juta rupiah) sampai dengan Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d04 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tarif PPh orang pribadi untuk penghasilan kena pajak di atas Rp5 miliar?

**Jawaban referensi:** 35% (tiga puluh lima persen) [Pasal 17 ayat (1) huruf a UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0056` **ATAU** `uu-hpp-2021-bt:0057`

<details>
<summary>uu-hpp-2021-bt:0056 (hlm. 61-63)</summary>

kerugian dan jumlah yang diterima sebagai penggantian merupakan penghasilan pada tahun terjadinya pengalihan tersebut. (8) Apabila terjadi pengalihan harta yang memenuhi syarat sebagaimana dimaksud dalam Pasal 4 ayat (3) huruf a dan huruf b, yang berupa harta tak berwujud, maka jumlah nilai sisa buku harta tersebut tidak boleh dibebankan sebagai kerugian bagi pihak yang mengalihkan. 7. Ketentuan ayat (1), ayat (2), ayat (2b), dan ayat (3) Pasal 17 diubah, Pasal 17 ayat (2a) dihapus, di antara ayat (2d) dan ayat (3) Pasal 17 disisipkan 1 (satu) ayat, yakni ayat (2e), serta penjelasan ayat (5) dan ayat (6) Pasal 17 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 17 berbunyi sebagai berikut: Pasal 17 (1) Tarif pajak yang diterapkan atas Penghasilan Kena Pajak bagi: a. Wajib Pajak orang pribadi dalam negeri sebagai berikut: Lapisan Penghasilan Kena Pajak Tarif Pajak sampai dengan Rp60.000.000,00 (enam puluh juta rupiah) 5% (lima persen) di atas Rp60.000.000,00 (enam puluh juta rupiah) sampai dengan Rp250.000.000,00 (dua ratus lima puluh juta rupiah) 15% (lima belas persen) di atas Rp250.000.000,00 (dua ratus lima puluh juta rupiah) sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) 25% (dua puluh lima persen) di atas Rp500.000.000,00 (lima ratus juta rupiah) sampai dengan Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf

</details>

<details>
<summary>uu-hpp-2021-bt:0057 (hlm. 62-64)</summary>

Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Pemerintah setelah disampaikan oleh pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. (2a) Dihapus. (2b) Wajib Pajak badan dalam negeri: a. berbentuk perseroan terbuka; b. dengan jumlah keseluruhan saham yang disetor diperdagangkan pada bursa efek di Indonesia paling sedikit 40% (empat puluh persen); dan c. memenuhi persyaratan tertentu, dapat memperoleh tarif sebesar 3% (tiga persen) lebih rendah dari tarif sebagaimana dimaksud pada ayat (1) huruf b. (2c) Tarif yang dikenakan atas penghasilan berupa dividen yang dibagikan kepada Wajib Pajak orang pribadi dalam negeri adalah paling tinggi sebesar 10% (sepuluh persen) dan bersifat final. (2d) Ketentuan lebih lanjut mengenai besarnya tarif sebagaimana dimaksud pada ayat (2c) diatur dengan Peraturan Pemerintah. (2e) Ketentuan lebih lanjut mengenai persyaratan tertentu sebagaimana dimaksud pada ayat (2b) huruf c diatur dengan atau berdasarkan Peraturan Pemerintah. (3) Besarnya lapisan Penghasilan Kena Pajak sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Menteri Keuangan. (4) Untuk keperluan penerapan tarif pajak sebagaimana dimaksud pada ayat (1), jumlah Penghasilan Kena Pajak dibulatkan ke bawah dalam ribuan rupiah penuh. (5) Besarnya pajak yang terutang bagi Wajib Pajak orang pribadi dalam negeri yang terutang

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d05 · direct · ⬜ BELUM
**Pertanyaan:** Berapa besaran Penghasilan Tidak Kena Pajak per tahun untuk diri Wajib Pajak orang pribadi?

**Jawaban referensi:** Paling sedikit Rp54.000.000,00 (lima puluh empat juta rupiah) per tahun [Pasal 7 ayat (1) huruf a UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0048`

<details>
<summary>uu-hpp-2021-bt:0048 (hlm. 53-54)</summary>

ayat (1) didapat kerugian, kerugian tersebut dikompensasikan dengan penghasilan mulai tahun pajak berikutnya berturut-turut sampai dengan 5 (lima) tahun. (3) Kepada orang pribadi sebagai Wajib Pajak dalam negeri diberikan pengurangan berupa Penghasilan Tidak Kena Pajak sebagaimana dimaksud dalam Pasal 7. 3. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, di antara ayat (2) dan ayat (3) Pasal 7 disisipkan 1 (satu) ayat, yakni ayat (2a), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Penghasilan Tidak Kena Pajak per tahun diberikan paling sedikit: a. Rp54.000.000,00 (lima puluh empat juta rupiah) untuk diri Wajib Pajak orang pribadi; b. Rp4.500.000,00 (empat juta lima ratus ribu rupiah) tambahan untuk Wajib Pajak yang kawin; c. Rp54.000.000,00 (lima puluh empat juta rupiah) tambahan untuk seorang isteri yang penghasilannya digabung dengan penghasilan suami sebagaimana dimaksud dalam Pasal 8 ayat (1); dan d. Rp4.500.000,00 (empat juta lima ratus ribu rupiah) tambahan untuk setiap anggota keluarga sedarah dan keluarga semenda dalam garis keturunan lurus serta anak angkat, yang menjadi tanggungan sepenuhnya, paling banyak 3 (tiga) orang untuk setiap keluarga. (2) Penerapan ketentuan sebagaimana dimaksud pada ayat (1) ditentukan oleh keadaan pada awal tahun pajak atau awal bagian tahun pajak. (2a) Wajib Pajak orang pribadi yang memiliki peredaran bruto tertentu sebagaimana dimaksud dalam Pasal 4 ayat (2) huruf e tidak dikenai Pajak Penghasilan atas bagian peredaran bruto sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) dalam 1 (satu) tahun pajak. (3) Penyesuaian besarnya: a. Penghasilan

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d06 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tambahan Penghasilan Tidak Kena Pajak untuk Wajib Pajak yang kawin?

**Jawaban referensi:** Rp4.500.000,00 (empat juta lima ratus ribu rupiah) [Pasal 7 ayat (1) huruf b UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0048`

<details>
<summary>uu-hpp-2021-bt:0048 (hlm. 53-54)</summary>

ayat (1) didapat kerugian, kerugian tersebut dikompensasikan dengan penghasilan mulai tahun pajak berikutnya berturut-turut sampai dengan 5 (lima) tahun. (3) Kepada orang pribadi sebagai Wajib Pajak dalam negeri diberikan pengurangan berupa Penghasilan Tidak Kena Pajak sebagaimana dimaksud dalam Pasal 7. 3. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, di antara ayat (2) dan ayat (3) Pasal 7 disisipkan 1 (satu) ayat, yakni ayat (2a), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Penghasilan Tidak Kena Pajak per tahun diberikan paling sedikit: a. Rp54.000.000,00 (lima puluh empat juta rupiah) untuk diri Wajib Pajak orang pribadi; b. Rp4.500.000,00 (empat juta lima ratus ribu rupiah) tambahan untuk Wajib Pajak yang kawin; c. Rp54.000.000,00 (lima puluh empat juta rupiah) tambahan untuk seorang isteri yang penghasilannya digabung dengan penghasilan suami sebagaimana dimaksud dalam Pasal 8 ayat (1); dan d. Rp4.500.000,00 (empat juta lima ratus ribu rupiah) tambahan untuk setiap anggota keluarga sedarah dan keluarga semenda dalam garis keturunan lurus serta anak angkat, yang menjadi tanggungan sepenuhnya, paling banyak 3 (tiga) orang untuk setiap keluarga. (2) Penerapan ketentuan sebagaimana dimaksud pada ayat (1) ditentukan oleh keadaan pada awal tahun pajak atau awal bagian tahun pajak. (2a) Wajib Pajak orang pribadi yang memiliki peredaran bruto tertentu sebagaimana dimaksud dalam Pasal 4 ayat (2) huruf e tidak dikenai Pajak Penghasilan atas bagian peredaran bruto sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) dalam 1 (satu) tahun pajak. (3) Penyesuaian besarnya: a. Penghasilan

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d07 · direct · ⬜ BELUM
**Pertanyaan:** Apa yang digunakan sebagai Nomor Pokok Wajib Pajak bagi Wajib Pajak orang pribadi penduduk Indonesia?

**Jawaban referensi:** Nomor induk kependudukan (NIK) [Pasal 2 ayat (1a) UU KUP jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0005`

<details>
<summary>uu-hpp-2021-bt:0005 (hlm. 6-7)</summary>

49, Tambahan Lembaran Negara Republik Indonesia Nomor 3262) sebagaimana telah beberapa kali diubah terakhir dengan Undang-Undang Nomor 16 Tahun 2009 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 5 Tahun 2008 tentang Perubahan Keempat atas Undang-Undang Nomor 6 Tahun 1983 tentang Ketentuan Umum dan Tata Cara Perpajakan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2009 Nomor 62, Tambahan Lembaran Negara Republik Indonesia Nomor 4999) diubah sebagai berikut: 1. Di antara ayat (1) dan ayat (2) Pasal 2 disisipkan 1 (satu) ayat, yakni ayat (1a), Pasal 2 ayat (5) dihapus, serta ditambahkan 1 (satu) ayat, yakni ayat (10) sehingga Pasal 2 berbunyi sebagai berikut: Pasal 2 (1) Setiap Wajib Pajak yang telah memenuhi persyaratan subjektif dan objektif sesuai dengan ketentuan peraturan perundang-undangan perpajakan wajib mendaftarkan diri pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya meliputi tempat tinggal atau tempat kedudukan Wajib Pajak dan kepadanya diberikan Nomor Pokok Wajib Pajak. (1a) Nomor Pokok Wajib Pajak sebagaimana dimaksud pada ayat (1) bagi Wajib Pajak orang pribadi yang merupakan penduduk Indonesia menggunakan nomor induk kependudukan. (2) Setiap Wajib Pajak sebagai Pengusaha yang dikenai pajak berdasarkan Undang-Undang Pajak Pertambahan Nilai 1984 dan perubahannya, wajib melaporkan usahanya pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya meliputi tempat tinggal atau tempat kedudukan Pengusaha, dan tempat kegiatan usaha dilakukan untuk dikukuhkan menjadi Pengusaha Kena Pajak. (3) Direktur Jenderal Pajak dapat menetapkan: a. tempat pendaftaran dan/atau tempat pelaporan usaha selain yang ditetapkan pada ayat (1) dan ayat (2); dan/atau b. tempat pendaftaran pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d08 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tarif PPN yang mulai berlaku 1 April 2022?

**Jawaban referensi:** 11% (sebelas persen) [Pasal 7 ayat (1) huruf a UU PPN jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0068`

<details>
<summary>uu-hpp-2021-bt:0068 (hlm. 74-75)</summary>

daerah; o. dihapus; p. dihapus; dan q. jasa boga atau katering, meliputi semua kegiatan pelayanan penyediaan makanan dan minuman yang merupakan objek pajak daerah dan retribusi daerah sesuai dengan ketentuan peraturan perundang-undangan di bidang pajak daerah dan retribusi daerah. 2. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, ditambahkan 1 (satu) ayat, yakni ayat (4), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Tarif Pajak Pertambahan Nilai yaitu: a. sebesar 11% (sebelas persen) yang mulai berlaku pada tanggal 1 April 2022; b. sebesar 12% (dua belas persen) yang mulai berlaku paling lambat pada tanggal 1 Januari 2025. (2) Tarif Pajak Pertambahan Nilai sebesar 0% (nol persen) diterapkan atas: a. ekspor Barang Kena Pajak Berwujud; b. ekspor Barang Kena Pajak Tidak Berwujud; dan c. ekspor Jasa Kena Pajak. (3) Tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (1) dapat diubah menjadi paling rendah 5% (lima persen) dan paling tinggi 15% (lima belas persen). (4) Perubahan tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah setelah disampaikan oleh Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. 3. Ketentuan Pasal 8A ayat (2) dihapus, dan ditambahkan 1 (satu) ayat, yakni ayat (3) sehingga Pasal 8A berbunyi sebagai berikut: Pasal 8A (1) Pajak Pertambahan Nilai yang terutang dihitung dengan cara mengalikan tarif sebagaimana dimaksud dalam Pasal 7 dengan Dasar Pengenaan Pajak yang meliputi

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d09 · direct · ⬜ BELUM
**Pertanyaan:** Kapan paling lambat tarif PPN 12% mulai berlaku?

**Jawaban referensi:** Paling lambat 1 Januari 2025 [Pasal 7 ayat (1) huruf b UU PPN jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0068`

<details>
<summary>uu-hpp-2021-bt:0068 (hlm. 74-75)</summary>

daerah; o. dihapus; p. dihapus; dan q. jasa boga atau katering, meliputi semua kegiatan pelayanan penyediaan makanan dan minuman yang merupakan objek pajak daerah dan retribusi daerah sesuai dengan ketentuan peraturan perundang-undangan di bidang pajak daerah dan retribusi daerah. 2. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, ditambahkan 1 (satu) ayat, yakni ayat (4), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Tarif Pajak Pertambahan Nilai yaitu: a. sebesar 11% (sebelas persen) yang mulai berlaku pada tanggal 1 April 2022; b. sebesar 12% (dua belas persen) yang mulai berlaku paling lambat pada tanggal 1 Januari 2025. (2) Tarif Pajak Pertambahan Nilai sebesar 0% (nol persen) diterapkan atas: a. ekspor Barang Kena Pajak Berwujud; b. ekspor Barang Kena Pajak Tidak Berwujud; dan c. ekspor Jasa Kena Pajak. (3) Tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (1) dapat diubah menjadi paling rendah 5% (lima persen) dan paling tinggi 15% (lima belas persen). (4) Perubahan tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah setelah disampaikan oleh Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. 3. Ketentuan Pasal 8A ayat (2) dihapus, dan ditambahkan 1 (satu) ayat, yakni ayat (3) sehingga Pasal 8A berbunyi sebagai berikut: Pasal 8A (1) Pajak Pertambahan Nilai yang terutang dihitung dengan cara mengalikan tarif sebagaimana dimaksud dalam Pasal 7 dengan Dasar Pengenaan Pajak yang meliputi

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d10 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tarif PPN atas ekspor Barang Kena Pajak Berwujud?

**Jawaban referensi:** 0% (nol persen) [Pasal 7 ayat (2) UU PPN jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0068`

<details>
<summary>uu-hpp-2021-bt:0068 (hlm. 74-75)</summary>

daerah; o. dihapus; p. dihapus; dan q. jasa boga atau katering, meliputi semua kegiatan pelayanan penyediaan makanan dan minuman yang merupakan objek pajak daerah dan retribusi daerah sesuai dengan ketentuan peraturan perundang-undangan di bidang pajak daerah dan retribusi daerah. 2. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, ditambahkan 1 (satu) ayat, yakni ayat (4), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Tarif Pajak Pertambahan Nilai yaitu: a. sebesar 11% (sebelas persen) yang mulai berlaku pada tanggal 1 April 2022; b. sebesar 12% (dua belas persen) yang mulai berlaku paling lambat pada tanggal 1 Januari 2025. (2) Tarif Pajak Pertambahan Nilai sebesar 0% (nol persen) diterapkan atas: a. ekspor Barang Kena Pajak Berwujud; b. ekspor Barang Kena Pajak Tidak Berwujud; dan c. ekspor Jasa Kena Pajak. (3) Tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (1) dapat diubah menjadi paling rendah 5% (lima persen) dan paling tinggi 15% (lima belas persen). (4) Perubahan tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah setelah disampaikan oleh Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. 3. Ketentuan Pasal 8A ayat (2) dihapus, dan ditambahkan 1 (satu) ayat, yakni ayat (3) sehingga Pasal 8A berbunyi sebagai berikut: Pasal 8A (1) Pajak Pertambahan Nilai yang terutang dihitung dengan cara mengalikan tarif sebagaimana dimaksud dalam Pasal 7 dengan Dasar Pengenaan Pajak yang meliputi

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d11 · direct · ⬜ BELUM
**Pertanyaan:** Atas apa pajak karbon dikenakan?

**Jawaban referensi:** Atas emisi karbon yang memberikan dampak negatif bagi lingkungan hidup [Pasal 13 ayat (1) UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0096` **ATAU** `uu-hpp-2021-bt:0097`

<details>
<summary>uu-hpp-2021-bt:0096 (hlm. 103-104)</summary>

Pajak yang tidak memenuhi ketentuan sebagaimana dimaksud dalam Pasal 9 ayat (3) huruf d angka 1, dalam hal Direktur Jenderal Pajak menerbitkan Surat Ketetapan Pajak Kurang Bayar; atau b. terhadap penghasilan dimaksud dikenai tambahan Pajak Penghasilan yang bersifat final dengan tarif sebesar: 1. 3% (tiga persen) bagi Wajib Pajak yang tidak memenuhi ketentuan sebagaimana dimaksud dalam Pasal 9 ayat (3) huruf a; 2. 3% (tiga persen) bagi Wajib Pajak yang tidak memenuhi ketentuan sebagaimana dimaksud dalam Pasal 9 ayat (3) huruf c angka 2; 3. 7% (tujuh persen) bagi Wajib Pajak yang tidak memenuhi ketentuan sebagaimana dimaksud dalam Pasal 9 ayat (3) huruf c; atau 4. 5% (lima persen) bagi Wajib Pajak yang tidak memenuhi ketentuan sebagaimana dimaksud dalam Pasal 9 ayat (3) huruf d angka 1, dalam hal Wajib Pajak atas kehendak sendiri mengungkapkan penghasilan tersebut dan menyetorkan sendiri Pajak Penghasilan yang terutang. (5) Ketentuan lebih lanjut mengenai: a. tata cara pengalihan harta bersih ke dalam wilayah Negara Kesatuan Republik Indonesia; b. investasi harta bersih pada kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan c. instrumen surat berharga negara yang digunakan untuk investasi, diatur dengan Peraturan Menteri Keuangan. BAB VI PAJAK KARBON Pasal 13 (1) Pajak karbon dikenakan atas emisi karbon yang memberikan dampak negatif bagi lingkungan hidup. (2) Pengenaan pajak karbon sebagaimana dimaksud pada ayat (1) dilakukan dengan memperhatikan: a. peta jalan pajak karbon; dan/atau b. peta jalan pasar karbon. (3) Peta jalan pajak karbon sebagaimana dimaksud

</details>

<details>
<summary>uu-hpp-2021-bt:0097 (hlm. 104-105)</summary>

BAB VI PAJAK KARBON Pasal 13 (1) Pajak karbon dikenakan atas emisi karbon yang memberikan dampak negatif bagi lingkungan hidup. (2) Pengenaan pajak karbon sebagaimana dimaksud pada ayat (1) dilakukan dengan memperhatikan: a. peta jalan pajak karbon; dan/atau b. peta jalan pasar karbon. (3) Peta jalan pajak karbon sebagaimana dimaksud pada ayat (2) huruf a memuat: a. strategi penurunan emisi karbon; b. sasaran sektor prioritas; c. keselarasan dengan pembangunan energi baru dan terbarukan; dan/atau d. keselarasan antarberbagai kebijakan lainnya. (4) Kebijakan peta jalan pajak karbon sebagaimana dimaksud pada ayat (3) ditetapkan oleh Pemerintah dengan persetujuan Dewan Perwakilan Rakyat Republik Indonesia. (5) Subjek pajak karbon yaitu orang pribadi atau badan yang membeli barang yang mengandung karbon dan/atau melakukan aktivitas yang menghasilkan emisi karbon. (6) Pajak karbon terutang atas pembelian barang yang mengandung karbon atau aktivitas yang menghasilkan emisi karbon dalam jumlah tertentu pada periode tertentu. (7) Saat terutang pajak karbon ditentukan: a. pada saat pembelian barang yang mengandung karbon; b. pada akhir periode tahun kalender dari aktivitas yang menghasilkan emisi karbon dalam jumlah tertentu; atau c. saat lain yang diatur dengan atau berdasarkan Peraturan Pemerintah. (8) Tarif pajak karbon ditetapkan lebih tinggi atau sama dengan harga karbon di pasar karbon per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (9) Dalam hal harga karbon di pasar karbon sebagaimana dimaksud pada ayat (8) lebih rendah dari Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara, tarif pajak karbon ditetapkan sebesar paling rendah Rp30,00 (tiga puluh rupiah)

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d12 · direct · ⬜ BELUM
**Pertanyaan:** Berapa tarif minimum pajak karbon per kilogram CO2 ekuivalen?

**Jawaban referensi:** Paling rendah Rp30,00 (tiga puluh rupiah) per kilogram CO2e [Pasal 13 ayat (8)-(9) UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0097` **ATAU** `uu-hpp-2021-bt:0098`

<details>
<summary>uu-hpp-2021-bt:0097 (hlm. 104-105)</summary>

BAB VI PAJAK KARBON Pasal 13 (1) Pajak karbon dikenakan atas emisi karbon yang memberikan dampak negatif bagi lingkungan hidup. (2) Pengenaan pajak karbon sebagaimana dimaksud pada ayat (1) dilakukan dengan memperhatikan: a. peta jalan pajak karbon; dan/atau b. peta jalan pasar karbon. (3) Peta jalan pajak karbon sebagaimana dimaksud pada ayat (2) huruf a memuat: a. strategi penurunan emisi karbon; b. sasaran sektor prioritas; c. keselarasan dengan pembangunan energi baru dan terbarukan; dan/atau d. keselarasan antarberbagai kebijakan lainnya. (4) Kebijakan peta jalan pajak karbon sebagaimana dimaksud pada ayat (3) ditetapkan oleh Pemerintah dengan persetujuan Dewan Perwakilan Rakyat Republik Indonesia. (5) Subjek pajak karbon yaitu orang pribadi atau badan yang membeli barang yang mengandung karbon dan/atau melakukan aktivitas yang menghasilkan emisi karbon. (6) Pajak karbon terutang atas pembelian barang yang mengandung karbon atau aktivitas yang menghasilkan emisi karbon dalam jumlah tertentu pada periode tertentu. (7) Saat terutang pajak karbon ditentukan: a. pada saat pembelian barang yang mengandung karbon; b. pada akhir periode tahun kalender dari aktivitas yang menghasilkan emisi karbon dalam jumlah tertentu; atau c. saat lain yang diatur dengan atau berdasarkan Peraturan Pemerintah. (8) Tarif pajak karbon ditetapkan lebih tinggi atau sama dengan harga karbon di pasar karbon per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (9) Dalam hal harga karbon di pasar karbon sebagaimana dimaksud pada ayat (8) lebih rendah dari Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara, tarif pajak karbon ditetapkan sebesar paling rendah Rp30,00 (tiga puluh rupiah)

</details>

<details>
<summary>uu-hpp-2021-bt:0098 (hlm. 105-106)</summary>

kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (9) Dalam hal harga karbon di pasar karbon sebagaimana dimaksud pada ayat (8) lebih rendah dari Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara, tarif pajak karbon ditetapkan sebesar paling rendah Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (10) Ketentuan mengenai: a. penetapan tarif pajak karbon sebagaimana dimaksud pada ayat (8); b. perubahan tarif pajak karbon sebagaimana dimaksud pada ayat (9); dan/atau c. dasar pengenaan pajak, diatur dengan Peraturan Menteri Keuangan setelah dikonsultasikan dengan Dewan Perwakilan Rakyat Republik Indonesia. (11) Ketentuan mengenai penambahan objek pajak yang dikenai pajak karbon sebagaimana dimaksud pada ayat (1) diatur dengan atau berdasarkan Peraturan Pemerintah setelah disampaikan Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. (12) Penerimaan dari pajak karbon dapat dialokasikan untuk pengendalian perubahan iklim. (13) Wajib Pajak yang berpartisipasi dalam perdagangan emisi karbon, pengimbangan emisi karbon, dan/atau mekanisme lain sesuai peraturan perundang- undangan di bidang lingkungan hidup dapat diberikan: a. pengurangan pajak karbon; dan/atau b. perlakuan lainnya atas pemenuhan kewajiban pajak karbon. (14) Ketentuan mengenai: a. tata cara penghitungan, pemungutan, pembayaran atau penyetoran, pelaporan, dan mekanisme pengenaan pajak karbon; dan b. tata cara pengurangan pajak karbon sebagaimana dimaksud pada ayat (13) huruf a dan/atau perlakuan lainnya atas pemenuhan kewajiban pajak karbon sebagaimana dimaksud pada ayat (13) huruf b, diatur dengan Peraturan Menteri Keuangan. (15) Ketentuan mengenai: a. subjek pajak karbon

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d13 · direct · ⬜ BELUM
**Pertanyaan:** Sektor apa yang pertama kali dikenakan pajak karbon dan kapan mulai berlaku?

**Jawaban referensi:** Badan di bidang pembangkit listrik tenaga uap batubara, mulai 1 April 2022, tarif Rp30/kg CO2e [Pasal 17 ayat (3) UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0105`

<details>
<summary>uu-hpp-2021-bt:0105 (hlm. 112-114)</summary>

Lembaran Negara Republik Indonesia Nomor 6573), dinyatakan masih tetap berlaku sepanjang tidak bertentangan dengan ketentuan dalam Undang-Undang ini atau belum diganti berdasarkan Undang-Undang ini. Pasal 17 (1) Ketentuan sebagaimana dimaksud dalam Pasal 3 mulai berlaku pada Tahun Pajak 2022. (2) Ketentuan sebagaimana dimaksud dalam Pasal 4 mulai berlaku pada tanggal 1 April 2022. (3) Ketentuan sebagaimana dimaksud dalam Pasal 13 mulai berlaku pada tanggal 1 April 2022, yang pertama kali dikenakan terhadap badan yang bergerak di bidang pembangkit listrik tenaga uap batubara dengan tarif Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. Pasal 18 Ketentuan Pasal 5 ayat (1) huruf b Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan Untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 87, Tambahan Lembaran Negara Republik Indonesia Nomor 6485) yang telah ditetapkan menjadi Undang-Undang Nomor 2 Tahun 2020 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 134, Tambahan Lembaran Negara Republik Indonesia Nomor 6516), dicabut dan dinyatakan tidak berlaku. Pasal 19 Undang-Undang ini mulai berlaku pada tanggal diundangkan. Agar setiap orang mengetahuinya, memerintahkan pengundangan Undang-Undang ini dengan penempatannya dalam Lembaran

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d14 · direct · ⬜ BELUM
**Pertanyaan:** Apakah imbalan dalam bentuk natura dan/atau kenikmatan termasuk objek Pajak Penghasilan?

**Jawaban referensi:** Ya, penggantian atau imbalan dalam bentuk natura dan/atau kenikmatan termasuk penghasilan yang menjadi objek PPh, kecuali ditentukan lain [Pasal 4 ayat (1) huruf a UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0036`

<details>
<summary>uu-hpp-2021-bt:0036 (hlm. 39-40)</summary>

1983 tentang Pajak Penghasilan (Lembaran Negara Republik Indonesia Tahun 1983 Nomor 50, Tambahan Lembaran Negara Republik Indonesia Nomor 3263) sebagaimana telah beberapa kali diubah terakhir dengan Undang-Undang Nomor 36 Tahun 2008 tentang Perubahan Keempat atas Undang-Undang Nomor 7 Tahun 1983 tentang Pajak Penghasilan (Lembaran Negara Republik Indonesia Tahun 2008 Nomor 133, Tambahan Lembaran Negara Republik Indonesia Nomor 4893) diubah sebagai berikut: 1. Ketentuan ayat (1), ayat (1a), ayat (2), dan ayat (3) Pasal 4 diubah serta Pasal 4 ayat (1d) dihapus sehingga Pasal 4 berbunyi sebagai berikut: Pasal 4 (1) Yang menjadi objek pajak adalah penghasilan, yaitu setiap tambahan kemampuan ekonomis yang diterima atau diperoleh Wajib Pajak, baik yang berasal dari Indonesia maupun dari luar Indonesia, yang dapat dipakai untuk konsumsi atau untuk menambah kekayaan Wajib Pajak yang bersangkutan, dengan nama dan dalam bentuk apa pun, termasuk: a. penggantian atau imbalan berkenaan dengan pekerjaan atau jasa yang diterima atau diperoleh termasuk gaji, upah, tunjangan, honorarium, komisi, bonus, gratifikasi, uang pensiun, atau imbalan dalam bentuk lainnya termasuk natura dan/atau kenikmatan, kecuali ditentukan lain dalam Undang- Undang ini; b. hadiah dari undian atau pekerjaan atau kegiatan, dan penghargaan; c. laba usaha; d. keuntungan karena penjualan atau karena pengalihan harta termasuk: 1. keuntungan karena pengalihan harta kepada perseroan, persekutuan, dan badan lainnya sebagai pengganti saham atau penyertaan modal; 2. keuntungan karena pengalihan harta kepada pemegang saham, sekutu, atau anggota yang diperoleh perseroan, persekutuan, dan badan lainnya; 3. keuntungan karena likuidasi, penggabungan, peleburan, pemekaran, pemecahan, pengambilalihan usaha, atau reorganisasi dengan nama dan dalam bentuk

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d15 · direct · ⬜ BELUM
**Pertanyaan:** Natura jenis apa saja yang dikecualikan dari objek Pajak Penghasilan?

**Jawaban referensi:** Antara lain: makanan/bahan makanan/minuman bagi seluruh pegawai, natura di daerah tertentu, natura karena keharusan pekerjaan, natura dari APBN/APBD, dan natura jenis/batasan tertentu [Pasal 4 ayat (3) huruf d UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0040`

<details>
<summary>uu-hpp-2021-bt:0040 (hlm. 43-44)</summary>

penerima zakat yang berhak atau sumbangan keagamaan yang sifatnya wajib bagi pemeluk agama yang diakui di Indonesia, yang diterima oleh lembaga keagamaan yang dibentuk atau disahkan oleh pemerintah dan yang diterima oleh penerima sumbangan yang berhak, yang ketentuannya diatur dengan atau berdasarkan Peraturan Pemerintah; dan 2. harta hibahan yang diterima oleh keluarga sedarah dalam garis keturunan lurus satu derajat, badan keagamaan, badan pendidikan, badan sosial termasuk yayasan, koperasi, atau orang pribadi yang menjalankan usaha mikro dan kecil, sepanjang tidak ada hubungan dengan usaha, pekerjaan, kepemilikan, atau penguasaan di antara pihak-pihak yang bersangkutan; b. warisan; c. harta termasuk setoran tunai yang diterima oleh badan sebagaimana dimaksud dalam Pasal 2 ayat (1) huruf b sebagai pengganti saham atau sebagai pengganti penyertaan modal; d. penggantian atau imbalan sehubungan dengan pekerjaan atau jasa yang diterima atau diperoleh dalam bentuk natura dan/atau kenikmatan, meliputi: 1. makanan, bahan makanan, bahan minuman, dan/atau minuman bagi seluruh pegawai; 2. natura dan/atau kenikmatan yang disediakan di daerah tertentu; 3. natura dan/atau kenikmatan yang harus disediakan oleh pemberi kerja dalam pelaksanaan pekerjaan; 4. natura dan/atau kenikmatan yang bersumber atau dibiayai Anggaran Pendapatan dan Belanja Negara, Anggaran Pendapatan dan Belanja Daerah, dan/atau Anggaran Pendapatan dan Belanja Desa; atau 5. natura dan/atau kenikmatan dengan jenis dan/atau batasan tertentu; e. pembayaran dari perusahaan asuransi karena kecelakaan, sakit, atau karena meninggalnya orang yang tertanggung, dan pembayaran asuransi beasiswa; f. dividen atau penghasilan lain dengan ketentuan sebagai berikut: 1. dividen yang berasal dari dalam negeri yang diterima atau diperoleh Wajib Pajak: a) orang pribadi dalam

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## d16 · direct · ⬜ BELUM
**Pertanyaan:** Dalam program pengungkapan sukarela untuk harta perolehan 2016-2020, berapa tarif PPh final atas harta bersih di dalam negeri yang diinvestasikan pada SBN atau hilirisasi SDA/energi terbarukan?

**Jawaban referensi:** 12% (dua belas persen) [Pasal 9 ayat (3) huruf a UU HPP — Kebijakan II PPS, harta perolehan 2016-2020].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0089`

<details>
<summary>uu-hpp-2021-bt:0089 (hlm. 96-97)</summary>

sedang menjalani hukuman pidana atas tindak pidana di bidang perpajakan. Pasal 9 (1) Tambahan penghasilan sebagaimana dimaksud dalam Pasal 8 ayat (3) dikenai Pajak Penghasilan yang bersifat final. (2) Pajak Penghasilan yang bersifat final sebagaimana dimaksud pada ayat (1) dihitung dengan cara mengalikan tarif dengan dasar pengenaan pajak. (3) Tarif sebagaimana dimaksud pada ayat (2) ditetapkan sebesar: a. 12% (dua belas persen) atas harta bersih yang berada di dalam wilayah Negara Kesatuan Republik Indonesia, dengan ketentuan diinvestasikan pada: 1. kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau 2. surat berharga negara; b. 14% (empat belas persen) atas harta bersih yang berada di dalam wilayah Negara Kesatuan Republik Indonesia dan tidak diinvestasikan pada: 1. kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau 2. surat berharga negara; c. 12% (dua belas persen) atas harta bersih yang berada di luar wilayah Negara Kesatuan Republik Indonesia, dengan ketentuan: 1. dialihkan ke dalam wilayah Negara Kesatuan Republik Indonesia; dan 2. diinvestasikan pada: a) kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau b) surat berharga negara; d. 14% (empat belas persen) atas harta bersih yang berada di luar wilayah Negara Kesatuan Republik Indonesia dengan ketentuan: 1. dialihkan ke dalam wilayah Negara Kesatuan Republik Indonesia; dan 2. tidak diinvestasikan pada: a) kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p01 · paraphrase · ⬜ BELUM
**Pertanyaan:** PT kecil punyaku laba tahun 2023, setor pajak penghasilannya berapa persen ya?

**Jawaban referensi:** Tarif PPh badan dalam negeri 22% [Pasal 17 ayat (1) huruf b UU PPh jo. UU HPP]. (Catatan: fasilitas Pasal 31E untuk peredaran bruto kecil tidak tercakup korpus ini.)

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0056` **ATAU** `uu-hpp-2021-bt:0057`

<details>
<summary>uu-hpp-2021-bt:0056 (hlm. 61-63)</summary>

kerugian dan jumlah yang diterima sebagai penggantian merupakan penghasilan pada tahun terjadinya pengalihan tersebut. (8) Apabila terjadi pengalihan harta yang memenuhi syarat sebagaimana dimaksud dalam Pasal 4 ayat (3) huruf a dan huruf b, yang berupa harta tak berwujud, maka jumlah nilai sisa buku harta tersebut tidak boleh dibebankan sebagai kerugian bagi pihak yang mengalihkan. 7. Ketentuan ayat (1), ayat (2), ayat (2b), dan ayat (3) Pasal 17 diubah, Pasal 17 ayat (2a) dihapus, di antara ayat (2d) dan ayat (3) Pasal 17 disisipkan 1 (satu) ayat, yakni ayat (2e), serta penjelasan ayat (5) dan ayat (6) Pasal 17 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 17 berbunyi sebagai berikut: Pasal 17 (1) Tarif pajak yang diterapkan atas Penghasilan Kena Pajak bagi: a. Wajib Pajak orang pribadi dalam negeri sebagai berikut: Lapisan Penghasilan Kena Pajak Tarif Pajak sampai dengan Rp60.000.000,00 (enam puluh juta rupiah) 5% (lima persen) di atas Rp60.000.000,00 (enam puluh juta rupiah) sampai dengan Rp250.000.000,00 (dua ratus lima puluh juta rupiah) 15% (lima belas persen) di atas Rp250.000.000,00 (dua ratus lima puluh juta rupiah) sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) 25% (dua puluh lima persen) di atas Rp500.000.000,00 (lima ratus juta rupiah) sampai dengan Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf

</details>

<details>
<summary>uu-hpp-2021-bt:0057 (hlm. 62-64)</summary>

Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Pemerintah setelah disampaikan oleh pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. (2a) Dihapus. (2b) Wajib Pajak badan dalam negeri: a. berbentuk perseroan terbuka; b. dengan jumlah keseluruhan saham yang disetor diperdagangkan pada bursa efek di Indonesia paling sedikit 40% (empat puluh persen); dan c. memenuhi persyaratan tertentu, dapat memperoleh tarif sebesar 3% (tiga persen) lebih rendah dari tarif sebagaimana dimaksud pada ayat (1) huruf b. (2c) Tarif yang dikenakan atas penghasilan berupa dividen yang dibagikan kepada Wajib Pajak orang pribadi dalam negeri adalah paling tinggi sebesar 10% (sepuluh persen) dan bersifat final. (2d) Ketentuan lebih lanjut mengenai besarnya tarif sebagaimana dimaksud pada ayat (2c) diatur dengan Peraturan Pemerintah. (2e) Ketentuan lebih lanjut mengenai persyaratan tertentu sebagaimana dimaksud pada ayat (2b) huruf c diatur dengan atau berdasarkan Peraturan Pemerintah. (3) Besarnya lapisan Penghasilan Kena Pajak sebagaimana dimaksud pada ayat (1) huruf a dapat diubah dengan Peraturan Menteri Keuangan. (4) Untuk keperluan penerapan tarif pajak sebagaimana dimaksud pada ayat (1), jumlah Penghasilan Kena Pajak dibulatkan ke bawah dalam ribuan rupiah penuh. (5) Besarnya pajak yang terutang bagi Wajib Pajak orang pribadi dalam negeri yang terutang

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p02 · paraphrase · ⬜ BELUM
**Pertanyaan:** Gajiku setahun cuma 50 juta, kena potongan pajak berapa persen sih?

**Jawaban referensi:** Lapisan penghasilan kena pajak s.d. Rp60 juta dikenai 5% [Pasal 17 ayat (1) huruf a UU PPh jo. UU HPP] — itupun setelah dikurangi PTKP.

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0056`

<details>
<summary>uu-hpp-2021-bt:0056 (hlm. 61-63)</summary>

kerugian dan jumlah yang diterima sebagai penggantian merupakan penghasilan pada tahun terjadinya pengalihan tersebut. (8) Apabila terjadi pengalihan harta yang memenuhi syarat sebagaimana dimaksud dalam Pasal 4 ayat (3) huruf a dan huruf b, yang berupa harta tak berwujud, maka jumlah nilai sisa buku harta tersebut tidak boleh dibebankan sebagai kerugian bagi pihak yang mengalihkan. 7. Ketentuan ayat (1), ayat (2), ayat (2b), dan ayat (3) Pasal 17 diubah, Pasal 17 ayat (2a) dihapus, di antara ayat (2d) dan ayat (3) Pasal 17 disisipkan 1 (satu) ayat, yakni ayat (2e), serta penjelasan ayat (5) dan ayat (6) Pasal 17 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 17 berbunyi sebagai berikut: Pasal 17 (1) Tarif pajak yang diterapkan atas Penghasilan Kena Pajak bagi: a. Wajib Pajak orang pribadi dalam negeri sebagai berikut: Lapisan Penghasilan Kena Pajak Tarif Pajak sampai dengan Rp60.000.000,00 (enam puluh juta rupiah) 5% (lima persen) di atas Rp60.000.000,00 (enam puluh juta rupiah) sampai dengan Rp250.000.000,00 (dua ratus lima puluh juta rupiah) 15% (lima belas persen) di atas Rp250.000.000,00 (dua ratus lima puluh juta rupiah) sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) 25% (dua puluh lima persen) di atas Rp500.000.000,00 (lima ratus juta rupiah) sampai dengan Rp5.000.000.000,00 (lima miliar rupiah) 30% (tiga puluh persen) di atas Rp5.000.000.000,00 (lima miliar rupiah) 35% (tiga puluh lima persen) b. Wajib Pajak badan dalam negeri dan bentuk usaha tetap sebesar 22% (dua puluh dua persen) yang mulai berlaku pada tahun pajak 2022. (2) Tarif sebagaimana dimaksud pada ayat (1) huruf

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p03 · paraphrase · ⬜ BELUM
**Pertanyaan:** Batas penghasilan setahun yang bebas dari pajak buat yang masih lajang itu berapa?

**Jawaban referensi:** PTKP diri Wajib Pajak orang pribadi paling sedikit Rp54.000.000 per tahun [Pasal 7 ayat (1) huruf a UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0048`

<details>
<summary>uu-hpp-2021-bt:0048 (hlm. 53-54)</summary>

ayat (1) didapat kerugian, kerugian tersebut dikompensasikan dengan penghasilan mulai tahun pajak berikutnya berturut-turut sampai dengan 5 (lima) tahun. (3) Kepada orang pribadi sebagai Wajib Pajak dalam negeri diberikan pengurangan berupa Penghasilan Tidak Kena Pajak sebagaimana dimaksud dalam Pasal 7. 3. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, di antara ayat (2) dan ayat (3) Pasal 7 disisipkan 1 (satu) ayat, yakni ayat (2a), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Penghasilan Tidak Kena Pajak per tahun diberikan paling sedikit: a. Rp54.000.000,00 (lima puluh empat juta rupiah) untuk diri Wajib Pajak orang pribadi; b. Rp4.500.000,00 (empat juta lima ratus ribu rupiah) tambahan untuk Wajib Pajak yang kawin; c. Rp54.000.000,00 (lima puluh empat juta rupiah) tambahan untuk seorang isteri yang penghasilannya digabung dengan penghasilan suami sebagaimana dimaksud dalam Pasal 8 ayat (1); dan d. Rp4.500.000,00 (empat juta lima ratus ribu rupiah) tambahan untuk setiap anggota keluarga sedarah dan keluarga semenda dalam garis keturunan lurus serta anak angkat, yang menjadi tanggungan sepenuhnya, paling banyak 3 (tiga) orang untuk setiap keluarga. (2) Penerapan ketentuan sebagaimana dimaksud pada ayat (1) ditentukan oleh keadaan pada awal tahun pajak atau awal bagian tahun pajak. (2a) Wajib Pajak orang pribadi yang memiliki peredaran bruto tertentu sebagaimana dimaksud dalam Pasal 4 ayat (2) huruf e tidak dikenai Pajak Penghasilan atas bagian peredaran bruto sampai dengan Rp500.000.000,00 (lima ratus juta rupiah) dalam 1 (satu) tahun pajak. (3) Penyesuaian besarnya: a. Penghasilan

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p04 · paraphrase · ⬜ BELUM
**Pertanyaan:** Denger-denger sekarang KTP bisa langsung dipakai jadi nomor pajak, bener nggak?

**Jawaban referensi:** Benar — NPWP bagi WP orang pribadi penduduk Indonesia menggunakan nomor induk kependudukan [Pasal 2 ayat (1a) UU KUP jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0005`

<details>
<summary>uu-hpp-2021-bt:0005 (hlm. 6-7)</summary>

49, Tambahan Lembaran Negara Republik Indonesia Nomor 3262) sebagaimana telah beberapa kali diubah terakhir dengan Undang-Undang Nomor 16 Tahun 2009 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 5 Tahun 2008 tentang Perubahan Keempat atas Undang-Undang Nomor 6 Tahun 1983 tentang Ketentuan Umum dan Tata Cara Perpajakan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2009 Nomor 62, Tambahan Lembaran Negara Republik Indonesia Nomor 4999) diubah sebagai berikut: 1. Di antara ayat (1) dan ayat (2) Pasal 2 disisipkan 1 (satu) ayat, yakni ayat (1a), Pasal 2 ayat (5) dihapus, serta ditambahkan 1 (satu) ayat, yakni ayat (10) sehingga Pasal 2 berbunyi sebagai berikut: Pasal 2 (1) Setiap Wajib Pajak yang telah memenuhi persyaratan subjektif dan objektif sesuai dengan ketentuan peraturan perundang-undangan perpajakan wajib mendaftarkan diri pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya meliputi tempat tinggal atau tempat kedudukan Wajib Pajak dan kepadanya diberikan Nomor Pokok Wajib Pajak. (1a) Nomor Pokok Wajib Pajak sebagaimana dimaksud pada ayat (1) bagi Wajib Pajak orang pribadi yang merupakan penduduk Indonesia menggunakan nomor induk kependudukan. (2) Setiap Wajib Pajak sebagai Pengusaha yang dikenai pajak berdasarkan Undang-Undang Pajak Pertambahan Nilai 1984 dan perubahannya, wajib melaporkan usahanya pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya meliputi tempat tinggal atau tempat kedudukan Pengusaha, dan tempat kegiatan usaha dilakukan untuk dikukuhkan menjadi Pengusaha Kena Pajak. (3) Direktur Jenderal Pajak dapat menetapkan: a. tempat pendaftaran dan/atau tempat pelaporan usaha selain yang ditetapkan pada ayat (1) dan ayat (2); dan/atau b. tempat pendaftaran pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p05 · paraphrase · ⬜ BELUM
**Pertanyaan:** Pajak belanja naik jadi berapa persen dan mulainya kapan?

**Jawaban referensi:** PPN 11% mulai 1 April 2022, lalu 12% paling lambat 1 Januari 2025 [Pasal 7 ayat (1) UU PPN jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0068`

<details>
<summary>uu-hpp-2021-bt:0068 (hlm. 74-75)</summary>

daerah; o. dihapus; p. dihapus; dan q. jasa boga atau katering, meliputi semua kegiatan pelayanan penyediaan makanan dan minuman yang merupakan objek pajak daerah dan retribusi daerah sesuai dengan ketentuan peraturan perundang-undangan di bidang pajak daerah dan retribusi daerah. 2. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, ditambahkan 1 (satu) ayat, yakni ayat (4), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Tarif Pajak Pertambahan Nilai yaitu: a. sebesar 11% (sebelas persen) yang mulai berlaku pada tanggal 1 April 2022; b. sebesar 12% (dua belas persen) yang mulai berlaku paling lambat pada tanggal 1 Januari 2025. (2) Tarif Pajak Pertambahan Nilai sebesar 0% (nol persen) diterapkan atas: a. ekspor Barang Kena Pajak Berwujud; b. ekspor Barang Kena Pajak Tidak Berwujud; dan c. ekspor Jasa Kena Pajak. (3) Tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (1) dapat diubah menjadi paling rendah 5% (lima persen) dan paling tinggi 15% (lima belas persen). (4) Perubahan tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah setelah disampaikan oleh Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. 3. Ketentuan Pasal 8A ayat (2) dihapus, dan ditambahkan 1 (satu) ayat, yakni ayat (3) sehingga Pasal 8A berbunyi sebagai berikut: Pasal 8A (1) Pajak Pertambahan Nilai yang terutang dihitung dengan cara mengalikan tarif sebagaimana dimaksud dalam Pasal 7 dengan Dasar Pengenaan Pajak yang meliputi

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p06 · paraphrase · ⬜ BELUM
**Pertanyaan:** Kantor ngasih aku fasilitas mobil dinas, itu dihitung penghasilan kena pajak nggak?

**Jawaban referensi:** Imbalan dalam bentuk natura/kenikmatan pada prinsipnya termasuk objek PPh, kecuali yang dikecualikan [Pasal 4 ayat (1) huruf a UU PPh jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0036`

<details>
<summary>uu-hpp-2021-bt:0036 (hlm. 39-40)</summary>

1983 tentang Pajak Penghasilan (Lembaran Negara Republik Indonesia Tahun 1983 Nomor 50, Tambahan Lembaran Negara Republik Indonesia Nomor 3263) sebagaimana telah beberapa kali diubah terakhir dengan Undang-Undang Nomor 36 Tahun 2008 tentang Perubahan Keempat atas Undang-Undang Nomor 7 Tahun 1983 tentang Pajak Penghasilan (Lembaran Negara Republik Indonesia Tahun 2008 Nomor 133, Tambahan Lembaran Negara Republik Indonesia Nomor 4893) diubah sebagai berikut: 1. Ketentuan ayat (1), ayat (1a), ayat (2), dan ayat (3) Pasal 4 diubah serta Pasal 4 ayat (1d) dihapus sehingga Pasal 4 berbunyi sebagai berikut: Pasal 4 (1) Yang menjadi objek pajak adalah penghasilan, yaitu setiap tambahan kemampuan ekonomis yang diterima atau diperoleh Wajib Pajak, baik yang berasal dari Indonesia maupun dari luar Indonesia, yang dapat dipakai untuk konsumsi atau untuk menambah kekayaan Wajib Pajak yang bersangkutan, dengan nama dan dalam bentuk apa pun, termasuk: a. penggantian atau imbalan berkenaan dengan pekerjaan atau jasa yang diterima atau diperoleh termasuk gaji, upah, tunjangan, honorarium, komisi, bonus, gratifikasi, uang pensiun, atau imbalan dalam bentuk lainnya termasuk natura dan/atau kenikmatan, kecuali ditentukan lain dalam Undang- Undang ini; b. hadiah dari undian atau pekerjaan atau kegiatan, dan penghargaan; c. laba usaha; d. keuntungan karena penjualan atau karena pengalihan harta termasuk: 1. keuntungan karena pengalihan harta kepada perseroan, persekutuan, dan badan lainnya sebagai pengganti saham atau penyertaan modal; 2. keuntungan karena pengalihan harta kepada pemegang saham, sekutu, atau anggota yang diperoleh perseroan, persekutuan, dan badan lainnya; 3. keuntungan karena likuidasi, penggabungan, peleburan, pemekaran, pemecahan, pengambilalihan usaha, atau reorganisasi dengan nama dan dalam bentuk

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p07 · paraphrase · ⬜ BELUM
**Pertanyaan:** PLTU batu bara mulai kapan sih dipajakin emisinya?

**Jawaban referensi:** Pajak karbon pertama dikenakan pada badan pembangkit listrik tenaga uap batubara mulai 1 April 2022 [Pasal 17 ayat (3) UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0105`

<details>
<summary>uu-hpp-2021-bt:0105 (hlm. 112-114)</summary>

Lembaran Negara Republik Indonesia Nomor 6573), dinyatakan masih tetap berlaku sepanjang tidak bertentangan dengan ketentuan dalam Undang-Undang ini atau belum diganti berdasarkan Undang-Undang ini. Pasal 17 (1) Ketentuan sebagaimana dimaksud dalam Pasal 3 mulai berlaku pada Tahun Pajak 2022. (2) Ketentuan sebagaimana dimaksud dalam Pasal 4 mulai berlaku pada tanggal 1 April 2022. (3) Ketentuan sebagaimana dimaksud dalam Pasal 13 mulai berlaku pada tanggal 1 April 2022, yang pertama kali dikenakan terhadap badan yang bergerak di bidang pembangkit listrik tenaga uap batubara dengan tarif Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. Pasal 18 Ketentuan Pasal 5 ayat (1) huruf b Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan Untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 87, Tambahan Lembaran Negara Republik Indonesia Nomor 6485) yang telah ditetapkan menjadi Undang-Undang Nomor 2 Tahun 2020 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 134, Tambahan Lembaran Negara Republik Indonesia Nomor 6516), dicabut dan dinyatakan tidak berlaku. Pasal 19 Undang-Undang ini mulai berlaku pada tanggal diundangkan. Agar setiap orang mengetahuinya, memerintahkan pengundangan Undang-Undang ini dengan penempatannya dalam Lembaran

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## p08 · paraphrase · ⬜ BELUM
**Pertanyaan:** Kalau jualan barang ke luar negeri, PPN-nya gimana?

**Jawaban referensi:** Ekspor Barang Kena Pajak dikenai PPN 0% [Pasal 7 ayat (2) UU PPN jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0068`

<details>
<summary>uu-hpp-2021-bt:0068 (hlm. 74-75)</summary>

daerah; o. dihapus; p. dihapus; dan q. jasa boga atau katering, meliputi semua kegiatan pelayanan penyediaan makanan dan minuman yang merupakan objek pajak daerah dan retribusi daerah sesuai dengan ketentuan peraturan perundang-undangan di bidang pajak daerah dan retribusi daerah. 2. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, ditambahkan 1 (satu) ayat, yakni ayat (4), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Tarif Pajak Pertambahan Nilai yaitu: a. sebesar 11% (sebelas persen) yang mulai berlaku pada tanggal 1 April 2022; b. sebesar 12% (dua belas persen) yang mulai berlaku paling lambat pada tanggal 1 Januari 2025. (2) Tarif Pajak Pertambahan Nilai sebesar 0% (nol persen) diterapkan atas: a. ekspor Barang Kena Pajak Berwujud; b. ekspor Barang Kena Pajak Tidak Berwujud; dan c. ekspor Jasa Kena Pajak. (3) Tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (1) dapat diubah menjadi paling rendah 5% (lima persen) dan paling tinggi 15% (lima belas persen). (4) Perubahan tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah setelah disampaikan oleh Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. 3. Ketentuan Pasal 8A ayat (2) dihapus, dan ditambahkan 1 (satu) ayat, yakni ayat (3) sehingga Pasal 8A berbunyi sebagai berikut: Pasal 8A (1) Pajak Pertambahan Nilai yang terutang dihitung dengan cara mengalikan tarif sebagaimana dimaksud dalam Pasal 7 dengan Dasar Pengenaan Pajak yang meliputi

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## m01 · multi_hop · ⬜ BELUM
**Pertanyaan:** Kebijakan pajak apa saja dalam UU HPP yang sama-sama mulai berlaku pada 1 April 2022?

**Jawaban referensi:** PPN 11% [Pasal 7 ayat (1) huruf a UU PPN jo. UU HPP] dan pajak karbon untuk PLTU batubara [Pasal 17 ayat (3) UU HPP] sama-sama berlaku mulai 1 April 2022.

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0068`

<details>
<summary>uu-hpp-2021-bt:0068 (hlm. 74-75)</summary>

daerah; o. dihapus; p. dihapus; dan q. jasa boga atau katering, meliputi semua kegiatan pelayanan penyediaan makanan dan minuman yang merupakan objek pajak daerah dan retribusi daerah sesuai dengan ketentuan peraturan perundang-undangan di bidang pajak daerah dan retribusi daerah. 2. Ketentuan ayat (1) dan ayat (3) Pasal 7 diubah, ditambahkan 1 (satu) ayat, yakni ayat (4), serta penjelasan ayat (2) Pasal 7 diubah sebagaimana tercantum dalam penjelasan pasal demi pasal sehingga Pasal 7 berbunyi sebagai berikut: Pasal 7 (1) Tarif Pajak Pertambahan Nilai yaitu: a. sebesar 11% (sebelas persen) yang mulai berlaku pada tanggal 1 April 2022; b. sebesar 12% (dua belas persen) yang mulai berlaku paling lambat pada tanggal 1 Januari 2025. (2) Tarif Pajak Pertambahan Nilai sebesar 0% (nol persen) diterapkan atas: a. ekspor Barang Kena Pajak Berwujud; b. ekspor Barang Kena Pajak Tidak Berwujud; dan c. ekspor Jasa Kena Pajak. (3) Tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (1) dapat diubah menjadi paling rendah 5% (lima persen) dan paling tinggi 15% (lima belas persen). (4) Perubahan tarif Pajak Pertambahan Nilai sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah setelah disampaikan oleh Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. 3. Ketentuan Pasal 8A ayat (2) dihapus, dan ditambahkan 1 (satu) ayat, yakni ayat (3) sehingga Pasal 8A berbunyi sebagai berikut: Pasal 8A (1) Pajak Pertambahan Nilai yang terutang dihitung dengan cara mengalikan tarif sebagaimana dimaksud dalam Pasal 7 dengan Dasar Pengenaan Pajak yang meliputi

</details>

**Fakta 2:** cukup salah satu dari `uu-hpp-2021-bt:0105`

<details>
<summary>uu-hpp-2021-bt:0105 (hlm. 112-114)</summary>

Lembaran Negara Republik Indonesia Nomor 6573), dinyatakan masih tetap berlaku sepanjang tidak bertentangan dengan ketentuan dalam Undang-Undang ini atau belum diganti berdasarkan Undang-Undang ini. Pasal 17 (1) Ketentuan sebagaimana dimaksud dalam Pasal 3 mulai berlaku pada Tahun Pajak 2022. (2) Ketentuan sebagaimana dimaksud dalam Pasal 4 mulai berlaku pada tanggal 1 April 2022. (3) Ketentuan sebagaimana dimaksud dalam Pasal 13 mulai berlaku pada tanggal 1 April 2022, yang pertama kali dikenakan terhadap badan yang bergerak di bidang pembangkit listrik tenaga uap batubara dengan tarif Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. Pasal 18 Ketentuan Pasal 5 ayat (1) huruf b Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan Untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 87, Tambahan Lembaran Negara Republik Indonesia Nomor 6485) yang telah ditetapkan menjadi Undang-Undang Nomor 2 Tahun 2020 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 134, Tambahan Lembaran Negara Republik Indonesia Nomor 6516), dicabut dan dinyatakan tidak berlaku. Pasal 19 Undang-Undang ini mulai berlaku pada tanggal diundangkan. Agar setiap orang mengetahuinya, memerintahkan pengundangan Undang-Undang ini dengan penempatannya dalam Lembaran

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## m02 · multi_hop · ⬜ BELUM
**Pertanyaan:** Bagaimana NIK digunakan sebagai NPWP dan siapa yang menyediakan data kependudukannya?

**Jawaban referensi:** NPWP WP orang pribadi penduduk Indonesia menggunakan NIK [Pasal 2 ayat (1a) UU KUP]; menteri urusan pemerintahan dalam negeri memberikan data kependudukan dan data balikan kepada Menkeu untuk integrasi basis data [Pasal 2 ayat (10) UU KUP jo. UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0005` **ATAU** `uu-hpp-2021-pjl:0007`

<details>
<summary>uu-hpp-2021-bt:0005 (hlm. 6-7)</summary>

49, Tambahan Lembaran Negara Republik Indonesia Nomor 3262) sebagaimana telah beberapa kali diubah terakhir dengan Undang-Undang Nomor 16 Tahun 2009 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 5 Tahun 2008 tentang Perubahan Keempat atas Undang-Undang Nomor 6 Tahun 1983 tentang Ketentuan Umum dan Tata Cara Perpajakan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2009 Nomor 62, Tambahan Lembaran Negara Republik Indonesia Nomor 4999) diubah sebagai berikut: 1. Di antara ayat (1) dan ayat (2) Pasal 2 disisipkan 1 (satu) ayat, yakni ayat (1a), Pasal 2 ayat (5) dihapus, serta ditambahkan 1 (satu) ayat, yakni ayat (10) sehingga Pasal 2 berbunyi sebagai berikut: Pasal 2 (1) Setiap Wajib Pajak yang telah memenuhi persyaratan subjektif dan objektif sesuai dengan ketentuan peraturan perundang-undangan perpajakan wajib mendaftarkan diri pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya meliputi tempat tinggal atau tempat kedudukan Wajib Pajak dan kepadanya diberikan Nomor Pokok Wajib Pajak. (1a) Nomor Pokok Wajib Pajak sebagaimana dimaksud pada ayat (1) bagi Wajib Pajak orang pribadi yang merupakan penduduk Indonesia menggunakan nomor induk kependudukan. (2) Setiap Wajib Pajak sebagai Pengusaha yang dikenai pajak berdasarkan Undang-Undang Pajak Pertambahan Nilai 1984 dan perubahannya, wajib melaporkan usahanya pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya meliputi tempat tinggal atau tempat kedudukan Pengusaha, dan tempat kegiatan usaha dilakukan untuk dikukuhkan menjadi Pengusaha Kena Pajak. (3) Direktur Jenderal Pajak dapat menetapkan: a. tempat pendaftaran dan/atau tempat pelaporan usaha selain yang ditetapkan pada ayat (1) dan ayat (2); dan/atau b. tempat pendaftaran pada kantor Direktorat Jenderal Pajak yang wilayah kerjanya

</details>

<details>
<summary>uu-hpp-2021-pjl:0007 (hlm. 7-9)</summary>

dari pemenuhan kewajiban perpajakan sesuai dengan ketentuan peraturan perundang-undangan perpajakan. Hal ini dimaksudkan untuk memberikan kepastian hukum kepada Wajib Pajak maupun Pemerintah berkaitan dengan kewajiban Wajib Pajak untuk mendaftarkan diri dan hak untuk memperoleh Nomor Pokok Wajib Pajak dan/atau dikukuhkan sebagai Pengusaha Kena Pajak, misalnya terhadap Wajib Pajak diterbitkan No. 6736 Nomor Pokok Wajib Pajak secara jabatan pada tahun 2008 dan ternyata Wajib Pajak telah memenuhi persyaratan subjektif dan objektif sesuai dengan ketentuan peraturan perundang-undangan perpajakan terhitung sejak tahun 2005, kewajiban perpajakannya timbul terhitung sejak tahun 2005. Ayat (5) Dihapus. Ayat (6) Cukup jelas. Ayat (7) Cukup jelas. Ayat (8) Cukup jelas. Ayat (9) Cukup jelas. Ayat (10) Penggunaan nomor induk kependudukan sebagai identitas Wajib Pajak orang pribadi memerlukan pengintegrasian basis data kependudukan dengan basis data perpajakan yang digunakan sebagai pembentuk profil Wajib Pajak, serta dapat digunakan oleh Wajib Pajak dalam rangka pelaksanaan hak dan/atau pemenuhan kewajiban perpajakannya. Data kependudukan dan data balikan dari pengguna merupakan data kependudukan dan data balikan dari pengguna sebagaimana diatur dalam peraturan perundang-undangan yang mengatur mengenai administrasi kependudukan. Angka 2 Pasal 8 Ayat (1) Terhadap kekeliruan dalam pengisian Surat Pemberitahuan yang dibuat oleh Wajib Pajak, Wajib Pajak masih berhak untuk melakukan pembetulan atas kemauan sendiri, dengan syarat Direktur Jenderal No. 6736 Pajak belum mulai melakukan tindakan pemeriksaan. Yang dimaksud dengan "mulai melakukan tindakan pemeriksaan" adalah pada saat Surat Pemberitahuan Pemeriksaan Pajak disampaikan kepada Wajib Pajak, wakil, kuasa, pegawai, atau anggota keluarga yang telah dewasa dari Wajib Pajak. Ayat (1a) Yang dimaksud dengan daluwarsa penetapan adalah

</details>

**Fakta 2:** cukup salah satu dari `uu-hpp-2021-bt:0007`

<details>
<summary>uu-hpp-2021-bt:0007 (hlm. 8-9)</summary>

persyaratan subjektif dan/atau objektif sesuai dengan ketentuan peraturan perundang-undangan perpajakan; b. Wajib Pajak badan dilikuidasi karena penghentian atau penggabungan usaha; c. Wajib Pajak bentuk usaha tetap menghentikan kegiatan usahanya di Indonesia; atau d. dianggap perlu oleh Direktur Jenderal Pajak untuk menghapuskan Nomor Pokok Wajib Pajak dari Wajib Pajak yang sudah tidak memenuhi persyaratan subjektif dan/atau objektif sesuai dengan ketentuan peraturan perundang-undangan perpajakan. (7) Direktur Jenderal Pajak setelah melakukan pemeriksaan harus memberikan keputusan atas permohonan penghapusan Nomor Pokok Wajib Pajak dalam jangka waktu 6 (enam) bulan untuk Wajib Pajak orang pribadi atau 12 (dua belas) bulan untuk Wajib Pajak badan, sejak tanggal permohonan diterima secara lengkap. (8) Direktur Jenderal Pajak karena jabatan atau atas permohonan Wajib Pajak dapat melakukan pencabutan pengukuhan Pengusaha Kena Pajak. (9) Direktur Jenderal Pajak setelah melakukan pemeriksaan harus memberikan keputusan atas permohonan pencabutan pengukuhan Pengusaha Kena Pajak dalam jangka waktu 6 (enam) bulan sejak tanggal permohonan diterima secara lengkap. (10) Dalam rangka penggunaan nomor induk kependudukan sebagai Nomor Pokok Wajib Pajak sebagaimana dimaksud pada ayat (1a), menteri yang menyelenggarakan urusan pemerintahan dalam negeri memberikan data kependudukan dan data balikan dari pengguna kepada Menteri Keuangan untuk diintegrasikan dengan basis data perpajakan. 2. Ketentuan ayat (4) Pasal 8 diubah sehingga berbunyi sebagai berikut: Pasal 8 (1) Wajib Pajak dengan kemauan sendiri dapat membetulkan Surat Pemberitahuan yang telah disampaikan dengan menyampaikan pernyataan tertulis dengan syarat Direktur Jenderal Pajak belum melakukan tindakan pemeriksaan. (1a) Dalam hal pembetulan Surat Pemberitahuan sebagaimana dimaksud pada ayat (1) menyatakan rugi atau lebih bayar, pembetulan Surat

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## m03 · multi_hop · ⬜ BELUM
**Pertanyaan:** Dalam program pengungkapan sukarela untuk harta perolehan 1985-2015, bandingkan tarif untuk harta di dalam negeri yang diinvestasikan pada SBN dengan harta di luar negeri yang tidak dialihkan ke Indonesia.

**Jawaban referensi:** Untuk harta perolehan 1985-2015 (Kebijakan I): harta dalam negeri yang diinvestasikan pada SBN/hilirisasi dikenai 6% [Pasal 5 ayat (7) huruf a UU HPP]; harta luar negeri yang tidak dialihkan ke dalam negeri dikenai 11% [Pasal 5 ayat (7) huruf e UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0082`

<details>
<summary>uu-hpp-2021-bt:0082 (hlm. 89-90)</summary>

sampai dengan tanggal 31 Desember 2015. (5) Harta bersih sebagaimana dimaksud pada ayat (1) dianggap sebagai tambahan penghasilan dan dikenai Pajak Penghasilan yang bersifat final. (6) Pajak Penghasilan yang bersifat final sebagaimana dimaksud pada ayat (5) dihitung dengan cara mengalikan tarif dengan dasar pengenaan pajak. (7) Tarif sebagaimana dimaksud pada ayat (6) ditetapkan sebesar: a. 6% (enam persen) atas harta bersih yang berada di dalam wilayah Negara Kesatuan Republik Indonesia, dengan ketentuan diinvestasikan pada: 1. kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau 2. surat berharga negara; b. 8% (delapan persen) atas harta bersih yang berada di dalam wilayah Negara Kesatuan Republik Indonesia dan tidak diinvestasikan pada: 1. kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau 2. surat berharga negara; c. 6% (enam persen) atas harta bersih yang berada di luar wilayah Negara Kesatuan Republik Indonesia, dengan ketentuan: 1. dialihkan ke dalam wilayah Negara Kesatuan Republik Indonesia; dan 2. diinvestasikan pada: a) kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau b) surat berharga negara; d. 8% (delapan persen) atas harta bersih yang berada di luar wilayah Negara Kesatuan Republik Indonesia dengan ketentuan: 1. dialihkan ke dalam wilayah Negara Kesatuan Republik Indonesia; dan 2. tidak diinvestasikan pada: a) kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau b)

</details>

**Fakta 2:** cukup salah satu dari `uu-hpp-2021-bt:0083`

<details>
<summary>uu-hpp-2021-bt:0083 (hlm. 90-91)</summary>

persen) atas harta bersih yang berada di luar wilayah Negara Kesatuan Republik Indonesia dengan ketentuan: 1. dialihkan ke dalam wilayah Negara Kesatuan Republik Indonesia; dan 2. tidak diinvestasikan pada: a) kegiatan usaha sektor pengolahan sumber daya alam atau sektor energi terbarukan di dalam wilayah Negara Kesatuan Republik Indonesia; dan/atau b) surat berharga negara; atau e. 11% (sebelas persen) atas harta bersih yang berada di luar wilayah Negara Kesatuan Republik Indonesia dan tidak dialihkan ke dalam wilayah Negara Kesatuan Republik Indonesia. (8) Dasar pengenaan pajak sebagaimana dimaksud pada ayat (6) yakni sebesar jumlah harta bersih yang belum atau kurang diungkapkan dalam surat pernyataan. (9) Nilai harta yang dijadikan pedoman untuk menghitung besarnya jumlah harta bersih sebagaimana dimaksud pada ayat (8) ditentukan berdasarkan: a. nilai nominal, untuk harta berupa kas atau setara kas; b. nilai yang ditetapkan oleh pemerintah yaitu Nilai Jual Objek Pajak, untuk tanah dan/atau bangunan dan Nilai Jual Kendaraan Bermotor, untuk kendaraan bermotor; c. nilai yang dipublikasikan oleh PT Aneka Tambang Tbk., untuk emas dan perak; d. nilai yang dipublikasikan oleh PT Bursa Efek Indonesia, untuk saham dan waran (warrant) yang diperjualbelikan di PT Bursa Efek Indonesia; dan/atau e. nilai yang dipublikasikan oleh PT Penilai Harga Efek Indonesia, untuk surat berharga negara dan efek bersifat utang dan/atau sukuk yang diterbitkan oleh perusahaan, sesuai kondisi dan keadaan harta pada akhir Tahun Pajak terakhir. (10) Dalam hal tidak terdapat nilai yang dapat dijadikan pedoman sebagaimana dimaksud pada ayat (9) huruf b sampai dengan huruf e, nilai harta ditentukan berdasarkan nilai dari

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## m04 · multi_hop · ⬜ BELUM
**Pertanyaan:** Berapa tarif minimum pajak karbon dan sektor apa yang pertama kali dikenakan?

**Jawaban referensi:** Tarif paling rendah Rp30/kg CO2e [Pasal 13 ayat (9) UU HPP]; pertama dikenakan pada PLTU batubara mulai 1 April 2022 [Pasal 17 ayat (3) UU HPP].

**Fakta 1:** cukup salah satu dari `uu-hpp-2021-bt:0097` **ATAU** `uu-hpp-2021-bt:0098`

<details>
<summary>uu-hpp-2021-bt:0097 (hlm. 104-105)</summary>

BAB VI PAJAK KARBON Pasal 13 (1) Pajak karbon dikenakan atas emisi karbon yang memberikan dampak negatif bagi lingkungan hidup. (2) Pengenaan pajak karbon sebagaimana dimaksud pada ayat (1) dilakukan dengan memperhatikan: a. peta jalan pajak karbon; dan/atau b. peta jalan pasar karbon. (3) Peta jalan pajak karbon sebagaimana dimaksud pada ayat (2) huruf a memuat: a. strategi penurunan emisi karbon; b. sasaran sektor prioritas; c. keselarasan dengan pembangunan energi baru dan terbarukan; dan/atau d. keselarasan antarberbagai kebijakan lainnya. (4) Kebijakan peta jalan pajak karbon sebagaimana dimaksud pada ayat (3) ditetapkan oleh Pemerintah dengan persetujuan Dewan Perwakilan Rakyat Republik Indonesia. (5) Subjek pajak karbon yaitu orang pribadi atau badan yang membeli barang yang mengandung karbon dan/atau melakukan aktivitas yang menghasilkan emisi karbon. (6) Pajak karbon terutang atas pembelian barang yang mengandung karbon atau aktivitas yang menghasilkan emisi karbon dalam jumlah tertentu pada periode tertentu. (7) Saat terutang pajak karbon ditentukan: a. pada saat pembelian barang yang mengandung karbon; b. pada akhir periode tahun kalender dari aktivitas yang menghasilkan emisi karbon dalam jumlah tertentu; atau c. saat lain yang diatur dengan atau berdasarkan Peraturan Pemerintah. (8) Tarif pajak karbon ditetapkan lebih tinggi atau sama dengan harga karbon di pasar karbon per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (9) Dalam hal harga karbon di pasar karbon sebagaimana dimaksud pada ayat (8) lebih rendah dari Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara, tarif pajak karbon ditetapkan sebesar paling rendah Rp30,00 (tiga puluh rupiah)

</details>

<details>
<summary>uu-hpp-2021-bt:0098 (hlm. 105-106)</summary>

kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (9) Dalam hal harga karbon di pasar karbon sebagaimana dimaksud pada ayat (8) lebih rendah dari Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara, tarif pajak karbon ditetapkan sebesar paling rendah Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. (10) Ketentuan mengenai: a. penetapan tarif pajak karbon sebagaimana dimaksud pada ayat (8); b. perubahan tarif pajak karbon sebagaimana dimaksud pada ayat (9); dan/atau c. dasar pengenaan pajak, diatur dengan Peraturan Menteri Keuangan setelah dikonsultasikan dengan Dewan Perwakilan Rakyat Republik Indonesia. (11) Ketentuan mengenai penambahan objek pajak yang dikenai pajak karbon sebagaimana dimaksud pada ayat (1) diatur dengan atau berdasarkan Peraturan Pemerintah setelah disampaikan Pemerintah kepada Dewan Perwakilan Rakyat Republik Indonesia untuk dibahas dan disepakati dalam penyusunan Rancangan Anggaran Pendapatan dan Belanja Negara. (12) Penerimaan dari pajak karbon dapat dialokasikan untuk pengendalian perubahan iklim. (13) Wajib Pajak yang berpartisipasi dalam perdagangan emisi karbon, pengimbangan emisi karbon, dan/atau mekanisme lain sesuai peraturan perundang- undangan di bidang lingkungan hidup dapat diberikan: a. pengurangan pajak karbon; dan/atau b. perlakuan lainnya atas pemenuhan kewajiban pajak karbon. (14) Ketentuan mengenai: a. tata cara penghitungan, pemungutan, pembayaran atau penyetoran, pelaporan, dan mekanisme pengenaan pajak karbon; dan b. tata cara pengurangan pajak karbon sebagaimana dimaksud pada ayat (13) huruf a dan/atau perlakuan lainnya atas pemenuhan kewajiban pajak karbon sebagaimana dimaksud pada ayat (13) huruf b, diatur dengan Peraturan Menteri Keuangan. (15) Ketentuan mengenai: a. subjek pajak karbon

</details>

**Fakta 2:** cukup salah satu dari `uu-hpp-2021-bt:0105`

<details>
<summary>uu-hpp-2021-bt:0105 (hlm. 112-114)</summary>

Lembaran Negara Republik Indonesia Nomor 6573), dinyatakan masih tetap berlaku sepanjang tidak bertentangan dengan ketentuan dalam Undang-Undang ini atau belum diganti berdasarkan Undang-Undang ini. Pasal 17 (1) Ketentuan sebagaimana dimaksud dalam Pasal 3 mulai berlaku pada Tahun Pajak 2022. (2) Ketentuan sebagaimana dimaksud dalam Pasal 4 mulai berlaku pada tanggal 1 April 2022. (3) Ketentuan sebagaimana dimaksud dalam Pasal 13 mulai berlaku pada tanggal 1 April 2022, yang pertama kali dikenakan terhadap badan yang bergerak di bidang pembangkit listrik tenaga uap batubara dengan tarif Rp30,00 (tiga puluh rupiah) per kilogram karbon dioksida ekuivalen (CO2e) atau satuan yang setara. Pasal 18 Ketentuan Pasal 5 ayat (1) huruf b Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan Untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 87, Tambahan Lembaran Negara Republik Indonesia Nomor 6485) yang telah ditetapkan menjadi Undang-Undang Nomor 2 Tahun 2020 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 1 Tahun 2020 tentang Kebijakan Keuangan Negara dan Stabilitas Sistem Keuangan untuk Penanganan Pandemi Corona Virus Disease 2019 (COVID-19) dan/atau Dalam Rangka Menghadapi Ancaman yang Membahayakan Perekonomian Nasional dan/atau Stabilitas Sistem Keuangan Menjadi Undang-Undang (Lembaran Negara Republik Indonesia Tahun 2020 Nomor 134, Tambahan Lembaran Negara Republik Indonesia Nomor 6516), dicabut dan dinyatakan tidak berlaku. Pasal 19 Undang-Undang ini mulai berlaku pada tanggal diundangkan. Agar setiap orang mengetahuinya, memerintahkan pengundangan Undang-Undang ini dengan penempatannya dalam Lembaran

</details>

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## u01 · unanswerable · ⬜ BELUM
**Pertanyaan:** Berapa tarif pajak kendaraan bermotor tahunan untuk mobil pribadi?

**Jawaban referensi:** Tidak ditemukan di dokumen — pajak kendaraan bermotor diatur UU PDRD/UU HKPD, bukan UU HPP.

_(unanswerable — tidak ada chunk; cek bahwa korpus memang tak menjawab)_

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## u02 · unanswerable · ⬜ BELUM
**Pertanyaan:** Berapa denda keterlambatan pembayaran Pajak Bumi dan Bangunan?

**Jawaban referensi:** Tidak ditemukan di dokumen — ketentuan PBB tidak diatur dalam UU HPP.

_(unanswerable — tidak ada chunk; cek bahwa korpus memang tak menjawab)_

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## u03 · unanswerable · ⬜ BELUM
**Pertanyaan:** Apakah UU HPP mengatur besaran iuran BPJS Kesehatan?

**Jawaban referensi:** Tidak ditemukan di dokumen — iuran BPJS bukan materi UU HPP.

_(unanswerable — tidak ada chunk; cek bahwa korpus memang tak menjawab)_

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)

---
## u04 · unanswerable · ⬜ BELUM
**Pertanyaan:** Berapa tarif bea masuk untuk impor mobil listrik?

**Jawaban referensi:** Tidak ditemukan di dokumen — bea masuk diatur UU Kepabeanan, bukan UU HPP.

_(unanswerable — tidak ada chunk; cek bahwa korpus memang tak menjawab)_

- [ ] pertanyaan wajar & tidak ambigu
- [ ] SEMUA chunk di tiap grup benar-benar memuat faktanya
- [ ] jawaban referensi akurat (angka, pasal, ayat)
