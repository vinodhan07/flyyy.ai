# ─── BOQ Extraction & Consolidation ───
import pandas as pd
from typing import List, Dict
from loguru import logger

from app.config.settings import MAX_REASONABLE_QUANTITY
from app.utils.text_cleaner import clean_text, clean_quantity, is_valid_product
from app.services.column_identifier import identify_columns
from app.services.category_classifier import classify_category


def extract_items(df: pd.DataFrame, header_row: int, field_mapping: Dict, threshold: int = 70) -> List[Dict]:
    """
    Given a raw DataFrame and the detected header row index:
    1. Set header row as column names
    2. Slice data rows
    3. Map columns
    4. Clean, validate, and extract items
    """
    # Set header and slice data
    df.columns = df.iloc[header_row]
    df = df.iloc[header_row + 1:].reset_index(drop=True)

    # Map columns
    columns = identify_columns(df.columns.tolist(), field_mapping, threshold=threshold)
    logger.info(f"Column mapping: {columns}")

    if "product" not in columns:
        logger.warning("Product column not found — skipping sheet.")
        return []

    product_col = columns["product"]
    brand_col = columns.get("brand")
    qty_col = columns.get("quantity")

    items: List[Dict] = []

    for row in df.itertuples(index=False):
        try:
            raw_product = getattr(row, product_col, None) if hasattr(row, product_col) else None
            # Fallback: access by column index if attribute name is mangled
            if raw_product is None:
                col_idx = df.columns.tolist().index(product_col)
                raw_product = row[col_idx]

            product = clean_text(raw_product)

            # ── Validation ──
            if not is_valid_product(product):
                continue

            # ── Quantity ──
            raw_qty = None
            if qty_col:
                raw_qty = getattr(row, qty_col, None) if hasattr(row, qty_col) else None
                if raw_qty is None:
                    col_idx = df.columns.tolist().index(qty_col)
                    raw_qty = row[col_idx]

            quantity = clean_quantity(raw_qty)

            if quantity <= 0 or quantity > MAX_REASONABLE_QUANTITY:
                continue

            # ── Brand ──
            raw_brand = None
            if brand_col:
                raw_brand = getattr(row, brand_col, None) if hasattr(row, brand_col) else None
                if raw_brand is None:
                    col_idx = df.columns.tolist().index(brand_col)
                    raw_brand = row[col_idx]

            brand = clean_text(raw_brand) or "Generic"

            # ── Build item ──
            item = {
                "product": product,
                "brand": brand,
                "quantity": quantity,
                "category": classify_category(product),
            }
            items.append(item)

        except Exception as e:
            logger.error(f"Row processing error: {e}")
            continue

    logger.info(f"Extracted {len(items)} valid items from sheet.")
    return items


def consolidate_duplicates(items: List[Dict]) -> List[Dict]:
    """Group identical product+brand pairs and sum their quantities."""
    if not items:
        return []

    df = pd.DataFrame(items)

    grouped = (
        df.groupby(["product", "brand"], as_index=False)
        .agg({"quantity": "sum", "category": "first"})
    )

    return grouped.to_dict(orient="records")
