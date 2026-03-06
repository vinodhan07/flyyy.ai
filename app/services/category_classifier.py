# ─── Category Classification ───
from app.config.settings import CATEGORY_RULES


def classify_category(product: str) -> str:
    """Classify a product string into a category based on keyword rules."""
    text = product.lower() if product else ""

    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in text:
                return category

    return "misc"