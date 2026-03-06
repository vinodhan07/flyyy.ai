# ─── Header Detection (Keyword Scoring) ───
import pandas as pd
from typing import Optional

from app.config.settings import HEADER_KEYWORDS, HEADER_SCAN_LIMIT


def detect_header_row(df: pd.DataFrame) -> int:
    """Return the row index with the highest header-keyword score."""
    best_row = 0
    best_score = 0

    scan_limit = min(len(df), HEADER_SCAN_LIMIT)

    for i in range(scan_limit):
        row_text = " ".join(df.iloc[i].astype(str).str.lower())
        score = sum(1 for kw in HEADER_KEYWORDS if kw in row_text)

        if score > best_score:
            best_score = score
            best_row = i

    return best_row