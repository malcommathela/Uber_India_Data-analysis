"""
column_mapper.py
Auto-detects actual column names in the dataset and maps them to standardized names.
Run this before any other module to ensure column name compatibility.
"""

import pandas as pd

# Mapping of expected names → possible variations found in real datasets
COLUMN_ALIASES = {
    'Date': ['date', 'Date', 'DATE', 'Booking_Date'],
    'Time': ['time', 'Time', 'TIME', 'Booking_Time'],
    'Booking ID': ['booking id', 'Booking ID', 'Booking_ID', 'booking_id', 'BookingId'],
    'Booking Status': ['booking status', 'Booking Status', 'Booking_Status', 'booking_status', 'Status'],
    'Customer ID': ['customer id', 'Customer ID', 'Customer_ID', 'customer_id', 'CustomerId'],
    'Vehicle Type': ['vehicle type', 'Vehicle Type', 'Vehicle_Type', 'vehicle_type', 'VehicleType', 'vehicle'],
    'Pickup Location': ['pickup location', 'Pickup Location', 'Pickup_Location', 'pickup_location', 'Pickup', 'pickup'],
    'Drop Location': ['drop location', 'Drop Location', 'Drop_Location', 'drop_location', 'Drop', 'drop', 'Destination'],
    'Avg VTAT': ['avg vtat', 'Avg VTAT', 'Avg_VTAT', 'avg_vtat', 'VTAT', 'vtat', 'Driver Arrival Time'],
    'Avg CTAT': ['avg ctat', 'Avg CTAT', 'Avg_CTAT', 'avg_ctat', 'CTAT', 'ctat', 'Trip Duration'],

    # YOUR ACTUAL COLUMN NAMES:
    'Customer Cancellation': [
        'customer cancellation', 'Customer Cancellation', 'Customer_Cancellation', 'customer_cancellation',
        'Cust_Cancel', 'cust_cancel',
        'Cancelled Rides by Customer', 'cancelled rides by customer', 'Cancelled_Rides_by_Customer'
    ],
    'Customer Cancellation Reason': [
        'customer cancellation reason', 'Customer Cancellation Reason', 'Customer_Cancellation_Reason',
        'Cust_Cancel_Reason', 'cust_cancel_reason',
        'Reason for cancelling by Customer', 'reason for cancelling by customer',
        'Reason_for_cancelling_by_Customer'
    ],
    'Driver Cancellation': [
        'driver cancellation', 'Driver Cancellation', 'Driver_Cancellation', 'driver_cancellation',
        'Driv_Cancel', 'driv_cancel',
        'Cancelled Rides by Driver', 'cancelled rides by driver', 'Cancelled_Rides_by_Driver'
    ],
    'Driver Cancellation Reason': [
        'driver cancellation reason', 'Driver Cancellation Reason', 'Driver_Cancellation_Reason',
        'Driv_Cancel_Reason', 'driv_cancel_reason'
    ],
    'Incomplete Ride': [
        'incomplete ride', 'Incomplete Ride', 'Incomplete_Ride', 'incomplete_ride', 'Incomplete',
        'Incomplete Rides', 'incomplete rides', 'Incomplete_Rides'
    ],
    'Incomplete Ride Reason': [
        'incomplete ride reason', 'Incomplete Ride Reason', 'Incomplete_Ride_Reason',
        'Incomplete Rides Reason', 'incomplete rides reason', 'Incomplete_Rides_Reason'
    ],
    'Booking Value': [
        'booking value', 'Booking Value', 'Booking_Value', 'booking_value',
        'Fare', 'fare', 'Price', 'price', 'Amount', 'amount'
    ],
    'Ride Distance': [
        'ride distance', 'Ride Distance', 'Ride_Distance', 'ride_distance',
        'Distance', 'distance', 'KM', 'km'
    ],
    'Driver Rating': [
        'driver rating', 'Driver Rating', 'Driver_Rating', 'driver_rating',
        'Driv_Rating', 'driv_rating',
        'Driver Ratings', 'driver ratings', 'Driver_Ratings'
    ],
    'Customer Rating': [
        'customer rating', 'Customer Rating', 'Customer_Rating', 'customer_rating',
        'Cust_Rating', 'cust_rating', 'Rating'
    ],
    'Payment Method': [
        'payment method', 'Payment Method', 'Payment_Method', 'payment_method',
        'Payment', 'payment', 'Payment_Mode'
    ],
}


def detect_columns(df: pd.DataFrame) -> dict:
    """
    Detect actual column names in the dataframe and map to standardized names.

    Returns:
        dict: {standardized_name: actual_column_name} for found columns
    """
    actual_cols = list(df.columns)
    actual_cols_lower = [c.lower().strip().replace('_', ' ') for c in actual_cols]

    mapping = {}
    unmatched = []

    for standard_name, aliases in COLUMN_ALIASES.items():
        found = False
        for alias in aliases:
            alias_normalized = alias.lower().strip().replace('_', ' ')
            if alias in actual_cols:
                mapping[standard_name] = alias
                found = True
                break
            elif alias_normalized in actual_cols_lower:
                idx = actual_cols_lower.index(alias_normalized)
                mapping[standard_name] = actual_cols[idx]
                found = True
                break

        if not found:
            unmatched.append(standard_name)

    print("=" * 60)
    print("📋 COLUMN NAME DETECTION")
    print("=" * 60)
    print(f"\n✅ Found {len(mapping)} matching columns:")
    for std, actual in mapping.items():
        if std != actual:
            print(f"   '{actual}' → '{std}'")
        else:
            print(f"   '{std}'")

    if unmatched:
        print(f"\n❌ {len(unmatched)} columns not found:")
        for col in unmatched:
            print(f"   '{col}'")

    return mapping


def rename_columns(df: pd.DataFrame, mapping: dict = None) -> pd.DataFrame:
    """
    Rename dataframe columns to standardized names using detected mapping.

    Parameters:
        df (pd.DataFrame): Input dataframe.
        mapping (dict): Optional pre-computed mapping. If None, auto-detects.

    Returns:
        pd.DataFrame: DataFrame with standardized column names.
    """
    if mapping is None:
        mapping = detect_columns(df)

    # Create reverse mapping: actual_name → standard_name
    rename_map = {actual: standard for standard, actual in mapping.items()}

    # Only rename columns that exist in the mapping
    cols_to_rename = {k: v for k, v in rename_map.items() if k in df.columns}

    df = df.rename(columns=cols_to_rename)
    print(f"\n🔧 Renamed {len(cols_to_rename)} columns to standardized names.")

    return df


if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from src.data_loader import load_uber_data

    df = load_uber_data()
    mapping = detect_columns(df)
    df_renamed = rename_columns(df, mapping)
    print("\n📊 Standardized columns:", list(df_renamed.columns))