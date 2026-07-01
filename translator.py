import torch, json, os, re
from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-en-id"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
model.eval()

DICT_FILE = "dictionary.json"
def load_dict():
    if os.path.exists(DICT_FILE):
        try:
            with open(DICT_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: return {}
    return {}

dictionary = load_dict()
def save_dict():
    with open(DICT_FILE, 'w', encoding='utf-8') as f: json.dump(dictionary, f, ensure_ascii=False, indent=4)

def translate(text):
    text_clean = text.strip().lower()
    if text_clean in dictionary: return dictionary[text_clean]
    try:
        with torch.inference_mode():
            inputs = tokenizer(text_clean, return_tensors="pt")
            translated = model.generate(**inputs, max_new_tokens=64)
            result = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        result = re.sub(r'[^a-zA-Z0-9\s,!?]', '', result)
        result = ' '.join(result.split())
        dictionary[text_clean] = result
        save_dict() 
        return result
    except: return text