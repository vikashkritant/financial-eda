# ── Step 1: Setup + Load + First Look ──────────────────────────────────────
import os
from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def download_csv(url, filename):
    """Download a CSV file from a URL and save it locally."""
    folder_name = "data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, filename)

    if os.path.isfile(file_path):
        print(f"File '{file_path}' already exists. Skipping download.")
        return
    try:
        df = pd.read_csv(url)
        df.to_csv(file_path, index=False)
        print(f"File downloaded and saved as {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# ── Load dataset directly from public URL ──────────────────────────────────
url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/main/data/constituents-financials.csv"

download_csv(url, "financials.csv")

df=pd.read_csv("data/financials.csv")

# ── First look ─────────────────────────────────────────────────────────────
print("=== SHAPE ===")
print(df.shape)                    # rows × columns

print("\n=== COLUMNS ===")
print(df.columns.tolist())         # what fields do we have?

print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== DATA TYPES ===")
print(df.dtypes)                   # are numbers stored as numbers?

print("\n=== NULL COUNT PER COLUMN ===")
print(df.isnull().sum())           # where is data missing?

print("\n=== BASIC STATS ===")
print(df.describe())               # mean, std, min, max for numeric columns