from .config import CATEGORIES

def get_category(filename: str) -> str:
    fn = filename.lower()
    for cat, keys in CATEGORIES.items():
        if any(k in fn for k in keys):
            return cat
    return "other"