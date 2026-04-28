# main.py

from src.data_loader import load_financials
from src.data_cleaner import clean_financials

# Load
df_raw = load_financials()

# Clean
df = clean_financials(df_raw)

print(f"Clean data shape: {df.shape}")
print(f"Any nulls: {df.isnull().values.any()}")