"""Stage 3: derive analytical fields from the Stage-4-cleaned dataset."""
from pathlib import Path
import pandas as pd
from src.feature_engineering import engineer_all_features
from src.preprocessing import clean_dataset

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "04_Data_Validation_and_Cleaning" / "cleaned_dataset.csv"
OUT = ROOT / "03_Data_Extraction" / "extracted_dataset.csv"

df = pd.read_csv(INPUT)
cleaned = clean_dataset(df)
engineered = engineer_all_features(cleaned)
engineered.to_csv(OUT, index=False)
print(f"Saved extracted dataset: {OUT}")
