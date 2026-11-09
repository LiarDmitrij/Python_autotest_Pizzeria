import re


def clean(text):
    return re.sub(r'[«»""„“”]', '', text).strip()