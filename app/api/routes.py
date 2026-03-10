# ─── API Routes ───
from fastapi import APIRouter, UploadFile, Query, HTTPException
import io
from loguru import logger

from ..config.settings import get_config
from ..services.boq_table_detector import detect_header_row
from ..services.column_identifier import identify_columns
from ..services.boq_extractor import extract_items, consolidate_duplicates, group_by_category, read_excel_to_text
from ..services.excel_analyzer import process_excel
from ..utils.product_normalizer import normalize_products
from ..models.boq_schema import BOQList, BOQItem
from ..graphs.excel_graph import extract_with_ai
import shutil

router = APIRouter()

ALLOWED_EXTENSIONS = {".xlsx", ".xls"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def validate_file(file: UploadFile) -> bytes:
    """Validate file extension and size, return raw bytes."""
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Supported: {ALLOWED_EXTENSIONS}",
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        logger.error(f"File too large: {len(contents)} bytes")
        raise HTTPException(status_code=400, detail="File too large. Max 10 MB.")

    return contents


@router.post("/extract")
async def extract_excel_data(
    file: UploadFile,
    industry: str = Query(
        "construction", description="Target industry for extraction logic"
    ),
):
    """
    Full extraction pipeline:
    Upload → Validate → Load → Loop sheets → Detect header →
    Map columns → Filter rows → Clean → Classify → Deduplicate → Return
    """
    logger.info(f"Request: industry={industry}, file={file.filename}")

    try:
        # 1. Validate
        contents = await validate_file(file)

        # 2-8. Process all sheets (Load, Loop, Header, Map, Filter, Extract)
        result = process_excel(io.BytesIO(contents), industry=industry)
        items = result["items"]

        # 9. Normalize Product Names (Fuzzy Merge)
        items = normalize_products(items)

        # 11. Merge Duplicate Materials (Final Exact Grouping)
        items = consolidate_duplicates(items)

        logger.info(f"Final output: {len(items)} items from {result['total_sheets']} sheet(s).")

        # 12. Return Structured BOQ Output
        # Grouping by category (optional extra step for response)
        categories = group_by_category(items)

        return {
            "total_sheets": result["total_sheets"],
            "sheets_with_data": result["sheets_with_data"],
            "extracted_items": len(items),
            "items": items,
            "categories": categories,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail="Extraction failed.")


@router.post("/upload-excel")
async def upload_excel_file(
    file: UploadFile,
    industry: str = Query(
        "construction", description="Target industry for AI context"
    )
):
    logger.info(f"AI Extraction Request: industry={industry}, file={file.filename}")

    try:
        # 1. Validate file
        contents = await validate_file(file)

        # 2. Save the file temporarily
        import tempfile, os
        temp_path = os.path.join(tempfile.gettempdir(), "boq_temp.xlsx")
        with open(temp_path, "wb") as buffer:
            buffer.write(contents)

        # 3. Read ALL sheets into text
        messy_text = read_excel_to_text(temp_path)
        logger.info(f"Total text length from Excel: {len(messy_text)} chars")

        # 4. Count sheets for the response
        import pandas as pd
        xls = pd.ExcelFile(temp_path)
        total_sheets = len(xls.sheet_names)
        sheets_with_data = list(xls.sheet_names)
        xls.close()

        # 5. Try AI Agent first
        final_boq = extract_with_ai(messy_text, industry=industry)
        items = final_boq.get("items", [])

        # 6. FALLBACK: If AI returned 0 items (quota exhausted), use heuristic extraction
        if len(items) == 0:
            logger.warning("AI extraction returned 0 items — falling back to heuristic extraction")
            result = process_excel(io.BytesIO(contents), industry=industry)
            items = result["items"]
            items = normalize_products(items)
            items = consolidate_duplicates(items)
            logger.info(f"Heuristic fallback: {len(items)} items extracted")

        # 7. Build category groups
        from collections import defaultdict
        categories = defaultdict(list)
        for item in items:
            cat = item.get("category", "Uncategorized")
            categories[cat].append(item)

        logger.info(f"Extraction complete: {len(items)} items from {total_sheets} sheet(s)")

        # Clean up temp file
        try:
            os.remove(temp_path)
        except OSError:
            pass

        # 8. Return consistent response
        return {
            "total_sheets": total_sheets,
            "sheets_with_data": sheets_with_data,
            "extracted_items": len(items),
            "items": items,
            "categories": dict(categories),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

