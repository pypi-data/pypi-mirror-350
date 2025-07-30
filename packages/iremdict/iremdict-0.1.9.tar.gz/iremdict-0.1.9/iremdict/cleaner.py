import os
import re

def load_words():
    path = os.path.join(os.path.dirname(__file__), "data", "sozluk.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def clean_text(text, word_list):
    # Çok kelimelileri ayrı tut
    multi_words = [w for w in word_list if " " in w]
    single_words = [w for w in word_list if " " not in w]

    # Çoklu kelimeleri korumak için geçici placeholder
    placeholder_map = {}
    for i, phrase in enumerate(sorted(multi_words, key=len, reverse=True)):
        if phrase in text:
            placeholder = f"__PHRASE_{i}__"
            text = text.replace(phrase, placeholder)
            placeholder_map[placeholder] = phrase

    # Token'lara böl
    tokens = re.findall(r'\b\w+\b|__PHRASE_\d+__', text)

    result_tokens = []

    for token in tokens:
        if token.startswith("__PHRASE_"):
            result_tokens.append(token)
        else:
            matched = False

            # 1. Tam eşleşme varsa doğrudan al
            if token in single_words:
                result_tokens.append(token)
                matched = True
            else:
                # 2. En uzun eşleşmeyi bulana kadar kırp
                for i in range(len(token) - 1, 0, -1):
                    partial = token[:i]
                    if partial in single_words:
                        result_tokens.append(partial)  # sadece kökü tut
                        matched = True
                        break

            # 3. Eğer eşleşme yoksa token'ı atla (continue)
            if not matched:
                continue

    # Placeholder'ları geri al
    cleaned = ' '.join(result_tokens)
    for ph, phrase in placeholder_map.items():
        cleaned = cleaned.replace(ph, phrase)

    return cleaned
