"""Stage 8: produce a machine-readable results snapshot for interpretation."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "03_Data_Extraction" / "extracted_dataset.csv")

total = len(df)
outcomes = df["Booking_Outcome"].value_counts(dropna=False).to_dict()

result = {
    "total_bookings": int(total),
    "outcomes": {str(k): int(v) for k, v in outcomes.items()},
    "rates": {str(k): round(float(v / total), 6) for k, v in outcomes.items()},
    "rating_observation": {},
}

for col in ["Driver Rating", "Customer Rating"]:
    if col in df.columns:
        n = int(df[col].notna().sum())
        result["rating_observation"][col] = {
            "observed": n,
            "coverage": round(n / total, 6),
            "mean": None if n == 0 else round(float(df[col].mean()), 4),
            "median": None if n == 0 else round(float(df[col].median()), 4),
        }

if "Booking Value" in df.columns and "Is_Completed" in df.columns:
    values = df.loc[df["Is_Completed"] == True, "Booking Value"].dropna()
    result["completed_revenue"] = {
        "observed_completed_bookings": int(len(values)),
        "total_booking_value": round(float(values.sum()), 2),
        "mean_booking_value": round(float(values.mean()), 2) if len(values) else None,
        "median_booking_value": round(float(values.median()), 2) if len(values) else None,
    }

OUT = ROOT / "08_Results_and_Interpretation" / "results_snapshot.json"
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(f"Saved: {OUT}")
