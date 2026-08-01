"""
feature_engineering.py
Engineer new features for the Uber dataset to support analysis and modeling.
"""

import pandas as pd
import numpy as np


def extract_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract temporal features from Booking_DateTime.

    Features: hour, day, month, weekday, is_weekend, time_of_day
    """
    if 'Booking_DateTime' not in df.columns:
        print("⚠️  'Booking_DateTime' column not found. Run preprocessing first.")
        return df

    print("\n🔧 Extracting Temporal Features...")

    df['Booking_Hour'] = df['Booking_DateTime'].dt.hour
    df['Booking_Day'] = df['Booking_DateTime'].dt.day
    df['Booking_Month'] = df['Booking_DateTime'].dt.month_name()
    df['Booking_Weekday'] = df['Booking_DateTime'].dt.day_name()
    df['Is_Weekend'] = df['Booking_DateTime'].dt.weekday >= 5

    # Time of day categories
    def categorize_time(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    df['Time_of_Day'] = df['Booking_Hour'].apply(categorize_time)

    print("   Created: Booking_Hour, Booking_Day, Booking_Month, Booking_Weekday, Is_Weekend, Time_of_Day")
    return df


def create_cancellation_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create cancellation-related features.

    Features: Is_Cancelled, Cancellation_Type
    """
    print("\n🔧 Creating Cancellation Features...")

    has_customer_cancel = 'Customer Cancellation' in df.columns
    has_driver_cancel = 'Driver Cancellation' in df.columns

    if not has_customer_cancel and not has_driver_cancel:
        print("   ⚠️ No cancellation columns found. Skipping cancellation features.")
        df['Is_Cancelled'] = False
        df['Cancellation_Type'] = 'None'
        return df

    # Overall cancellation flag
    if has_customer_cancel and has_driver_cancel:
        df['Is_Cancelled'] = (df['Customer Cancellation'] == True) | (df['Driver Cancellation'] == True)
    elif has_customer_cancel:
        df['Is_Cancelled'] = df['Customer Cancellation'] == True
    elif has_driver_cancel:
        df['Is_Cancelled'] = df['Driver Cancellation'] == True
    else:
        df['Is_Cancelled'] = False

    # Cancellation type
    def get_cancellation_type(row):
        cust = row.get('Customer Cancellation', False) == True
        driv = row.get('Driver Cancellation', False) == True

        if cust and driv:
            return 'Both'
        elif cust:
            return 'Customer'
        elif driv:
            return 'Driver'
        else:
            return 'None'

    df['Cancellation_Type'] = df.apply(get_cancellation_type, axis=1)

    print(f"   Created: Is_Cancelled ({df['Is_Cancelled'].sum():,} cancellations found)")
    print("   Created: Cancellation_Type")
    return df


def create_revenue_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create revenue-related features.

    Features: Revenue_per_km, High_Value_Ride
    """
    print("\n🔧 Creating Revenue Features...")

    has_value = 'Booking Value' in df.columns
    has_distance = 'Ride Distance' in df.columns

    if has_value and has_distance:
        # Avoid division by zero
        df['Revenue_per_km'] = df['Booking Value'] / df['Ride Distance'].replace(0, np.nan)
        df['Revenue_per_km'] = df['Revenue_per_km'].fillna(0)

        # High-value ride flag (top 25%)
        threshold = df['Booking Value'].quantile(0.75)
        df['High_Value_Ride'] = df['Booking Value'] >= threshold

        print(f"   Created: Revenue_per_km, High_Value_Ride (threshold: ₹{threshold:.2f})")
    else:
        print(f"   ⚠️ Missing columns: {'Booking Value' if not has_value else ''} {'Ride Distance' if not has_distance else ''}")

    return df


def create_operational_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create operational efficiency features.

    Features: Wait_Time_Category, Distance_Category
    """
    print("\n🔧 Creating Operational Features...")

    # Wait time category (based on VTAT)
    if 'Avg VTAT' in df.columns:
        def categorize_wait(vtat):
            if pd.isna(vtat):
                return 'Unknown'
            elif vtat <= 5:
                return 'Quick (<5 min)'
            elif vtat <= 10:
                return 'Moderate (5-10 min)'
            elif vtat <= 20:
                return 'Long (10-20 min)'
            else:
                return 'Very Long (>20 min)'

        df['Wait_Time_Category'] = df['Avg VTAT'].apply(categorize_wait)
        print("   Created: Wait_Time_Category")
    else:
        print("   ⚠️ 'Avg VTAT' not found. Skipping Wait_Time_Category.")

    # Distance category
    if 'Ride Distance' in df.columns:
        def categorize_distance(dist):
            if pd.isna(dist):
                return 'Unknown'
            elif dist <= 3:
                return 'Short (≤3 km)'
            elif dist <= 10:
                return 'Medium (3-10 km)'
            elif dist <= 25:
                return 'Long (10-25 km)'
            else:
                return 'Very Long (>25 km)'

        df['Distance_Category'] = df['Ride Distance'].apply(categorize_distance)
        print("   Created: Distance_Category")
    else:
        print("   ⚠️ 'Ride Distance' not found. Skipping Distance_Category.")

    return df


def create_rating_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create rating-related features.

    Features: Avg_Rating, Rating_Category
    """
    print("\n🔧 Creating Rating Features...")

    has_driver_rating = 'Driver Rating' in df.columns
    has_customer_rating = 'Customer Rating' in df.columns

    if has_driver_rating and has_customer_rating:
        df['Avg_Rating'] = (df['Driver Rating'] + df['Customer Rating']) / 2

        def categorize_rating(rating):
            if pd.isna(rating):
                return 'Unknown'
            elif rating >= 4.5:
                return 'Excellent'
            elif rating >= 4.0:
                return 'Good'
            elif rating >= 3.0:
                return 'Average'
            else:
                return 'Poor'

        df['Rating_Category'] = df['Avg_Rating'].apply(categorize_rating)

        print("   Created: Avg_Rating, Rating_Category")
    else:
        print(f"   ⚠️ Missing rating columns. Driver: {has_driver_rating}, Customer: {has_customer_rating}")

    return df


def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run all feature engineering steps.

    Parameters:
        df (pd.DataFrame): Cleaned dataset.

    Returns:
        pd.DataFrame: Dataset with engineered features.
    """
    print("\n" + "=" * 60)
    print("⚙️  FEATURE ENGINEERING")
    print("=" * 60)

    df = extract_temporal_features(df)
    df = create_cancellation_features(df)
    df = create_revenue_features(df)
    df = create_operational_features(df)
    df = create_rating_features(df)

    print("\n✅ Feature engineering complete!")
    print(f"   Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    return df


if __name__ == "__main__":
    from src.data_loader import load_uber_data
    from src.preprocessing import clean_dataset

    df = load_uber_data()
    df_clean = clean_dataset(df)
    df_engineered = engineer_all_features(df_clean)

    from src.data_loader import save_processed_data
    save_processed_data(df_engineered, "data/processed/engineered_uber_data.csv")