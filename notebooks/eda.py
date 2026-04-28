# notebooks/eda.ipynb

import sys
sys.path.append("..") # so notebook can find src/

from src.data_loader import load_financials
from src.data_cleaner import clean_financials

df_raw = load_financials()
df = clean_financials(df_raw)