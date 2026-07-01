import cv2
from easyocr import Reader

# Inisialisasi EasyOCR Reader untuk bahasa Inggris sekali saja pada CPU (Aman untuk Windows)
reader = Reader(['en'], gpu=False)

def read(img):
    """
    Membaca teks langsung dari area boks seleksi dinamis yang diatur oleh user.
    Tanpa auto-crop tambahan agar akurat sesuai posisi boks di layar.
    """
    if img is None or img.size == 0:
        return ""
        
    try:
        # 1. Ubah gambar ke Hitam Putih (Grayscale)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 2. Perbesar skala gambar 2x agar font teks game yang kecil terbaca lebih tajam oleh AI
        gray = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        
        # 3. Thresholding otomatis (Otsu Binarization) untuk memisahkan teks dari background box game
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 4. Jalankan OCR dengan optimasi kecepatan CPU tanpa bikin crash di Windows
        result = reader.readtext(
            thresh, 
            detail=0, 
            paragraph=False,
            workers=0,             # Wajib 0 di Windows agar tidak terjadi tabrakan proses background
            slope_ths=0.5,         # Mengabaikan pencarian teks miring (teks game selalu lurus)
            ycenter_ths=0.5,       # Mempercepat penggabungan potongan baris kalimat
            height_ths=0.5         # Mempercepat pembacaan tinggi ukuran huruf
        )

        # 5. Gabungkan hasil pembacaan potongan kata menjadi satu kalimat utuh yang bersih
        text = " ".join(result)
        return " ".join(text.split()).strip()

    except Exception as e:
        print("OCR Engine Error:", e)
        return ""