"""Stage 5: reproducible analytical tables."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "03_Data_Extraction" / "extracted_dataset.csv"
OUT = ROOT / "05_Data_Aggregation_and_Representation" / "aggregated_tables"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

def save(name, frame):
    frame.to_csv(OUT / f"{name}.csv", index=False)

save("booking_outcomes", df["Booking_Outcome"].value_counts(dropna=False).rename_axis("outcome").reset_index(name="bookings"))

if "Booking_Hour" in df:
    save("bookings_by_hour", df.groupby("Booking_Hour").size().reset_index(name="bookings"))
if "Booking_Weekday" in df:
    save("bookings_by_weekday", df.groupby("Booking_Weekday").size().reset_index(name="bookings"))

if {"Vehicle Type", "Is_Cancelled"}.issubset(df.columns):
    cancel = df.groupby("Vehicle Type").agg(
        bookings=("Booking ID", "count") if "Booking ID" in df else ("Is_Cancelled", "size"),
        cancellations=("Is_Cancelled", "sum"),
    ).reset_index()
    cancel["cancellation_rate"] = cancel["cancellations"] / cancel["bookings"]
    save("cancellation_by_vehicle", cancel)

if {"Vehicle Type", "Booking Value"}.issubset(df.columns):
    completed = df[df["Is_Completed"] == True].copy()
    revenue = completed.groupby("Vehicle Type").agg(
        completed_bookings=("Booking Value", "size"),
        total_booking_value=("Booking Value", "sum"),
        average_booking_value=("Booking Value", "mean"),
        median_booking_value=("Booking Value", "median"),
    ).reset_index()
    save("revenue_by_vehicle", revenue)

if "Payment Method" in df and "Booking Value" in df:
    completed = df[df["Is_Completed"] == True]
    save("revenue_by_payment", completed.groupby("Payment Method")["Booking Value"].agg(
        total_booking_value="sum", average_booking_value="mean",
        median_booking_value="median", completed_bookings="size"
    ).reset_index())

for col in ["Driver Rating", "Customer Rating"]:
    if col in df and "Vehicle Type" in df:
        observed = df.dropna(subset=[col])
        save(f"{col.lower().replace(' ', '_')}_by_vehicle",
             observed.groupby("Vehicle Type")[col].agg(
                 observed_ratings="count", mean="mean", median="median"
             ).reset_index())

print(f"Aggregation complete: {OUT}")
