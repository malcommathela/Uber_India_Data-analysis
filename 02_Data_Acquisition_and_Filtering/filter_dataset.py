"""Stage 2: explicit acquisition/filtering boundary.

No arbitrary row filters are applied by default. This makes the original
dataset size observable and prevents silently changing the study population.
"""
from pathlib import Path
import pandas as pd
from src.data_loader import load_uber_data

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "uber_data_india_2024.csv"
OUT = ROOT / "02_Data_Acquisition_and_Filtering" / "filtered_dataset.csv"
LOG = ROOT / "02_Data_Acquisition_and_Filtering" / "filtering_log.csv"

df = load_uber_data(str(RAW))
before = len(df)

# Keep this stage intentionally conservative. Validation belongs to Stage 4.
filtered = df.copy()

pd.DataFrame([{
    "rows_before": before,
    "rows_after": len(filtered),
    "rows_removed": before - len(filtered),
    "rule": "No analytical filtering applied; raw study population retained",
}]).to_csv(LOG, index=False)

filtered.to_csv(OUT, index=False)
print(f"Rows retained: {len(filtered):,}")
