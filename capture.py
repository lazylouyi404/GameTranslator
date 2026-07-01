import mss
import numpy as np
import cv2

def capture(region):
    """
    Mengambil tangkapan layar (screenshot) berdasarkan koordinat tuple (x, y, w, h)
    yang dikirim secara dinamis dari pergerakan boks overlay.
    """
    try:
        # Ekstrak data tuple angka dari posisi boks overlay saat ini
        x, y, w, h = region

        # Format untuk library mss harus berupa dictionary dengan nama key yang sesuai
        monitor = {
            "top": int(y),
            "left": int(x),
            "width": int(w),
            "height": int(h)
        }

        with mss.mss() as sct:
            # Ambil screenshot di area boks tersebut
            screenshot = sct.grab(monitor)
            
            # Ubah format gambar mss menjadi numpy array agar bisa diolah OpenCV (BGR)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img

    except Exception as e:
        print("Capture Error:", e)
        return None