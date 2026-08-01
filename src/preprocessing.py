"""
preprocessing.py
Data cleaning pipeline for Uber Data India (2024).
Handles missing values, duplicates, outliers, and data type corrections.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the dataset."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"🗑️  Removed {before - after} duplicate rows")
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correct data types for analysis.

    - Date/Time → datetime
    - Booking Value, Distance → float
    - Ratings → float
    - Cancellation flags → boolean
    """
    print("\n🔧 Fixing Data Types...")

    # Combine Date and Time into a single datetime column
    if 'Date' in df.columns and 'Time' in df.columns:
        try:
            df['Booking_DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')
            print("   Created 'Booking_DateTime' from Date + Time")
        except Exception as e:
            print(f"   ⚠️ Could not create datetime: {e}")
    elif 'Date' in df.columns:
        try:
            df['Booking_DateTime'] = pd.to_datetime(df['Date'], errors='coerce')
            print("   Created 'Booking_DateTime' from Date only")
        except Exception as e:
            print(f"   ⚠️ Could not parse Date: {e}")

    # Numeric columns
    numeric_cols = ['Booking Value', 'Ride Distance', 'Avg VTAT', 'Avg CTAT',
                    'Driver Rating', 'Customer Rating']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Boolean/categorical cancellation flags
    bool_cols = ['Customer Cancellation', 'Driver Cancellation', 'Incomplete Ride']
    for col in bool_cols:
        if col in df.columns:
            # Handle various formats: Yes/No, 1/0, True/False, 1.0/0.0, strings
            # First convert to numeric (1/0/NaN), then to boolean
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Converts '1', '1.0', 1, 1.0 → 1.0; 'null' → NaN
            df[col] = df[col].fillna(0)  # NaN → 0
            df[col] = df[col].astype(bool)  # 1.0 → True, 0.0 → False

    # DERIVE cancellation flags from Booking Status if they're all False
    if 'Booking Status' in df.columns:
        status = df['Booking Status'].astype(str).str.strip()

        # If Customer Cancellation is all False, derive from Booking Status
        if 'Customer Cancellation' in df.columns and df['Customer Cancellation'].sum() == 0:
            df.loc[status.str.contains('Cancelled by Customer', case=False, na=False), 'Customer Cancellation'] = True
            print("   Derived Customer Cancellation from Booking Status")

        # If Driver Cancellation is all False, derive from Booking Status
        if 'Driver Cancellation' in df.columns and df['Driver Cancellation'].sum() == 0:
            df.loc[status.str.contains('Cancelled by Driver', case=False, na=False), 'Driver Cancellation'] = True
            print("   Derived Driver Cancellation from Booking Status")

        # Derive Incomplete Ride from Booking Status
        if 'Incomplete Ride' in df.columns and df['Incomplete Ride'].sum() == 0:
            df.loc[status.str.contains('Incomplete', case=False, na=False), 'Incomplete Ride'] = True
            print("   Derived Incomplete Ride from Booking Status")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values based on column type and business logic.

    Strategy:
    - Numeric columns (VTAT, CTAT, Booking Value, Distance): impute with median
    - Categorical columns: impute with mode or 'Unknown'
    - Cancellation reasons: fill with 'Not Cancelled' for non-cancelled rides
    """
    print("\n🔧 Handling Missing Values...")

    # Numeric columns — impute with median
    numeric_cols = ['Avg VTAT', 'Avg CTAT', 'Booking Value', 'Ride Distance',
                    'Driver Rating', 'Customer Rating']
    for col in numeric_cols:
        if col in df.columns:
            missing_before = df[col].isnull().sum()
            if missing_before > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"   {col}: Imputed {missing_before} missing values with median ({median_val:.2f})")

    # Cancellation reasons — fill based on cancellation flag
    if 'Customer Cancellation' in df.columns and 'Customer Cancellation Reason' in df.columns:
        mask = df['Customer Cancellation'] != True
        df.loc[mask, 'Customer Cancellation Reason'] = 'Not Cancelled'
        print("   Customer Cancellation Reason: Filled non-cancelled rows with 'Not Cancelled'")

    if 'Driver Cancellation' in df.columns and 'Driver Cancellation Reason' in df.columns:
        mask = df['Driver Cancellation'] != True
        df.loc[mask, 'Driver Cancellation Reason'] = 'Not Cancelled'
        print("   Driver Cancellation Reason: Filled non-cancelled rows with 'Not Cancelled'")

    # Categorical columns — impute with mode
    cat_cols = ['Vehicle Type', 'Payment Method', 'Pickup Location', 'Drop Location', 'Booking Status']
    for col in cat_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            missing_before = df[col].isnull().sum()
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col] = df[col].fillna(mode_val[0])
                print(f"   {col}: Imputed {missing_before} missing values with mode ('{mode_val[0]}')")

    return df


def handle_outliers(df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
    """
    Handle outliers in numeric columns using IQR method.
    Caps extreme values rather than removing them.
    """
    print("\n🔧 Handling Outliers...")

    outlier_cols = ['Booking Value', 'Ride Distance']

    for col in outlier_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_before = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            print(f"   {col}: Capped {outliers_before} outliers (bounds: {lower_bound:.2f} - {upper_bound:.2f})")

    return df


def standardise_text(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise text columns (strip whitespace, title case for locations)."""
    text_cols = ['Pickup Location', 'Drop Location', 'Vehicle Type', 'Payment Method']

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    print("   Standardised text columns (locations, vehicle type, payment method)")
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline.

    Parameters:
        df (pd.DataFrame): Raw dataset.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    print("\n" + "=" * 60)
    print("🧹 DATA CLEANING PIPELINE")
    print("=" * 60)

    # Step 0: Auto-detect and rename columns to standard names
    try:
        from src.column_mapper import detect_columns, rename_columns
        mapping = detect_columns(df)
        df = rename_columns(df, mapping)
    except ImportError:
        print("⚠️ column_mapper not found. Using original column names.")
    except Exception as e:
        print(f"⚠️ Column mapping failed: {e}. Using original column names.")

    df = remove_duplicates(df)
    df = fix_data_types(df)
    df = handle_missing_values(df)
    df = handle_outliers(df)
    df = standardise_text(df)

    print("\n✅ Cleaning complete!")
    print(f"   Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    return df


if __name__ == "__main__":
    from src.data_loader import load_uber_data

    df = load_uber_data()
    df_clean = clean_dataset(df)

    from src.data_loader import save_processed_data
    save_processed_data(df_clean)