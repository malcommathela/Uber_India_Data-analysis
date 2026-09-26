"""Stage 1: load the raw dataset and save a reproducible profile."""
from pathlib import Path
import pandas as pd
from src.data_loader import load_uber_data, inspect_data

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "uber_data_india_2024.csv"
OUT = ROOT / "01_Data_Loading_and_Reading" / "data_profile.csv"

df = load_uber_data(str(RAW))
inspect_data(df)
profile = pd.DataFrame({
    "column": df.columns,
    "dtype": [str(x) for x in df.dtypes],
    "missing_count": [int(df[c].isna().sum()) for c in df.columns],
    "missing_pct": [round(float(df[c].isna().mean()*100), 3) for c in df.columns],
    "unique_count": [int(df[c].nunique(dropna=True)) for c in df.columns],
})
profile.to_csv(OUT, index=False)
print(f"Saved profile: {OUT}")
