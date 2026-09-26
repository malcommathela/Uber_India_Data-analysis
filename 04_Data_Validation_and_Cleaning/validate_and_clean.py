"""Stage 4: validate and clean the filtered study population."""
from pathlib import Path
from src.preprocessing import clean_dataset

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "02_Data_Acquisition_and_Filtering" / "filtered_dataset.csv"
OUT = ROOT / "04_Data_Validation_and_Cleaning" / "cleaned_dataset.csv"
AUDIT = ROOT / "04_Data_Validation_and_Cleaning" / "validation_audit.csv"

df = pd.read_csv(INPUT)
cleaned, audit = clean_dataset(df, return_audit=True)
cleaned.to_csv(OUT, index=False)
audit.to_csv(AUDIT, index=False)

print(f"Input rows: {len(df):,}")
print(f"Output rows: {len(cleaned):,}")
print(f"Saved: {OUT}")
print(f"Audit: {AUDIT}")
