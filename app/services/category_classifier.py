from app.config.settings import CATEGORY_RULES

def classify_category(product: str):
    p = product.lower() if product else ""

    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in p:
                return category

    return "misc"