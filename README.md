# GameTranslator

GameTranslator adalah aplikasi *real-time screen translator* yang dirancang khusus untuk membantu *gamer* PC maupun Handheld menerjemahkan teks dalam game secara instan ke bahasa Indonesia.

## Fitur Utama
* **Real-time Translation**: Menggunakan model AI Helsinki-NLP untuk menerjemahkan teks dari bahasa Inggris ke bahasa Indonesia secara cepat.
* **OCR Akurat**: Mendukung dua mesin OCR (Tesseract dan EasyOCR) dengan pemrosesan gambar yang dioptimalkan untuk teks berukuran kecil di game.
* **Sistem Caching**: Dilengkapi dengan dictionary.json untuk menyimpan hasil terjemahan kata yang sering muncul, sehingga proses menjadi jauh lebih cepat.
* **Mode Overlay**: Antarmuka berbasis PyQt6 yang ringan, memungkinkan Anda memilih area layar yang ingin dipantau dan melihat hasil terjemahan langsung di atas game.

## Persiapan
Sebelum menjalankan aplikasi, pastikan Anda telah menginstal:
1. **Python 3.x**
2. **Tesseract OCR** (Anda harus menginstalnya di sistem Windows agar modul pytesseract bisa berjalan).

## Cara Menjalankan
1. Clone repositori ini ke komputer Anda.
2. Masuk ke direktori proyek dan instal semua pustaka yang dibutuhkan:
   pip install -r requirements.txt
3. Jalankan aplikasi dengan perintah:
   python main.py

## Lisensi
Proyek ini dirilis di bawah lisensi **GNU GPL v3**. Anda bebas menggunakan dan memodifikasi kode sumber ini, dengan syarat harus tetap membagikan kode sumber untuk setiap distribusi aplikasi yang Anda lakukan.

## Dukungan
Jika aplikasi ini membantu pengalaman bermain game Anda, pertimbangkan untuk mendukung pengembangan lebih lanjut melalui:
* [https://saweria.co/lazylouyi404](https://saweria.co/lazylouyi404)