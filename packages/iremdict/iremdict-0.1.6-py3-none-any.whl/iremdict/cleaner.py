import os
import re

def load_words():
    path = os.path.join(os.path.dirname(__file__), "data", "sozluk.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def clean_text(text, word_list):
    multi_words = [w for w in word_list if " " in w]
    single_words = [w for w in word_list if " " not in w]

    placeholder_map = {}
    for i, phrase in enumerate(sorted(multi_words, key=len, reverse=True)):
        if phrase in text:
            placeholder = f"__PHRASE_{i}__"
            text = text.replace(phrase, placeholder)
            placeholder_map[placeholder] = phrase

    tokens = re.findall(r'\b\w+\b|__PHRASE_\d+__', text)

    result_tokens = []
    for token in tokens:
        if token.startswith("__PHRASE_"):
            result_tokens.append(token)
        else:
            matched = False
            for root in single_words:
                if root in token:
                    result_tokens.append(root)
                    matched = True
                    break
            if not matched:
                continue

    cleaned = ' '.join(result_tokens)
    for ph, phrase in placeholder_map.items():
        cleaned = cleaned.replace(ph, phrase)

    return cleaned
