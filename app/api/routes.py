# Optimized API Routes
from fastapi import APIRouter, UploadFile, Query, HTTPException
from typing import List
import pandas as pd
import io
from loguru import logger

from app.config.settings import get_config
from app.services.boq_table_detector import detect_boq_table
from app.services.column_identifier import identify_columns
from app.services.boq_extractor import extract_boq, consolidate_duplicates
from app.services.excel_analyzer import select_boq_sheet
from app.utils.product_normalizer import normalize_products
from app.models.boq_schema import ExtractedItem

router = APIRouter()

ALLOWED_EXTENSIONS = {".xlsx", ".xls"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_file(file: UploadFile):
    """Validate file extension and size."""
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail=f"Invalid file type. Supported: {ALLOWED_EXTENSIONS}")

    # Check size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        logger.error(f"File too large: {len(contents)} bytes")
        raise HTTPException(status_code=400, detail="File too large. Max 10MB allowed.")
    
    # Reset file pointer for subsequent reads if needed (using BytesIO instead)
    return contents

@router.post("/extract")
async def extract_excel_data(
    file: UploadFile,
    industry: str = Query("construction", description="Target industry for extraction logic")
):
    """
    Generalized endpoint to extract structured data from Excel files
    using industry-specific configurations.
    """
    logger.info(f"Received extraction request for industry: {industry}, file: {file.filename}")
    
    # Load configuration
    config = get_config(industry)
    
    try:
        # Validate and read file
        contents = await validate_file(file)
        
        # 1. Multi-Sheet Detection
        df, sheet_name = select_boq_sheet(io.BytesIO(contents))
        
        # 2. Detect where the data table starts
        df = detect_boq_table(df, config["table_detection_keywords"])
        logger.info(f"Table detection completed. Samples remaining: {len(df)}")
        
        # 3. Identify relevant columns
        column_map = identify_columns(df.columns.tolist(), config["field_mapping"], threshold=config["thresholds"]["fuzzy_match"])
        logger.info(f"Column mapping: {column_map}")
        
        # 4. Validation: Ensure we at least found product/description
        if "product" not in column_map:
            logger.warning("Could not identify product column.")
            return {
                "sheet_name": sheet_name,
                "header_row": None,
                "total_rows": len(df),
                "extracted_items": 0,
                "items": []
            }
        
        # 5. Extract structured items
        items = extract_boq(df, column_map)
        
        # 6. Duplicate Consolidation
        items_consolidated = consolidate_duplicates(items)
        
        # 7. Product Normalization
        items_normalized = normalize_products(items_consolidated)
        
        # Minimum extraction quality check
        if len(items_normalized) < 3:
             logger.warning(f"Low confidence extraction: only {len(items_normalized)} items found.")
        
        logger.info(f"Successfully extracted {len(items_normalized)} items.")
        
        return {
            "sheet_name": sheet_name,
            "header_row": df.index[0] if not df.empty else 0,
            "total_rows": len(df),
            "extracted_items": len(items_normalized),
            "items": items_normalized
        }

    except Exception as e:
        logger.exception(f"Error during extraction: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during extraction.")