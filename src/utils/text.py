import re


def clean(text):
    return re.sub(r'[«»""„“”]', '', text).strip()


def parse_price(text):
    """Извлекает число из строки цены: '115,00₽' -> 115.0."""
    cleaned = (
        text.replace("\u00a0", "")
        .replace(" ", "")
        .replace("₽", "")
        .replace(",", ".")
    )
    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    return float(match.group()) if match else None
