import pandas as pd
from loguru import logger
from app.config.settings import HEADER_KEYWORDS

def select_boq_sheet(file_path):
    xls = pd.ExcelFile(file_path)
    best_sheet = None
    best_score = 0
    best_df = None

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, engine="openpyxl", header=None)

        # Scan first 20 rows only
        scan_rows = min(len(df), 20)
        score = 0

        for i in range(scan_rows):
            row_text = " ".join(df.iloc[i].astype(str).str.lower())
            for kw in HEADER_KEYWORDS:
                if kw in row_text:
                    score += 1

        if score > best_score:
            best_score = score
            best_sheet = sheet
            best_df = df

    if best_df is None:
        raise ValueError("No valid BOQ sheet detected")

    logger.info(f"Selected sheet: {best_sheet} (score={best_score})")
    return best_df, best_sheet