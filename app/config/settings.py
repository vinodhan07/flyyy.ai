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
MAX_PRODUCT_LENGTH = 200  # Raised slightly to allow merged descriptions
MAX_REASONABLE_QUANTITY = 999999  # No practical upper limit — large civil quantities are valid

# ─── Engineering Attribute Ignore Words ───
# NOTE: 'total'/'subtotal' are NOT here — they're in INVALID_ROW_KEYWORDS
IGNORE_WORDS = [
    "floor", "depth", "nominal", "dia",
    "from", "upto", "schedule",
    "as per", "refer", "drawing"
]

# ─── Regex Patterns for Attribute Lines ───
DIMENSION_PATTERN = r"^\s*\d+\s*(mm|cm|m|sq\.?mm)"
DEPTH_PATTERN = r"\d+(\.\d+)?\s*m\s*depth"

# ─── EPC Material Classification Keywords ───
EPC_CATEGORY_RULES = {
    "Electrical": [
        "switch", "socket", "mcb", "isolator",
        "earthing", "charger", "junction",
        "transformer", "dg set", "substation",
        "switchgear", "breaker", "ups"
    ],
    "Plumbing": [
        "pipe", "valve", "tap", "cock",
        "pump", "chilled water", "drain", "water supply"
    ],
    "Lighting": [
        "light", "lamp", "led", "downlight",
        "tube", "flood", "bulkhead", "lighting"
    ],
    "Cable & Wiring": [
        "cable", "wire", "conduit",
        "tray", "xlpe", "armoured", "wiring"
    ],
    "Panels": [
        "panel", "distribution board",
        "rmu", "ht panel", "lt panel", "control panel"
    ],
    "Civil materials": [
        "cement", "sand", "brick",
        "aggregate", "concrete",
        "bitumen", "steel", "reinforcement"
    ],
    "Fixtures": [
        "lift", "elevator", "fan",
        "mirror", "dryer", "holder",
        "sensor", "fixture"
    ]
}

# ─── Material Keyword Validation ───
# Only keep rows that contain at least one of these real-material words
MATERIAL_KEYWORDS = [
    # Electrical
    "cable", "wire", "conduit", "tray", "xlpe", "armoured", "wiring",
    "switch", "socket", "mcb", "isolator", "earthing", "charger", "junction",
    "transformer", "breaker", "ups", "dg set", "substation", "switchgear",
    "distribution board", "rmu", "panel", "busbar", "contactor", "relay",
    "fuse", "meter", "capacitor", "inverter", "rectifier",
    # Lighting
    "light", "lamp", "led", "downlight", "tube", "flood", "bulkhead",
    "lighting", "luminaire", "spotlight", "streetlight", "lantern",
    # Plumbing / HVAC
    "pipe", "valve", "tap", "cock", "pump", "chilled water", "drain",
    "water supply", "fitting", "coupling", "flange", "elbow", "tee",
    "reducer", "hanger", "support", "clamp", "bracket", "strainer",
    "duct", "insulation", "grille", "diffuser", "damper", "ahu", "fcu",
    # Vertical transport
    "lift", "elevator", "escalator",
    # Fixtures & fittings
    "fan", "sensor", "fixture", "holder", "dryer", "mirror",
    "toilet", "basin", "urinal", "cistern", "shower",
    # Civil / structural
    "cement", "sand", "brick", "aggregate", "concrete", "bitumen",
    "steel", "reinforcement", "rebar", "rod", "bar", "mesh", "fiber",
    "formwork", "shutter", "waterproofing", "sealant", "grout",
    "paint", "plaster", "gypsum", "tile", "granite", "marble",
    "flooring", "coping", "cladding", "curtain wall", "glazing",
    "bolt", "anchor", "screw", "nut", "washer",
    # Misc structural
    "beam", "column", "slab", "footing", "raft", "pile", "truss",
    "purlin", "rafter", "gutter", "roof", "metal deck",
]

# ─── Industry Configs ───
INDUSTRY_CONFIGS: Dict[str, Dict] = {
    "construction": {
        "table_detection_keywords": ["description", "item", "equipment", "sl no", "particulars"],
        "field_mapping": {
            "description": ["description", "item name", "equipment", "particulars", "item"],
            "brand": ["brand", "make", "manufacturer"],
            "quantity": ["qty", "quantity", "nos"],
            "unit": ["unit", "uom", "measurement"],
            "category": ["category", "group", "system"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    },
    "retail": {
        "table_detection_keywords": ["sku", "product", "stock", "upc", "barcode"],
        "field_mapping": {
            "description": ["product name", "item description", "sku name"],
            "brand": ["brand", "manufacturer", "label"],
            "quantity": ["stock level", "count", "remaining", "inventory"],
            "unit": ["unit", "pkg", "size"],
            "category": ["department", "aisle", "section"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    },
    "default": {
        "table_detection_keywords": ["item", "qty", "description"],
        "field_mapping": {
            "description": ["item", "description"],
            "brand": ["brand", "make"],
            "quantity": ["qty", "quantity"],
            "unit": ["unit"],
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
