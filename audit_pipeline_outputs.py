"""Audit generated Stage 5-8 artifacts for capstone submission quality.

Run after:
    python run_pipeline.py
"""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
errors = []
warnings = []

def check(condition, message, warning=False):
    (warnings if warning else errors).append(message) if not condition else None

# Stage 5
stage5 = ROOT / "05_Data_Aggregation_and_Representation" / "aggregated_tables"
required_tables = [
    "booking_outcomes.csv",
    "bookings_by_hour.csv",
    "bookings_by_weekday.csv",
    "cancellation_by_vehicle.csv",
    "revenue_by_vehicle.csv",
    "revenue_by_payment.csv",
    "driver_rating_by_vehicle.csv",
    "customer_rating_by_vehicle.csv",
]
print("\n=== STAGE 5: AGGREGATED TABLES ===")
for name in required_tables:
    path = stage5 / name
    check(path.exists(), f"Missing Stage 5 artifact: {name}")
    if path.exists():
        frame = pd.read_csv(path)
        print(f"{name}: {len(frame):,} rows, columns={list(frame.columns)}")

# Core consistency checks
outcomes_path = stage5 / "booking_outcomes.csv"
if outcomes_path.exists():
    outcomes = pd.read_csv(outcomes_path)
    total = int(outcomes["bookings"].sum())
    print(f"Total bookings represented by outcome table: {total:,}")
    print(f"Outcome table row total: {total:,}")

# Stage 6
print("\n=== STAGE 6: ANALYSIS SOURCE ===")
analysis_input = ROOT / "03_Data_Extraction" / "extracted_dataset.csv"
check(analysis_input.exists(), "Missing Stage 6 input: extracted_dataset.csv")
if analysis_input.exists():
    df = pd.read_csv(analysis_input)
    print(f"Extracted dataset: {len(df):,} rows × {len(df.columns):,} columns")
    print("Outcome counts:")
    print(df["Booking_Outcome"].value_counts(dropna=False).to_string())
    print(f"Cancellation rate: {df['Is_Cancelled'].mean():.2%}")
    print(f"Completion rate: {df['Is_Completed'].mean():.2%}")
    completed = df.loc[df["Is_Completed"] == True, "Booking Value"].dropna()
    print(f"Completed booking value total: ₹{completed.sum():,.2f}")
    print(f"Completed booking value mean: ₹{completed.mean():,.2f}")
    print(f"Completed booking value median: ₹{completed.median():,.2f}")

# Stage 7
print("\n=== STAGE 7: VISUALIZATIONS ===")
fig_dir = ROOT / "outputs" / "figures"
required_figures = [
    "booking_trends.png",
    "cancellation_analysis.png",
    "revenue_analysis.png",
    "rating_analysis.png",
    "operational_metrics.png",
]
for name in required_figures:
    path = fig_dir / name
    check(path.exists(), f"Missing Stage 7 figure: {name}")
    if path.exists():
        print(f"{name}: {path.stat().st_size:,} bytes")

# Stage 8
print("\n=== STAGE 8: RESULTS ===")
result_path = ROOT / "08_Results_and_Interpretation" / "results_snapshot.json"
check(result_path.exists(), "Missing Stage 8 results_snapshot.json")
if result_path.exists():
    result = json.loads(result_path.read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2))
    check(result.get("total_bookings") == 150000,
          f"Stage 8 total_bookings={result.get('total_bookings')}, expected 150000.")

print("\n=== AUDIT SUMMARY ===")
if errors:
    print("ERRORS:")
    for item in errors:
        print(f"  - {item}")
else:
    print("No structural Stage 5-8 errors detected.")

if warnings:
    print("WARNINGS:")
    for item in warnings:
        print(f"  - {item}")

if errors:
    raise SystemExit(1)

print("Stage 5-8 artifact audit passed.")
