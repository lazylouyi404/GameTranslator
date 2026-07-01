# 🎮 GameTranslator

GameTranslator adalah aplikasi penerjemah otomatis yang membantu menerjemahkan dialog atau teks game berbahasa Inggris ke Bahasa Indonesia secara instan langsung di layar menggunakan OCR.

---

# 🚀 Cara Menjalankan

## 1. Persiapan

Pastikan **Python** sudah terinstal di komputer Anda.

> **Penting:** Saat menginstal Python, centang opsi **"Add Python to PATH"**.

---

## 2. Instalasi

Unduh atau clone seluruh folder **GameTranslator**.

Buka folder tersebut, lalu buka Terminal atau PowerShell di dalam folder.

Jalankan perintah berikut:

```bash
pip install -r requirements.txt
```

Perintah di atas akan menginstal seluruh library yang dibutuhkan.

---

## 3. Menjalankan Aplikasi

Jalankan game dalam **Windowed Mode** (mode jendela).

Kemudian jalankan:

```bash
python main.py
```

Setelah aplikasi berjalan, akan muncul **overlay transparan**.

Anda dapat:

- Menggeser overlay menggunakan mouse.
- Menempatkannya tepat di atas teks game.
- Teks yang terdeteksi akan diterjemahkan secara otomatis.

---

# 💡 Tips Penting

## Jika terjadi error

Pastikan **Tesseract OCR** sudah terinstal.

GameTranslator menggunakan Tesseract untuk membaca teks pada layar.

---

## Mengatur Lokasi Tesseract

Apabila aplikasi tidak dapat menemukan Tesseract, buka file:

```
main.py
```

Kemudian sesuaikan lokasi:

```
tesseract.exe
```

dengan folder instalasi Tesseract di komputer Anda.

Contoh:

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## Debug

Jika aplikasi mengalami masalah, buka file:

```
debug_log.txt
```

untuk melihat penyebab error.

---

# ☕ Dukungan

Jika GameTranslator membantu pengalaman bermain game Anda, Anda dapat mendukung pengembang melalui Saweria.

**Saweria:**
https://saweria.co/lazylouyi404

Terima kasih telah menggunakan **GameTranslator** ❤️
