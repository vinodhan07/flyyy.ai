# ─── Text Cleaning & Row Validation Utilities ───
import re
from typing import Any

from app.config.settings import (
    INVALID_ROW_KEYWORDS,
    SECTION_KEYWORDS,
    MAX_PRODUCT_LENGTH,
)


def clean_text(text: Any) -> str:
    """Standardized text cleaning for consistency."""
    if text is None:
        return ""

    text_str = str(text).strip()
    text_str = re.sub(r"\s+", " ", text_str)
    return text_str


def clean_quantity(value: Any) -> float:
    """Extract the first numeric value from strings like '10 Nos' or '5.5 Units'."""
    if value is None:
        return 0.0

    match = re.search(r"\d+(\.\d+)?", str(value))
    if match:
        return float(match.group())

    return 0.0


def is_valid_product(product: Any) -> bool:
    """Combined validation: length, numeric, totals, sections."""
    if product is None:
        return False

    text = str(product).strip()

    # Too short
    if len(text) < 3:
        return False

    # Pure number (row index)
    if text.replace(".", "").isnumeric():
        return False

    # Paragraph description
    if len(text) > MAX_PRODUCT_LENGTH:
        return False

    text_lower = text.lower()

    # Total / subtotal rows
    if any(k in text_lower for k in INVALID_ROW_KEYWORDS):
        return False

    # Section headings
    if any(k in text_lower for k in SECTION_KEYWORDS):
        return False

    return True
