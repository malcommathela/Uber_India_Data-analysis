"""
model_utils.py
Machine learning utilities for predictive modeling (Stretch Goal).
Includes: cancellation prediction, booking value prediction, demand forecasting.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (classification_report, confusion_matrix, 
                             mean_absolute_error, mean_squared_error, r2_score,
                             accuracy_score, precision_score, recall_score, f1_score)
import pickle
import os


def prepare_features(df: pd.DataFrame, target_col: str, feature_cols: list) -> tuple:
    """
    Prepare features for modeling by encoding categoricals and scaling numerics.

    Parameters:
        df (pd.DataFrame): Input dataset.
        target_col (str): Target column name.
        feature_cols (list): List of feature column names.

    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler, label_encoders)
    """
    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # Handle categorical columns
    label_encoders = {}
    for col in X.select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

    # Fill any remaining NaN
    X = X.fillna(X.median())

    # Scale numeric features
    scaler = StandardScaler()
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() <= 10 else None
    )

    return X_train, X_test, y_train, y_test, scaler, label_encoders


def train_cancellation_predictor(df: pd.DataFrame, save_model: bool = False) -> dict:
    """
    Train models to predict ride cancellation.

    Parameters:
        df (pd.DataFrame): Dataset with engineered features.
        save_model (bool): Whether to save the best model.

    Returns:
        dict: Model performance metrics and trained models.
    """
    print("\n" + "=" * 60)
    print("🤖 TRAINING CANCELLATION PREDICTION MODEL")
    print("=" * 60)

    # Feature selection
    feature_cols = [
        'Vehicle Type', 'Booking Value', 'Ride Distance', 'Avg VTAT', 'Avg CTAT',
        'Booking_Hour', 'Is_Weekend', 'Time_of_Day', 'Wait_Time_Category', 
        'Distance_Category', 'Payment Method'
    ]

    # Only use columns that exist
    feature_cols = [col for col in feature_cols if col in df.columns]

    if 'Is_Cancelled' not in df.columns:
        print("⚠️  'Is_Cancelled' not found. Run feature engineering first.")
        return {}

    X_train, X_test, y_train, y_test, scaler, encoders = prepare_features(
        df, 'Is_Cancelled', feature_cols
    )

    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
    }

    results = {}

    for name, model in models.items():
        print(f"\n📊 Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'predictions': y_pred
        }

        print(f"   Accuracy:  {accuracy:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall:    {recall:.4f}")
        print(f"   F1-Score:  {f1:.4f}")

    # Find best model
    best_model_name = max(results, key=lambda x: results[x]['f1_score'])
    print(f"\n🏆 Best Model: {best_model_name} (F1: {results[best_model_name]['f1_score']:.4f})")

    # Feature importance (for tree-based models)
    if hasattr(results[best_model_name]['model'], 'feature_importances_'):
        importances = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': results[best_model_name]['model'].feature_importances_
        }).sort_values('Importance', ascending=False)
        print("\n📈 Top 5 Important Features:")
        print(importances.head().to_string(index=False))

    # Save model
    if save_model:
        os.makedirs("outputs/models", exist_ok=True)
        filepath = "outputs/models/cancellation_predictor.pkl"
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': results[best_model_name]['model'],
                'scaler': scaler,
                'encoders': encoders,
                'feature_cols': feature_cols
            }, f)
        print(f"\n💾 Model saved to: {filepath}")

    return results


def train_booking_value_predictor(df: pd.DataFrame, save_model: bool = False) -> dict:
    """
    Train models to predict booking value (regression).

    Parameters:
        df (pd.DataFrame): Dataset with engineered features.
        save_model (bool): Whether to save the best model.

    Returns:
        dict: Model performance metrics.
    """
    print("\n" + "=" * 60)
    print("🤖 TRAINING BOOKING VALUE PREDICTION MODEL")
    print("=" * 60)

    feature_cols = [
        'Vehicle Type', 'Ride Distance', 'Avg VTAT', 'Avg CTAT',
        'Booking_Hour', 'Is_Weekend', 'Time_of_Day', 'Distance_Category',
        'Payment Method'
    ]
    feature_cols = [col for col in feature_cols if col in df.columns]

    if 'Booking Value' not in df.columns:
        print("⚠️  'Booking Value' not found.")
        return {}

    X_train, X_test, y_train, y_test, scaler, encoders = prepare_features(
        df, 'Booking Value', feature_cols
    )

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }

    results = {}

    for name, model in models.items():
        print(f"\n📊 Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            'model': model,
            'mae': mae,
            'rmse': rmse,
            'r2_score': r2
        }

        print(f"   MAE:  ₹{mae:.2f}")
        print(f"   RMSE: ₹{rmse:.2f}")
        print(f"   R²:   {r2:.4f}")

    best_model_name = max(results, key=lambda x: results[x]['r2_score'])
    print(f"\n🏆 Best Model: {best_model_name} (R²: {results[best_model_name]['r2_score']:.4f})")

    if save_model:
        os.makedirs("outputs/models", exist_ok=True)
        filepath = "outputs/models/booking_value_predictor.pkl"
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': results[best_model_name]['model'],
                'scaler': scaler,
                'encoders': encoders,
                'feature_cols': feature_cols
            }, f)
        print(f"\n💾 Model saved to: {filepath}")

    return results


if __name__ == "__main__":
    print("🤖 Model utilities loaded. Import functions in your notebooks.")
    print("Available functions:")
    print("  - train_cancellation_predictor(df, save_model=True)")
    print("  - train_booking_value_predictor(df, save_model=True)")
