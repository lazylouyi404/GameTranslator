import sys, threading, time, pytesseract, cv2, numpy as np
import re, os
from PIL import ImageGrab
from PyQt6.QtWidgets import QApplication
from overlay import OCRSelector, TranslationDisplay, ScreenToggleButton
from control import ControlPanel
from translator import translate

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

LOG_FILE = "debug_log.txt"

# Kamus kata pendek & kata valid umum untuk mencegah kata gantung terjemahan
VALID_SHORT_WORDS = {
    'i', 'a', 'an', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'do', 'did', 'does',
    'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'from', 'up', 'out', 'as', 'if',
    'it', 'its', 'he', 'she', 'we', 'they', 'you', 'my', 'me', 'us', 'him', 'them', 'our',
    'no', 'not', 'oh', 'yes', 'ah', 'hey', 'so', 'go', 'get', 'see', 'but', 'and', 'or',
    'the', 'this', 'that', 'here', 'there', 'who', 'what', 'how', 'why', 'can', 'will',
    'dave', 'bancho', 'hans', 'yoshie', 'cobra', 'suwam', 'sea', 'fish', 'boat', 'rock',
    'we', 'as', 'out', 'off', 'but', 'now', 'then', 'back', 'old', 'get', 'got', 'our'
}

def write_to_log(box_name, raw_ocr, translated):
    """Mencatat aktivitas OCR ke file teks dan terminal demi kemudahan debug"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"==================================================\n"
        f"[{timestamp}] - TARGET: {box_name}\n"
        f"--------------------------------------------------\n"
        f"RAW OCR (English)   : {raw_ocr}\n"
        f"TRANSLATED (Indo)   : \n{translated}\n"
        f"==================================================\n\n"
    )
    print(log_entry.strip())
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except:
        pass

def format_game_text(raw_text):
    """Memecah teks OCR panjang boks misi menjadi baris-baris berstruktur rapi"""
    cleaned = re.sub(r'[\(\[\{] ?[01L]? ?[\)\]\}]', '', raw_text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    patterns = [
        (r'(?i)\b(Find Sea People|Find)\b', '\n◽ Find Sea People'),
        (r'(?i)\b(A Scolding from Yoshie|Scolding)\b', '\n📌 A Scolding from Yoshie'),
        (r'(?i)\b(Serve Whole-Roasted|Serve|WholeRoasted)\b', '\n◽ Serve Whole-Roasted')
    ]
    
    structured_text = cleaned
    for pattern, replacement in patterns:
        structured_text = re.sub(pattern, replacement, structured_text)
        
    if structured_text and not structured_text.startswith('📌') and not structured_text.startswith('◽'):
        structured_text = "📌 " + structured_text

    lines = structured_text.split('\n')
    translated_lines = []
    
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
            
        prefix = ""
        if line_str.startswith("📌"):
            prefix = "⚠️ "
            line_content = line_str.replace("📌", "").strip()
        elif line_str.startswith("◽"):
            prefix = "⬜ "
            line_content = line_str.replace("◽", "").strip()
        else:
            line_content = line_str
            
        translated_content = translate(line_content)
        translated_content = re.sub(r'(?i)\b(70m|70)\b', '(70m)', translated_content)
        translated_lines.append(f"{prefix}{translated_content}")
        
    return "\n".join(translated_lines)

def clean_ocr_text(text):
    """Membersihkan jeda baris dan memotong kata gantung rusak di akhir akibat animasi pengetikan"""
    text = text.replace('\n', ' ')
    text = re.sub(r'[^a-zA-Z0-9\s.,!?\'\"-() ]', '', text)
    cleaned = ' '.join(text.split()).strip()
    
    words = cleaned.split()
    if len(words) > 1:
        last_word = words[-1]
        clean_last = re.sub(r'[^a-zA-Z]', '', last_word).lower()
        
        # Aturan Cegah Kata Gantung: Jika kata terakhir pendek (<= 4 huruf), bukan angka,
        # dan tidak ada di kamus kata utuh kita, asumsikan itu potongan teks ngetik (seperti 'weap', 'sh')
        if len(clean_last) <= 4 and clean_last not in VALID_SHORT_WORDS and not last_word.isdigit():
            # Cek tanda baca akhir seperti titik/tanda seru. Jika tidak ada, fiks kata gantung.
            if not last_word.endswith(('.', '!', '?', '"', '...')):
                words.pop()
                cleaned = ' '.join(words).strip()
            
    return cleaned

def is_valid_dialog_text(text, strict_mode=False):
    """Filter super ketat Boks Biru (Dialog) untuk membabat habis teks sampah/halusinasi"""
    test_text = re.sub(r'\s+', ' ', text).strip()
    
    if not re.search(r'[aeiouAEIOU]', test_text):
        return False
        
    clean_words = re.sub(r'[^a-zA-Z\s]', '', test_text).split()
    word_count = len(clean_words)
    
    if word_count == 0:
        return False
        
    # Jika teks di bawah 3 kata, pastikan mengandung kosa kata dialog yang valid
    if word_count < 3:
        lower_text = test_text.lower().strip()
        valid_short_dialogs = {
            'oh', 'hahaha', 'haha', 'dave', 'bancho', 'cobra', 'hans', 'yoshie', 
            'yes', 'no', 'hey', 'what', 'who', 'why', 'how', 'wait', 'look', 'ah', 'i', 'you'
        }
        if not any(w in valid_short_dialogs for w in lower_text.split()):
            return False

    # Analisis Kepadatan Vokal (Vowel Density Check)
    total_chars = sum(len(w) for w in clean_words)
    vowels_count = sum(1 for c in "".join(clean_words).lower() if c in 'aeiou')
    if total_chars > 0:
        vowel_ratio = vowels_count / total_chars
        if vowel_ratio < 0.22 or vowel_ratio > 0.52: 
            return False

    # Filter kata tidak valid berdasarkan kamus mini
    invalid_words_count = 0
    for w in clean_words:
        if len(w) <= 4 and w.lower() not in VALID_SHORT_WORDS:
            invalid_words_count += 1
            
    if word_count <= 3 and invalid_words_count > 0:
        return False
    elif word_count > 3 and (invalid_words_count / word_count) > 0.30:
        return False
        
    return True

def is_valid_mission_text(text):
    """Filter khusus Boks Hijau (Misi): Hanya lolos jika mendeteksi keyword misi Dave the Diver"""
    cleaned_lower = text.lower()
    keywords = ['track', 'sea people', 'artifact', 'scold', 'yoshie', 'serve', 'shark', 'head', 'whole roasted']
    return any(kw in cleaned_lower for kw in keywords)

def optimize_image_for_handheld(img, is_green_box=True):
    """Memproses gambar agar teks game solid dan tidak pecah saat dibaca Tesseract"""
    if img is None or img.size == 0:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_large = cv2.resize(gray, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
    
    if not is_green_box:
        thresh = cv2.threshold(gray_large, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    else:
        thresh = cv2.threshold(gray_large, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def ocr_worker(selector, display, is_green_box=True):
    box_label = "Boks Hijau (Misi)" if is_green_box else "Boks Biru (Dialog)"
    last_valid_text = ""
    flicker_counter = 0  
    
    while True:
        try:
            x, y, w, h = selector.get_ocr_region()
            img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x, y, x+w, y+h))), cv2.COLOR_RGB2BGR)
            
            if img is not None and img.size > 0:
                thresh = optimize_image_for_handheld(img, is_green_box=is_green_box)
                
                if thresh is not None:
                    custom_config = '--psm 6'
                    raw_text = pytesseract.image_to_string(thresh, config=custom_config)
                    cleaned_text = clean_ocr_text(raw_text)
                    
                    is_passed = False
                    if is_green_box and len(cleaned_text) >= 10:
                        is_passed = is_valid_mission_text(cleaned_text)
                    elif not is_green_box and len(cleaned_text) >= 3:
                        is_strict = (last_valid_text == "TRANSPARENT")
                        is_passed = is_valid_dialog_text(cleaned_text, strict_mode=is_strict)
                    
                    if is_passed:
                        flicker_counter = 0 
                        
                        if cleaned_text == last_valid_text:
                            time.sleep(0.4)
                            continue
                            
                        if is_green_box:
                            formatted_translation = format_game_text(raw_text)
                            if formatted_translation:
                                display.text_received.emit(formatted_translation)
                                last_valid_text = cleaned_text
                                write_to_log(box_label, cleaned_text, formatted_translation)
                        else:
                            translated_text = translate(cleaned_text)
                            if translated_text:
                                display.text_received.emit(translated_text)
                                last_valid_text = cleaned_text
                                write_to_log(box_label, cleaned_text, translated_text)
                    else:
                        if not is_green_box:
                            flicker_counter += 1
                            if flicker_counter >= 3:
                                if last_valid_text != "TRANSPARENT":
                                    display.text_received.emit("") 
                                    last_valid_text = "TRANSPARENT"
                        else:
                            if last_valid_text != "TRANSPARENT":
                                display.text_received.emit("") 
                                last_valid_text = "TRANSPARENT"
        except Exception as e: 
            pass
        time.sleep(0.4)

if __name__ == "__main__":
    if os.path.exists(LOG_FILE):
        try: os.remove(LOG_FILE)
        except: pass

    app = QApplication(sys.argv)
    
    pairs = [
        {"selector": OCRSelector("green"), "display": TranslationDisplay("default")},
        {"selector": OCRSelector("blue"), "display": TranslationDisplay("blue")}
    ]
    
    def global_toggle_ocr():
        for p in pairs:
            p["selector"].toggle_visibility()

    handheld_btn = ScreenToggleButton(global_toggle_ocr)
    handheld_btn.show()
    
    for i, p in enumerate(pairs):
        p["selector"].show()
        p["display"].show()
        p["display"].move(450, 80 + (i * 120)) 
        
        is_green = (i == 0)
        threading.Thread(target=ocr_worker, args=(p["selector"], p["display"], is_green), daemon=True).start()
    
    ControlPanel(pairs).show()
    sys.exit(app.exec())