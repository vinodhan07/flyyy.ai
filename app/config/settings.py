# ─── Centralized Configuration ───
from typing import Dict, List

# ─── Header Detection ───
HEADER_SCAN_LIMIT = 20

HEADER_KEYWORDS = [
    "description",
    "item",
    "material",
    "equipment",
    "qty",
    "quantity",
    "unit",
    "rate",
    "amount"
]

# ─── Row Filtering ───
SECTION_KEYWORDS = [
    "building",
    "hall",
    "laboratory",
    "room",
    "area"
]

INVALID_ROW_KEYWORDS = [
    "total",
    "subtotal",
    "grand total",
    "note",
    "remarks"
]

# ─── Extraction Limits ───
MAX_PRODUCT_LENGTH = 150
MAX_REASONABLE_QUANTITY = 1000

# ─── Category Rules ───
CATEGORY_RULES = {
    "switchgear": ["breaker", "rmu"],
    "power_equipment": ["transformer", "dg set", "substation"],
    "electrical_panel": ["panel", "distribution"],
    "electrical_appliance": ["fan", "light", "sensor", "ups"]
}

# ─── Industry Configs ───
INDUSTRY_CONFIGS: Dict[str, Dict] = {
    "construction": {
        "table_detection_keywords": ["description", "item", "equipment", "sl no", "particulars"],
        "field_mapping": {
            "product": ["description", "item name", "equipment", "particulars", "item"],
            "brand": ["brand", "make", "manufacturer"],
            "quantity": ["qty", "quantity", "nos"],
            "category": ["category", "group", "system"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    },
    "retail": {
        "table_detection_keywords": ["sku", "product", "stock", "upc", "barcode"],
        "field_mapping": {
            "product": ["product name", "item description", "sku name"],
            "brand": ["brand", "manufacturer", "label"],
            "quantity": ["stock level", "count", "remaining", "inventory"],
            "category": ["department", "aisle", "section"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    },
    "default": {
        "table_detection_keywords": ["item", "qty", "description"],
        "field_mapping": {
            "product": ["item", "description"],
            "brand": ["brand", "make"],
            "quantity": ["qty", "quantity"],
            "category": ["category"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    }
}

DEFAULT_INDUSTRY = "construction"


def get_config(industry: str = DEFAULT_INDUSTRY) -> Dict:
    return INDUSTRY_CONFIGS.get(industry, INDUSTRY_CONFIGS["default"])
