"""Stage 6: core analytical summaries.

Rates use all bookings as the denominator unless explicitly stated otherwise.
Revenue/rating analyses restrict themselves to observations where those
measurements exist.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "03_Data_Extraction" / "extracted_dataset.csv")

total = len(df)
outcomes = df["Booking_Outcome"].value_counts(dropna=False)
print("=== BOOKING OUTCOMES ===")
print(outcomes.to_string())
print("\n=== RATES OF TOTAL BOOKINGS ===")
print((outcomes / total).round(4).to_string())

if "Is_Cancelled" in df:
    print(f"\nCancellation rate: {df['Is_Cancelled'].mean():.2%}")
if "Is_Unfulfilled" in df:
    print(f"Unfulfilled/no-driver-found rate: {df['Is_Unfulfilled'].mean():.2%}")
if "Is_Incomplete" in df:
    print(f"Incomplete ride rate: {df['Is_Incomplete'].mean():.2%}")
if "Is_Completed" in df:
    print(f"Completion rate: {df['Is_Completed'].mean():.2%}")

print("\n=== RATING COVERAGE ===")
for col in ["Driver Rating", "Customer Rating"]:
    if col in df:
        observed = df[col].notna().sum()
        print(f"{col}: {observed:,}/{total:,} observed ({observed/total:.2%})")

print("\n=== REVENUE (COMPLETED RIDES ONLY) ===")
if {"Is_Completed", "Booking Value"}.issubset(df.columns):
    completed = df.loc[df["Is_Completed"] == True, "Booking Value"].dropna()
    print(f"Observed completed rides: {len(completed):,}")
    print(f"Total booking value: ₹{completed.sum():,.2f}")
    print(f"Mean booking value: ₹{completed.mean():,.2f}")
    print(f"Median booking value: ₹{completed.median():,.2f}")
