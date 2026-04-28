# src/data_loader.py
import os
import pandas as pd

url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/main/data/constituents-financials.csv"

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

def load_financials() -> pd.DataFrame:
    """
    Loads S&P 500 financials from public GitHub URL.
    Returns raw dataframe.
    """
    download_csv(url, "financials.csv")
    df=pd.read_csv("data/financials.csv")
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df