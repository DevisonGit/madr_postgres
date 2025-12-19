def sanitize_string(word: str) -> str:
    sanitize_word = ' '.join(word.lower().strip().split())
    return sanitize_word
