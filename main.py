# main.py

from src.data_loader import load_financials
from src.data_cleaner import clean_financials
from src.analyser import (
    sector_company_count,
    sector_avg_market_cap,
    sector_avg_earnings,
    sector_market_cap_stats,
    top_companies_by_market_cap
)
from src.visualiser import (
    plot_companies_per_sector,
    plot_avg_market_cap_per_sector,
    plot_market_cap_distribution,
    plot_top_companies,
    plot_price_vs_earnings
)


# Load
df_raw = load_financials()

# Clean
df = clean_financials(df_raw)

print(f"Clean data shape: {df.shape}")
print(f"Any nulls: {df.isnull().values.any()}")

# Analyse
print("=== COMPANIES PER SECTOR ===")
print(sector_company_count(df))

print("\n=== AVG MARKET CAP PER SECTOR ===")
print(sector_avg_market_cap(df))

print("\n=== AVG EARNINGS/SHARE PER SECTOR ===")
print(sector_avg_earnings(df))

print("\n=== MARKET CAP STATS PER SECTOR ===")
print(sector_market_cap_stats(df))

print("\n=== TOP 10 COMPANIES BY MARKET CAP ===")
print(top_companies_by_market_cap(df))

# ── Analyse ────────────────────────────────────────────────────────────────
counts      = sector_company_count(df)
avg_cap     = sector_avg_market_cap(df)
top_cos     = top_companies_by_market_cap(df)

# ── Visualise ──────────────────────────────────────────────────────────────

print("\nGenerating charts...")
plot_companies_per_sector(counts)
plot_avg_market_cap_per_sector(avg_cap)
plot_market_cap_distribution(df)
plot_top_companies(top_cos)
plot_price_vs_earnings(df)


