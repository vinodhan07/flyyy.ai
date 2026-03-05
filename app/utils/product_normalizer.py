from rapidfuzz import fuzz

SIMILARITY_THRESHOLD = 85

def normalize_products(items):
    normalized = []

    for item in items:
        found = False
        
        # Check if item is dict or object (since it could be ExtractedItem)
        is_dict = isinstance(item, dict)
        item_product = item["product"] if is_dict else getattr(item, "product", "")
        item_quantity = item["quantity"] if is_dict else getattr(item, "quantity", 0)

        for existing in normalized:
            existing_product = existing["product"] if is_dict else getattr(existing, "product", "")
            
            score = fuzz.ratio(
                str(item_product).lower(),
                str(existing_product).lower()
            )

            if score >= SIMILARITY_THRESHOLD:
                if is_dict:
                    existing["quantity"] += item_quantity
                else:
                    existing.quantity += item_quantity
                found = True
                break

        if not found:
            if is_dict:
                normalized.append(item.copy())
            else:
                import copy
                normalized.append(copy.deepcopy(item))

    return normalized
