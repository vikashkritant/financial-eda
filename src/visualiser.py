# src/visualiser.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# ── Global style — apply once for all charts ──────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
OUTPUT_DIR = "output/charts"

def _save(fig, filename: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}")

def plot_companies_per_sector(sector_counts: pd.Series):
    """Bar chart of number of companies per sector."""
    fig,ax=plt.subplots(figsize=(10, 7))
    sector_counts.sort_values().plot(
        kind="barh",        # horizontal bar — sector names are long
        ax=ax,
        color="steelblue"
    )
    ax.set_title("Number of Companies per Sector", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Companies")
    ax.set_ylabel("Sector")
    _save(fig, "01_companies_per_sector.png")

def plot_avg_market_cap_per_sector(sector_avg_cap: pd.Series):
    """Bar chart — average market cap per sector."""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Convert to billions for readability
    (sector_avg_cap / 1e9).sort_values().plot(
        kind="barh",
        ax=ax,
        color="teal"
    )
    ax.set_title("Average Market Cap per Sector (USD Billions)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Avg Market Cap (Billions)")
    ax.set_ylabel("Sector")
    _save(fig, "02_avg_market_cap_per_sector.png")

def plot_market_cap_distribution(df: pd.DataFrame):
    """Box plot — market cap spread across sectors."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Convert to billions
    df_plot = df.copy()
    df_plot["Market Cap (B)"] = df_plot["Market Cap"] / 1e9

    # Order sectors by median for readability
    order = (
        df_plot.groupby("Broad Sector")["Market Cap (B)"]
        .median()
        .sort_values()
        .index
    )

    sns.boxplot(
        data=df_plot,
        x="Market Cap (B)",
        y="Broad Sector",
        hue="Broad Sector",
        legend=False, 
        order=order,
        ax=ax,
        palette="muted"
    )
    ax.set_title("Market Cap Distribution per Sector (USD Billions)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Market Cap (Billions)")
    _save(fig, "03_market_cap_distribution.png")

def plot_top_companies(top_df: pd.DataFrame):
    """Horizontal bar — top 10 companies by market cap."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Convert to billions
    top_df_plot = top_df.copy()
    top_df_plot["Market Cap (B)"] = top_df_plot["Market Cap"] / 1e9

    sns.barplot(
    data=top_df_plot,
    x="Market Cap (B)",
    y="Name",
    hue="Name",        # ← add this
    legend=False,      # ← add this
    ax=ax,
    palette="Blues_d"
    )
    ax.set_title("Top 10 Companies by Market Cap (USD Billions)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Market Cap (Billions)")
    ax.set_ylabel("Company")
    _save(fig, "04_top_10_companies.png")


def plot_price_vs_earnings(df: pd.DataFrame):
    """Scatter plot — Price vs Earnings/Share coloured by sector."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Remove extreme outliers for cleaner plot (keep within 99th percentile)
    df_plot = df[
        (df["Price"] < df["Price"].quantile(0.99)) &
        (df["Earnings/Share"] > 0)   # only profitable companies
    ]

    sns.scatterplot(
        data=df_plot,
        x="Earnings/Share",
        y="Price",
        hue="Broad Sector",
        ax=ax,
        alpha=0.7,          # slight transparency so overlaps are visible
        s=60                # dot size
    )
    ax.set_title("Price vs Earnings/Share by Sector", fontsize=14, fontweight="bold")
    ax.set_xlabel("Earnings per Share (USD)")
    ax.set_ylabel("Stock Price (USD)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    _save(fig, "05_price_vs_earnings.png")