import os

def load_words():
    """
    data/sozluk.txt dosyasından kelime sözlüğünü yükler.
    """
    path = os.path.join(os.path.dirname(__file__), "data", "sozluk.txt")
    with open(path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f.readlines()]
    return words

def clean_text(text, word_list):
    sorted_words = sorted(word_list, key=lambda x: len(x.split()), reverse=True)

    phrase_map = {}
    phrase_id = 0
    for phrase in sorted_words:
        if " " in phrase and phrase in text:
            placeholder = f"__PHRASE_{phrase_id}__"
            text = text.replace(phrase, placeholder)
            phrase_map[placeholder] = phrase
            phrase_id += 1

    words = text.split()
    new_words = []

    for w in words:
        if w.startswith("__PHRASE_"):
            new_words.append(w)
            continue

        matched = False
        for dict_word in sorted_words:
            if " " not in dict_word and dict_word in w:
                new_words.append(dict_word)
                matched = True
                break
        if not matched:
            continue

    cleaned_text = ' '.join(new_words)
    for placeholder, phrase in phrase_map.items():
        cleaned_text = cleaned_text.replace(placeholder, phrase)

    return cleaned_text
