"""
data_loader.py
Handles loading and initial inspection of the Uber Data India (2024) dataset.
"""
import numpy as np
import pandas as pd
import os


def load_uber_data(filepath: str = None) -> pd.DataFrame:
    """
    Load the Uber dataset from the specified CSV file.

    Parameters:
        filepath (str): Path to the CSV file. If None, tries common locations.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    # Try common paths if none provided
    if filepath is None:
        possible_paths = [
            "data/raw/uber_data_india_2024.csv",
            "../data/raw/uber_data_india_2024.csv",
            "../../data/raw/uber_data_india_2024.csv",
            "uber_data_india_2024.csv",
            "../uber_data_india_2024.csv",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                filepath = path
                break

    if filepath is None or not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset not found. Please place the file at one of these locations:"
            f"  - data/raw/uber_data_india_2024.csv"
            f"  - uber_data_india_2024.csv (project root)"
            f"Or specify the full path: load_uber_data('your/path/file.csv')"
        )

    df = pd.read_csv(filepath)
    print(f"✅ Dataset loaded successfully from: {filepath}")
    print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """
    Perform initial inspection of the dataset.

    Parameters:
        df (pd.DataFrame): The dataset to inspect.
    """
    print("\n" + "=" * 60)
    print("📊 DATASET OVERVIEW")
    print("=" * 60)

    print(f"\nShape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    print("\n📋 Column Names & Data Types:")
    print(df.dtypes.to_string())

    print("\n🔍 Missing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0]
    if len(missing_df) > 0:
        print(missing_df.to_string())
    else:
        print("   No missing values found!")

    print(f"\n🔄 Duplicate Rows: {df.duplicated().sum()}")

    print("\n📈 Numeric Columns Summary:")
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) > 0:
        print(numeric_df.describe().round(2).to_string())
    else:
        print("   No numeric columns found.")

    print("\n📊 Categorical Columns (Top 5 Values):")
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        print(f"\n  {col}:")
        top5 = df[col].value_counts().head(5)
        for val, count in top5.items():
            pct = count / len(df) * 100
            print(f"    {val}: {count:,} ({pct:.1f}%)")


def save_processed_data(df: pd.DataFrame, filepath: str = "data/processed/cleaned_uber_data.csv") -> None:
    """
    Save processed DataFrame to CSV.

    Parameters:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): Output file path.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"\n💾 Processed data saved to: {filepath}")
    print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")


if __name__ == "__main__":
    df = load_uber_data()
    inspect_data(df)