# ─── BOQ Extraction with Multiline Merge & Material Detection ───
import re
import pandas as pd
from typing import List, Dict
from collections import defaultdict
from loguru import logger

from ..config.settings import MAX_REASONABLE_QUANTITY
from ..utils.text_cleaner import (
    clean_text,
    clean_quantity,
    is_valid_product,
    is_attribute_line,
    contains_material_keyword,
)
from .column_identifier import identify_columns
from .category_classifier import classify_category


# ─────────────────────────────────────────────
# Multiline Description Merger
# ─────────────────────────────────────────────

def merge_multiline_descriptions(df: pd.DataFrame, product_col: str, qty_col: str = None) -> pd.DataFrame:
    """
    BOQ sheets often spread one item across multiple rows:
      Row 1: 'Providing underground insulated chilled water pipe'   (description)
      Row 2: '250 mm nominal dia'                                   (attribute)
      Row 3: 'From 3.0 to 4.5m depth'                               (attribute)
      Row 4: (next real product or quantity row)

    This function merges attribute lines into their parent description row
    and removes the attribute-only rows.
    """
    merged_rows = []
    current_desc = None
    current_row_data = None

    col_list = df.columns.tolist()
    prod_idx = col_list.index(product_col) if product_col in col_list else None
    qty_idx = col_list.index(qty_col) if (qty_col and qty_col in col_list) else None

    if prod_idx is None:
        return df

    for i in range(len(df)):
        row = df.iloc[i]
        cell_text = clean_text(row.iloc[prod_idx]) if prod_idx is not None else ""

        # Skip completely empty rows
        if not cell_text or cell_text.lower() in ("nan", "none", ""):
            if current_row_data is not None:
                merged_rows.append(current_row_data)
                current_row_data = None
                current_desc = None
            continue

        if is_attribute_line(cell_text):
            # Append attribute text to the current description
            if current_desc is not None:
                current_desc += " " + cell_text
                current_row_data[product_col] = current_desc

                # If this attribute row has a qty and parent doesn't, take it
                if qty_col and qty_idx is not None:
                    parent_qty = clean_quantity(current_row_data.get(qty_col))
                    attr_qty = clean_quantity(row.iloc[qty_idx])
                    if parent_qty <= 0 and attr_qty > 0:
                        current_row_data[qty_col] = row.iloc[qty_idx]
        else:
            # This is a new product line — commit previous
            if current_row_data is not None:
                merged_rows.append(current_row_data)

            current_row_data = row.to_dict()
            current_desc = cell_text
            current_row_data[product_col] = current_desc

    # Flush last item
    if current_row_data is not None:
        merged_rows.append(current_row_data)

    if not merged_rows:
        return df

    result = pd.DataFrame(merged_rows)
    logger.info(f"Multiline merge: {len(df)} rows → {len(result)} merged rows")
    return result.reset_index(drop=True)


# ─────────────────────────────────────────────
# Main Extraction
# ─────────────────────────────────────────────

def extract_items(df: pd.DataFrame, header_row: int, field_mapping: Dict, threshold: int = 70) -> List[Dict]:
    """
    Full extraction pipeline per sheet:
    1. Set header row as column names
    2. Slice data rows
    3. Map columns
    4. Merge multiline descriptions
    5. Clean, validate, detect material keywords, and extract items
    """
    # Set header and slice data
    df.columns = df.iloc[header_row]
    df = df.iloc[header_row + 1:].reset_index(drop=True)

    # ── Full Dataset Cleaning (Structural Rules) ──
    from ..utils.data_cleaner import clean_dataframe_structure, standardize_dataframe_columns
    df = clean_dataframe_structure(df)

    # Map columns
    columns = identify_columns(df.columns.tolist(), field_mapping, threshold=threshold)
    logger.info(f"Column mapping: {columns}")

    # ── Full Dataset Cleaning (Column-Specific Rules) ──
    df = standardize_dataframe_columns(df, columns)

    desc_col = columns.get("description")
    brand_col = columns.get("brand")
    qty_col = columns.get("quantity")
    unit_col = columns.get("unit")

    # ── Multiline merge ──
    df = merge_multiline_descriptions(df, desc_col, qty_col)

    items: List[Dict] = []

    for row in df.itertuples(index=False):
        try:
            # ── Description ──
            raw_description = _safe_get(row, df, desc_col)
            description = clean_text(raw_description)

            # Basic validation (empty, numeric, totals, sections)
            if not is_valid_product(description):
                continue

            # Skip very short descriptions (likely noise like "1", "A", "Ref")
            if len(description) < 5:
                continue

            # ── Quantity ──
            raw_qty = _safe_get(row, df, qty_col) if qty_col else None
            quantity = clean_quantity(raw_qty)

            # Only skip if quantity is clearly over the max limit (don't skip qty=0 — it may just be missing)
            if quantity > MAX_REASONABLE_QUANTITY:
                continue

            # ── Brand ──
            raw_brand = _safe_get(row, df, brand_col) if brand_col else None
            brand = clean_text(raw_brand) or "Generic"

            # ── Unit ──
            raw_unit = _safe_get(row, df, unit_col) if unit_col else None
            unit = clean_text(raw_unit) or "-"

            # ── Build item ──
            item = {
                "description": description,
                "brand": brand,
                "quantity": quantity,
                "unit": unit,
                "category": classify_category(description),
            }
            items.append(item)

        except Exception as e:
            logger.error(f"Row processing error: {e}")
            continue

    logger.info(f"Extracted {len(items)} valid material items from sheet.")
    return items


def _safe_get(row, df, col_name):
    """Safely get a value from a namedtuple row, falling back to index access."""
    if col_name is None:
        return None
    val = getattr(row, col_name, None) if hasattr(row, col_name) else None
    if val is None:
        try:
            col_idx = df.columns.tolist().index(col_name)
            val = row[col_idx]
        except (ValueError, IndexError):
            pass
    return val


# ─────────────────────────────────────────────
# Consolidation & Grouping
# ─────────────────────────────────────────────

def consolidate_duplicates(items: List[Dict]) -> List[Dict]:
    """Group identical product+brand pairs and sum their quantities."""
    if not items:
        return []

    df = pd.DataFrame(items)

    grouped = (
        df.groupby(["description", "brand", "unit"], as_index=False)
        .agg({"quantity": "sum", "category": "first"})
    )

    return grouped.to_dict(orient="records")


def group_by_category(items: List[Dict]) -> Dict[str, List[Dict]]:
    """Group items by their EPC category."""
    grouped = defaultdict(list)
    for item in items:
        grouped[item["category"]].append(item)


def read_excel_to_text(file_path):
    # 'sheet_name=None' tells Pandas to read every single tab in the Excel file
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    combined_text = ""
    
    for sheet_name, df in all_sheets.items():
        combined_text += f"\n--- SHEET: {sheet_name} ---\n"
        combined_text += df.to_string()
        
    return combined_text
