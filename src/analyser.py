# src/analyser.py

import pandas as pd
import numpy as np


def sector_company_count(df: pd.DataFrame) -> pd.Series:
    """Number of companies per sector."""
    return df.groupby("Broad Sector")["Name"].count().sort_values(ascending=False)


def sector_avg_market_cap(df: pd.DataFrame) -> pd.Series:
    """Average Market Cap per sector — sorted descending."""
    return (
        df.groupby("Broad Sector")["Market Cap"]
        .mean()
        .sort_values(ascending=False)
    )


def sector_avg_earnings(df: pd.DataFrame) -> pd.Series:
    """Average Earnings/Share per sector — sorted descending."""
    return (
        df.groupby("Broad Sector")["Earnings/Share"]
        .mean()
        .sort_values(ascending=False)
    )


def sector_market_cap_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full descriptive stats for Market Cap per sector.
    Uses NumPy via pandas agg for mean, median, std, min, max.
    """
    return (
        df.groupby("Broad Sector")["Market Cap"]
        .agg(
            Mean=np.mean,
            Median=np.median,
            Std=np.std,
            Min=np.min,
            Max=np.max
        )
        .sort_values("Mean", ascending=False)
    )


def top_companies_by_market_cap(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top N companies by Market Cap."""
    return (
        df[["Name", "Broad Sector", "Market Cap", "Price", "Earnings/Share"]]
        .sort_values("Market Cap", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )