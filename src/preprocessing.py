"""
Data validation and cleaning for the Uber India 2024 capstone.

Design principles:
- preserve structural missingness;
- never silently manufacture ratings/VTAT/CTAT;
- separate cancellation, unfulfilled and incomplete outcomes;
- flag outliers instead of silently clipping them;
- return an audit log with every material transformation.
"""
from __future__ import annotations

from typing import Dict, Tuple
import numpy as np
import pandas as pd


NUMERIC_COLUMNS = [
    "Booking Value", "Ride Distance", "Avg VTAT", "Avg CTAT",
    "Driver Rating", "Customer Rating",
]


def remove_duplicates(df: pd.DataFrame, audit: list[dict] | None = None) -> pd.DataFrame:
    audit = audit if audit is not None else []
    before = len(df)
    out = df.drop_duplicates().copy()
    audit.append({"step": "exact_duplicates", "rows_before": before,
                  "rows_after": len(out), "removed": before - len(out)})
    return out


def normalize_boolean(series: pd.Series) -> pd.Series:
    """Normalize common boolean encodings without treating unknowns as False."""
    if pd.api.types.is_bool_dtype(series):
        return series
    normalized = series.astype("string").str.strip().str.lower()
    mapped = normalized.map({
        "yes": True, "y": True, "true": True, "1": True, "1.0": True,
        "no": False, "n": False, "false": False, "0": False, "0.0": False,
    })
    return mapped.astype("boolean")


def fix_data_types(df: pd.DataFrame, audit: list[dict] | None = None) -> pd.DataFrame:
    audit = audit if audit is not None else []
    out = df.copy()

    if "Date" in out.columns:
        out["Date"] = pd.to_datetime(out["Date"], errors="coerce")
    if "Time" in out.columns:
        # Keep the source time column while deriving a canonical datetime.
        parsed_time = pd.to_datetime(\n            out["Time"].astype("string").str.strip(),\n            format="%H:%M:%S",\n            errors="coerce",\n        )
        if "Date" in out.columns:
            out["Booking_DateTime"] = pd.to_datetime(
                out["Date"].dt.strftime("%Y-%m-%d") + " " +
                parsed_time.dt.strftime("%H:%M:%S"),
                errors="coerce",
            )
        else:
            out["Booking_DateTime"] = parsed_time

    for col in NUMERIC_COLUMNS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in ["Customer Cancellation", "Driver Cancellation", "Incomplete Ride"]:
        if col in out.columns:
            out[col] = normalize_boolean(out[col])

    if "Booking Status" in out.columns:
        out["Booking Status"] = out["Booking Status"].astype("string").str.strip()

    audit.append({
        "step": "data_types",
        "invalid_datetime": int(out.get("Booking_DateTime", pd.Series(dtype="datetime64[ns]")).isna().sum())
        if "Booking_DateTime" in out else 0,
    })
    return out


def derive_outcome_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Derive mutually meaningful outcome flags from source flags/status."""
    out = df.copy()
    status = out.get("Booking Status", pd.Series("", index=out.index, dtype="string")).astype("string").str.lower()

    customer = out.get("Customer Cancellation", pd.Series(False, index=out.index)).fillna(False).astype(bool)
    driver = out.get("Driver Cancellation", pd.Series(False, index=out.index)).fillna(False).astype(bool)
    incomplete = out.get("Incomplete Ride", pd.Series(False, index=out.index)).fillna(False).astype(bool)

    # Status is used as a fallback only where source boolean fields are absent/empty.
    customer = customer | status.str.contains("cancelled by customer", na=False)
    driver = driver | status.str.contains("cancelled by driver", na=False)
    incomplete = incomplete | status.str.contains("incomplete", na=False)

    no_driver = status.str.contains("no driver found", na=False)

    out["Is_Customer_Cancelled"] = customer
    out["Is_Driver_Cancelled"] = driver
    out["Is_Cancelled"] = customer | driver
    out["Is_Unfulfilled"] = no_driver
    out["Is_Incomplete"] = incomplete
    out["Is_Completed"] = status.eq("completed")

    def outcome(row):
        if row["Is_Completed"]:
            return "Completed"
        if row["Is_Customer_Cancelled"]:
            return "Cancelled by Customer"
        if row["Is_Driver_Cancelled"]:
            return "Cancelled by Driver"
        if row["Is_Unfulfilled"]:
            return "No Driver Found"
        if row["Is_Incomplete"]:
            return "Incomplete"
        return "Other/Unknown"

    out["Booking_Outcome"] = out.apply(outcome, axis=1)
    return out


def handle_missing_values(df: pd.DataFrame, audit: list[dict] | None = None) -> pd.DataFrame:
    """
    Clean missing values without fabricating measurements.

    Ratings, VTAT and CTAT remain NaN when the observation is structurally
    unavailable (for example, a cancelled ride).
    """
    audit = audit if audit is not None else []
    out = df.copy()

    reason_cols = [
        "Customer Cancellation Reason", "Driver Cancellation Reason",
        "Incomplete Ride Reason",
    ]
    for col in reason_cols:
        if col in out.columns:
            out[col] = out[col].astype("string").str.strip()

    categorical = ["Vehicle Type", "Payment Method", "Pickup Location",
                   "Drop Location", "Booking Status"]
    for col in categorical:
        if col in out.columns:
            out[col] = out[col].astype("string").str.strip()
            # Missing categorical values remain explicit rather than mode-imputed.
            out[col] = out[col].fillna("Unknown")

    audit.append({
        "step": "missing_values",
        "numeric_imputation": "none",
        "structural_missingness_preserved": True,
    })
    return out


def validate_ranges(df: pd.DataFrame, audit: list[dict] | None = None) -> pd.DataFrame:
    audit = audit if audit is not None else []
    out = df.copy()

    for col in ["Booking Value", "Ride Distance", "Avg VTAT", "Avg CTAT"]:
        if col in out.columns:
            invalid = out[col].notna() & (out[col] < 0)
            audit.append({"step": "range_check", "column": col,
                          "invalid_negative": int(invalid.sum())})
            out.loc[invalid, col] = np.nan

    for col in ["Driver Rating", "Customer Rating"]:
        if col in out.columns:
            invalid = out[col].notna() & ~out[col].between(1, 5)
            audit.append({"step": "rating_check", "column": col,
                          "invalid_out_of_range": int(invalid.sum())})
            out.loc[invalid, col] = np.nan
    return out


def flag_outliers(df: pd.DataFrame, audit: list[dict] | None = None) -> pd.DataFrame:
    """Flag IQR outliers; do not clip or delete them automatically."""
    audit = audit if audit is not None else []
    out = df.copy()

    for col in ["Booking Value", "Ride Distance"]:
        if col not in out.columns:
            continue
        valid = out[col].dropna()
        if valid.empty:
            continue
        q1, q3 = valid.quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        flag_col = f"{col.replace(' ', '_')}_Outlier"
        out[flag_col] = out[col].notna() & ~out[col].between(lo, hi)
        audit.append({"step": "outlier_flag", "column": col,
                      "lower_bound": float(lo), "upper_bound": float(hi),
                      "flagged": int(out[flag_col].sum())})
    return out


def standardise_text(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ["Pickup Location", "Drop Location", "Vehicle Type", "Payment Method"]:
        if col in out.columns:
            out[col] = out[col].astype("string").str.strip()
    return out


def clean_dataset(df: pd.DataFrame, return_audit: bool = False):
    """Run the Stage-4 validation/cleaning contract."""
    audit: list[dict] = []
    out = df.copy()

    try:
        from src.column_mapper import detect_columns, rename_columns
        mapping = detect_columns(out)
        out = rename_columns(out, mapping)
    except (ImportError, ValueError, TypeError):
        pass

    out = remove_duplicates(out, audit)
    out = fix_data_types(out, audit)
    out = standardise_text(out)
    out = validate_ranges(out, audit)
    out = handle_missing_values(out, audit)
    out = flag_outliers(out, audit)
    out = derive_outcome_flags(out)

    audit_df = pd.DataFrame(audit)
    return (out, audit_df) if return_audit else out
