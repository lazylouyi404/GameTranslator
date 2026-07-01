"""
Script sekali-pakai untuk membersihkan entri sampah dari dictionary.json
(entri yang valuenya sama persis dengan key, tanda translate gagal/percuma
yang sempat ke-cache sebelum perbaikan translator.py).

Cara pakai:
    python clean_dictionary.py dictionary.json
"""

import json
import sys


def clean(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    before = len(data)
    removed = []

    cleaned = {}
    for k, v in data.items():
        if v.strip().lower() == k.strip().lower():
            removed.append(k)
            continue
        cleaned[k] = v

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=4)

    print(f"Total entri sebelum : {before}")
    print(f"Entri dihapus       : {len(removed)}")
    print(f"Total entri sesudah : {len(cleaned)}")

    if removed:
        print("\nEntri yang dihapus:")
        for r in removed:
            print(f"  - {r}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "dictionary.json"
    clean(path)