# 🎮 GameTranslator

GameTranslator adalah aplikasi penerjemah otomatis yang membantu Anda memahami dialog atau teks dalam game berbahasa Inggris ke bahasa Indonesia secara instan langsung di layar.

## 🚀 Cara Menjalankan (Panduan Cepat)

Ikuti langkah-langkah di bawah ini agar GameTranslator bisa berjalan di komputer Anda:

### 1. Persiapan Awal
Pastikan Anda sudah menginstal Python di komputer. Saat proses instalasi Python, pastikan Anda mencentang pilihan "Add Python to PATH" agar GameTranslator bisa berjalan dengan lancar.

### 2. Instalasi Pendukung
1. Unduh seluruh folder GameTranslator ke komputer Anda.
2. Buka folder tersebut, lalu klik kanan di area kosong dan pilih "Open in Terminal" atau "Open PowerShell".
3. Masukkan perintah berikut dan tekan Enter:
   pip install -r requirements.txt
   (Perintah ini akan secara otomatis mengunduh semua alat yang dibutuhkan agar GameTranslator bisa bekerja.)

### 3. Cara Memulai
1. Jalankan game Anda dalam mode jendela (windowed mode) agar GameTranslator bisa tampil di atas game.
2. Di jendela terminal yang sama, ketik perintah berikut untuk memulai GameTranslator:
   python main.py
3. Kotak transparan (overlay) akan muncul di layar. Anda bisa menggesernya dengan mouse dan menaruhnya tepat di atas teks game yang ingin diterjemahkan.

## 💡 Tips Penting
* Jika terjadi error: Pastikan aplikasi Tesseract OCR sudah terinstal di komputer Anda. GameTranslator membutuhkannya untuk "membaca" tulisan di layar.
* Mengatur Tesseract: Jika GameTranslator tidak jalan, buka file main.py dan pastikan lokasi tesseract.exe sudah sesuai dengan folder instalasi di komputer Anda.
* Butuh Bantuan: Jika GameTranslator berhenti, buka file debug_log.txt untuk melihat catatan masalah yang terjadi.

## ☕ Dukungan
Jika GameTranslator membantu pengalaman bermain game Anda, dukung pengembangan lebih lanjut melalui:
* https://saweria.co/lazylouyi404
