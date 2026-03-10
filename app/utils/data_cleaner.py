import pandas as pd
from typing import Dict
from loguru import logger

def clean_dataframe_structure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply structural cleaning rules to the BOQ dataframe.
    """
    if df.empty:
        return df

    logger.debug(f"Initial shape: {df.shape}")

    # 1. Remove completely empty rows
    df = df.dropna(how="all")

    # 2. Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # 3. Strip spaces and 4. Lowercase column names
    if not df.columns.empty:
        df.columns = df.columns.astype(str).str.strip().str.lower()

    # 5. Remove duplicate rows
    df = df.drop_duplicates()

    # 6. For all text columns:
    #   - Remove leading/trailing spaces
    #   - Replace \n with space
    #   - Replace \t with space
    #   - Replace multiple spaces with single space
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
            # Use regex to replace multiple spaces/tabs/newlines
            df[col] = df[col].astype(str).replace(r'[\n\t\r]+', ' ', regex=True)
            df[col] = df[col].replace(r'\s+', ' ', regex=True).str.strip()
            
            # Convert string "nan" or "None" back to actual NaN if pandas converted them
            df[col] = df[col].replace({'nan': pd.NA, 'None': pd.NA, '': pd.NA})

    # 9. Remove repeated header rows that may appear inside the dataset
    # E.g. If the header keywords appear again in the rows
    # We do this by checking if a row looks exactly like the header
    header_row_values = list(df.columns)
    # create a mask where all row values match the header values
    mask = pd.Series([True] * len(df), index=df.index)
    for i, col in enumerate(df.columns):
        mask = mask & (df[col] == header_row_values[i])
    df = df[~mask]

    # 10. Reset dataframe index after cleaning
    df = df.reset_index(drop=True)

    logger.debug(f"Cleaned shape: {df.shape}")
    return df

def standardize_dataframe_columns(df: pd.DataFrame, mapped_columns: Dict[str, str]) -> pd.DataFrame:
    """
    Apply column specific cleaning rules to the BOQ dataframe after columns are mapped.
    """
    if df.empty:
        return df

    desc_col = mapped_columns.get("description")
    qty_col = mapped_columns.get("quantity")
    rate_col = mapped_columns.get("rate")
    amount_col = mapped_columns.get("amount")

    # 7. Standardize the "description" column
    if desc_col and desc_col in df.columns:
        # Convert all text to lowercase
        # It's already single-line from step 6 (removed \n)
        df[desc_col] = df[desc_col].astype(str).str.lower()

    # 8. Attempt to convert numeric columns
    numeric_cols = [col for col in [qty_col, rate_col, amount_col] if col and col in df.columns]
    for col in numeric_cols:
        # Remove any commas from numbers before to numeric conversion
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
             df[col] = df[col].astype(str).str.replace(',', '')
             
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Reset index again to be safe
    df = df.reset_index(drop=True)

    return df
