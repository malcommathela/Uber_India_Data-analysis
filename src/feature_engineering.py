"""
Stage-3 feature extraction for the Uber India 2024 capstone.
Derived metrics never overwrite source observations.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def extract_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "Booking_DateTime" not in out.columns:
        raise ValueError("Booking_DateTime is required before temporal extraction.")

    dt = pd.to_datetime(out["Booking_DateTime"], errors="coerce")
    out["Booking_Hour"] = dt.dt.hour
    out["Booking_Day"] = dt.dt.day
    out["Booking_Month"] = dt.dt.month
    out["Booking_Month_Name"] = dt.dt.month_name()
    out["Booking_Weekday"] = dt.dt.day_name()
    out["Is_Weekend"] = dt.dt.weekday >= 5

    out["Time_of_Day"] = np.select(
        [
            out["Booking_Hour"].between(5, 11, inclusive="both"),
            out["Booking_Hour"].between(12, 16, inclusive="both"),
            out["Booking_Hour"].between(17, 20, inclusive="both"),
        ],
        ["Morning", "Afternoon", "Evening"],
        default="Night",
    )
    return out


def create_cancellation_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "Is_Cancelled" not in out.columns:
        raise ValueError("Run Stage-4 outcome derivation before cancellation features.")

    out["Cancellation_Type"] = np.select(
        [
            out.get("Is_Customer_Cancelled", False),
            out.get("Is_Driver_Cancelled", False),
        ],
        ["Customer", "Driver"],
        default="None",
    )
    out.loc[
        out.get("Is_Customer_Cancelled", False) & out.get("Is_Driver_Cancelled", False),
        "Cancellation_Type"
    ] = "Both"
    return out


def create_revenue_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {"Booking Value", "Ride Distance"}.issubset(out.columns):
        # Revenue/fare efficiency is meaningful only for positive-distance trips.
        out["Revenue_per_km"] = np.where(
            out["Ride Distance"] > 0,
            out["Booking Value"] / out["Ride Distance"],
            np.nan,
        )
        threshold = out.loc[out["Is_Completed"], "Booking Value"].quantile(0.75)             if "Is_Completed" in out else out["Booking Value"].quantile(0.75)
        out["High_Value_Ride"] = out["Booking Value"].ge(threshold)
    return out


def create_operational_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "Avg VTAT" in out.columns:
        out["Wait_Time_Category"] = pd.cut(
            out["Avg VTAT"], [-np.inf, 5, 10, 20, np.inf],
            labels=["Quick (≤5 min)", "Moderate (5–10 min)",
                    "Long (10–20 min)", "Very Long (>20 min)"],
        ).astype("string")
    if "Ride Distance" in out.columns:
        out["Distance_Category"] = pd.cut(
            out["Ride Distance"], [-np.inf, 3, 10, 25, np.inf],
            labels=["Short (≤3 km)", "Medium (3–10 km)",
                    "Long (10–25 km)", "Very Long (>25 km)"],
        ).astype("string")
    return out


def create_rating_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {"Driver Rating", "Customer Rating"}.issubset(out.columns):
        out["Avg_Rating"] = out[["Driver Rating", "Customer Rating"]].mean(axis=1)
        out["Rating_Category"] = pd.cut(
            out["Avg_Rating"], [-np.inf, 3, 4, 4.5, np.inf],
            labels=["Poor", "Average", "Good", "Excellent"],
        ).astype("string")
    return out


def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    out = extract_temporal_features(df)
    out = create_cancellation_features(out)
    out = create_revenue_features(out)
    out = create_operational_features(out)
    out = create_rating_features(out)
    return out
