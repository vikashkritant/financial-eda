# src/data_cleaner.py

import pandas as pd


def clean_financials(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the S&P 500 financials dataframe.
    Steps:
      1. Drop rows with missing core price data
      2. Fill Dividend Yield nulls with 0
      3. Fill remaining numeric nulls with median
    Returns cleaned dataframe.
    """

    # Step 1 — Drop rows where core price columns are missing
    core_cols = ["Price", "Market Cap", "52 Week Low", "52 Week High"]
    df = df.dropna(subset=core_cols)

    # Step 2 — No dividend = 0, not missing
    df["Dividend Yield"] = df["Dividend Yield"].fillna(0)

    # Step 3 — Fill remaining numeric columns with median
    cols_to_fill = ["Price/Earnings", "Earnings/Share", "EBITDA", 
                    "Price/Sales", "Price/Book"]
    for col in cols_to_fill:
        df[col] = df[col].fillna(df[col].median())

    return df