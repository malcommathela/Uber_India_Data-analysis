"""
visualization.py
Reusable plotting functions for the Uber Data India (2024) analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List
import os

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def save_figure(filename: str, output_dir: str | None = None) -> None:
    """Save figure to the outputs directory."""
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "figures"))
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"💾 Figure saved: {filepath}")


def plot_booking_trends(df: pd.DataFrame, save: bool = False) -> None:
    """
    Plot booking trends over time.

    Includes: monthly bookings, hourly demand, weekday vs weekend.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Monthly bookings
    if 'Booking_Month' in df.columns:
        month_order = list(range(1, 13))
        monthly = pd.to_numeric(df['Booking_Month'], errors='coerce').dropna().astype(int).value_counts()
        monthly = monthly.reindex(month_order, fill_value=0)
        monthly.index = pd.Index(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        if monthly.sum() > 0:
            monthly.plot(kind='bar', ax=axes[0], color='steelblue')
        else:
            axes[0].text(0.5, 0.5, 'No monthly booking data', ha='center', va='center', transform=axes[0].transAxes)
        axes[0].set_title('Monthly Bookings', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Month')
        axes[0].set_ylabel('Number of Bookings')
        axes[0].tick_params(axis='x', rotation=45)
    else:
        axes[0].text(0.5, 0.5, 'Booking_Month not found', ha='center', va='center', transform=axes[0].transAxes)
        axes[0].set_title('Monthly Bookings — Data Unavailable')

    # Hourly demand
    if 'Booking_Hour' in df.columns:
        hourly = df['Booking_Hour'].value_counts().sort_index()
        hourly.plot(kind='line', ax=axes[1], marker='o', color='coral')
        axes[1].set_title('Hourly Ride Demand', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Hour of Day')
        axes[1].set_ylabel('Number of Bookings')
        axes[1].grid(True, alpha=0.3)
    else:
        axes[1].text(0.5, 0.5, 'Booking_Hour not found', ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('Hourly Demand — Data Unavailable')

    # Weekday vs Weekend
    if 'Is_Weekend' in df.columns:
        weekend_counts = df['Is_Weekend'].value_counts()
        labels = ['Weekday', 'Weekend']
        values = [weekend_counts.get(False, 0), weekend_counts.get(True, 0)]
        axes[2].pie(values, labels=labels, autopct='%1.1f%%',
                    colors=['lightblue', 'lightcoral'], startangle=90)
        axes[2].set_title('Weekday vs Weekend Bookings', fontsize=12, fontweight='bold')
    else:
        axes[2].text(0.5, 0.5, 'Is_Weekend not found', ha='center', va='center', transform=axes[2].transAxes)
        axes[2].set_title('Weekday vs Weekend — Data Unavailable')

    plt.tight_layout()
    if save:
        save_figure("booking_trends.png")
    plt.show()


def plot_cancellation_analysis(df: pd.DataFrame, save: bool = False) -> None:
    """
    Plot cancellation analysis.

    Includes: overall cancellation rate, customer vs driver, reasons, by vehicle.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Overall cancellation rate
    if 'Is_Cancelled' in df.columns:
        cancel_counts = df['Is_Cancelled'].value_counts()
        labels = ['Completed', 'Cancelled']
        values = [cancel_counts.get(False, 0), cancel_counts.get(True, 0)]
        colors = ['#2ecc71', '#e74c3c']
        axes[0, 0].pie(values, labels=labels, autopct='%1.1f%%',
                       colors=colors, startangle=90)
        axes[0, 0].set_title('Overall Cancellation Rate', fontsize=12, fontweight='bold')
    else:
        axes[0, 0].text(0.5, 0.5, 'Is_Cancelled not found', ha='center', va='center', transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('Cancellation Rate — Data Unavailable')

    # Customer vs Driver cancellations
    if 'Cancellation_Type' in df.columns:
        cancel_type = df['Cancellation_Type'].value_counts()
        if len(cancel_type) > 0:
            colors_map = {'None': '#95a5a6', 'Customer': '#3498db', 'Driver': '#e74c3c', 'Both': '#f39c12'}
            bar_colors = [colors_map.get(str(x), 'gray') for x in cancel_type.index]
            cancel_type.plot(kind='bar', ax=axes[0, 1], color=bar_colors)
            axes[0, 1].set_title('Cancellation Type Breakdown', fontsize=12, fontweight='bold')
            axes[0, 1].set_xlabel('Cancellation Type')
            axes[0, 1].set_ylabel('Count')
            axes[0, 1].tick_params(axis='x', rotation=45)
        else:
            axes[0, 1].text(0.5, 0.5, 'No cancellation data', ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('Cancellation Type — No Data')
    else:
        axes[0, 1].text(0.5, 0.5, 'Cancellation_Type not found', ha='center', va='center', transform=axes[0, 1].transAxes)
        axes[0, 1].set_title('Cancellation Type — Data Unavailable')

    # Top cancellation reasons (Customer)
    if 'Customer Cancellation Reason' in df.columns:
        reasons = df[df['Customer Cancellation Reason'] != 'Not Cancelled']['Customer Cancellation Reason'].value_counts().head(8)
        if len(reasons) > 0:
            reasons.plot(kind='barh', ax=axes[1, 0], color='salmon')
            axes[1, 0].set_title('Top Customer Cancellation Reasons', fontsize=12, fontweight='bold')
            axes[1, 0].set_xlabel('Count')
        else:
            axes[1, 0].text(0.5, 0.5, 'No cancellation reasons found', ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Cancellation Reasons — No Data')
    else:
        axes[1, 0].text(0.5, 0.5, 'Customer Cancellation Reason not found', ha='center', va='center', transform=axes[1, 0].transAxes)
        axes[1, 0].set_title('Cancellation Reasons — Data Unavailable')

    # Cancellation rate by vehicle type
    if 'Vehicle Type' in df.columns and 'Is_Cancelled' in df.columns:
        cancel_by_vehicle = df.groupby('Vehicle Type')['Is_Cancelled'].mean().sort_values(ascending=False)
        if len(cancel_by_vehicle) > 0:
            cancel_by_vehicle.plot(kind='bar', ax=axes[1, 1], color='indianred')
            axes[1, 1].set_title('Cancellation Rate by Vehicle Type', fontsize=12, fontweight='bold')
            axes[1, 1].set_xlabel('Vehicle Type')
            axes[1, 1].set_ylabel('Cancellation Rate')
            axes[1, 1].tick_params(axis='x', rotation=45)
        else:
            axes[1, 1].text(0.5, 0.5, 'No vehicle data', ha='center', va='center', transform=axes[1, 1].transAxes)
    else:
        axes[1, 1].text(0.5, 0.5, 'Required columns not found', ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Cancellation by Vehicle — Data Unavailable')

    plt.tight_layout()
    if save:
        save_figure("cancellation_analysis.png")
    plt.show()


def plot_revenue_analysis(df: pd.DataFrame, save: bool = False) -> None:
    """
    Plot revenue analysis.

    Includes: revenue by vehicle, payment method, distribution.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Revenue by vehicle type
    if 'Vehicle Type' in df.columns and 'Booking Value' in df.columns:
        revenue_df = df[df['Is_Completed'] == True] if 'Is_Completed' in df.columns else df
        revenue_by_vehicle = revenue_df.groupby('Vehicle Type')['Booking Value'].sum().sort_values(ascending=False)
        if len(revenue_by_vehicle) > 0:
            revenue_by_vehicle.plot(kind='bar', ax=axes[0], color='mediumseagreen')
            axes[0].set_title('Total Revenue by Vehicle Type', fontsize=12, fontweight='bold')
            axes[0].set_xlabel('Vehicle Type')
            axes[0].set_ylabel('Total Revenue (₹)')
            axes[0].tick_params(axis='x', rotation=45)
        else:
            axes[0].text(0.5, 0.5, 'No revenue data', ha='center', va='center', transform=axes[0].transAxes)
    else:
        axes[0].text(0.5, 0.5, 'Required columns not found', ha='center', va='center', transform=axes[0].transAxes)
        axes[0].set_title('Revenue by Vehicle — Data Unavailable')

    # Revenue by payment method
    if 'Payment Method' in df.columns and 'Booking Value' in df.columns:
        revenue_df = df[df['Is_Completed'] == True] if 'Is_Completed' in df.columns else df
        revenue_by_payment = revenue_df.groupby('Payment Method')['Booking Value'].sum().sort_values(ascending=False)
        if len(revenue_by_payment) > 0:
            revenue_by_payment.plot(kind='bar', ax=axes[1], color='mediumpurple')
            axes[1].set_title('Revenue by Payment Method', fontsize=12, fontweight='bold')
            axes[1].set_xlabel('Payment Method')
            axes[1].set_ylabel('Total Revenue (₹)')
            axes[1].tick_params(axis='x', rotation=45)
        else:
            axes[1].text(0.5, 0.5, 'No payment data', ha='center', va='center', transform=axes[1].transAxes)
    else:
        axes[1].text(0.5, 0.5, 'Required columns not found', ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('Revenue by Payment — Data Unavailable')

    # Booking value distribution
    if 'Booking Value' in df.columns:
        revenue_df = df[df['Is_Completed'] == True] if 'Is_Completed' in df.columns else df
        data = revenue_df['Booking Value'].dropna()
        if len(data) > 0:
            axes[2].hist(data, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
            axes[2].set_title('Booking Value Distribution', fontsize=12, fontweight='bold')
            axes[2].set_xlabel('Booking Value (₹)')
            axes[2].set_ylabel('Frequency')
            mean_val = data.mean()
            median_val = data.median()
            axes[2].axvline(mean_val, color='red', linestyle='--', label=f'Mean: ₹{mean_val:.2f}')
            axes[2].axvline(median_val, color='green', linestyle='--', label=f'Median: ₹{median_val:.2f}')
            axes[2].legend()
        else:
            axes[2].text(0.5, 0.5, 'No fare data', ha='center', va='center', transform=axes[2].transAxes)
    else:
        axes[2].text(0.5, 0.5, 'Booking Value not found', ha='center', va='center', transform=axes[2].transAxes)
        axes[2].set_title('Fare Distribution — Data Unavailable')

    plt.tight_layout()
    if save:
        save_figure("revenue_analysis.png")
    plt.show()


def plot_rating_analysis(df: pd.DataFrame, save: bool = False) -> None:
    """
    Plot rating analysis.

    Includes: customer rating distribution, driver rating distribution, by vehicle.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Customer rating distribution
    if 'Customer Rating' in df.columns:
        data = df['Customer Rating'].dropna()
        if len(data) > 0:
            axes[0].hist(data, bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
            axes[0].set_title('Customer Rating Distribution', fontsize=12, fontweight='bold')
            axes[0].set_xlabel('Rating')
            axes[0].set_ylabel('Frequency')
            mean_val = data.mean()
            axes[0].axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
            axes[0].legend()
        else:
            axes[0].text(0.5, 0.5, 'No rating data', ha='center', va='center', transform=axes[0].transAxes)
    else:
        axes[0].text(0.5, 0.5, 'Customer Rating not found', ha='center', va='center', transform=axes[0].transAxes)
        axes[0].set_title('Customer Ratings — Data Unavailable')

    # Driver rating distribution
    if 'Driver Rating' in df.columns:
        data = df['Driver Rating'].dropna()
        if len(data) > 0:
            axes[1].hist(data, bins=20, color='lightsalmon', edgecolor='black', alpha=0.7)
            axes[1].set_title('Driver Rating Distribution', fontsize=12, fontweight='bold')
            axes[1].set_xlabel('Rating')
            axes[1].set_ylabel('Frequency')
            mean_val = data.mean()
            axes[1].axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
            axes[1].legend()
        else:
            axes[1].text(0.5, 0.5, 'No rating data', ha='center', va='center', transform=axes[1].transAxes)
    else:
        axes[1].text(0.5, 0.5, 'Driver Rating not found', ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('Driver Ratings — Data Unavailable')

    # Ratings by vehicle type
    if 'Vehicle Type' in df.columns and 'Customer Rating' in df.columns:
        rating_by_vehicle = df.groupby('Vehicle Type')['Customer Rating'].mean().sort_values(ascending=False)
        if len(rating_by_vehicle) > 0:
            rating_by_vehicle.plot(kind='bar', ax=axes[2], color='gold')
            axes[2].set_title('Avg Customer Rating by Vehicle Type', fontsize=12, fontweight='bold')
            axes[2].set_xlabel('Vehicle Type')
            axes[2].set_ylabel('Average Rating')
            axes[2].tick_params(axis='x', rotation=45)
            axes[2].set_ylim(0, 5)
        else:
            axes[2].text(0.5, 0.5, 'No vehicle rating data', ha='center', va='center', transform=axes[2].transAxes)
    else:
        axes[2].text(0.5, 0.5, 'Required columns not found', ha='center', va='center', transform=axes[2].transAxes)
        axes[2].set_title('Ratings by Vehicle — Data Unavailable')

    plt.tight_layout()
    if save:
        save_figure("rating_analysis.png")
    plt.show()


def plot_operational_metrics(df: pd.DataFrame, save: bool = False) -> None:
    """
    Plot operational metrics.

    Includes: ride distance distribution, CTAT distribution, VTAT distribution.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    metrics = [
        ('Ride Distance', 'Ride Distance Distribution', 'Distance (km)', 'steelblue'),
        ('Avg CTAT', 'Trip Duration (CTAT) Distribution', 'Duration (min)', 'coral'),
        ('Avg VTAT', 'Driver Arrival Time (VTAT) Distribution', 'Time (min)', 'mediumseagreen')
    ]

    for idx, (col, title, xlabel, color) in enumerate(metrics):
        if col in df.columns:
            data = df[col].dropna()
            if len(data) > 0:
                axes[idx].hist(data, bins=50, color=color, edgecolor='black', alpha=0.7)
                axes[idx].set_title(title, fontsize=12, fontweight='bold')
                axes[idx].set_xlabel(xlabel)
                axes[idx].set_ylabel('Frequency')
                mean_val = data.mean()
                axes[idx].axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
                axes[idx].legend()
            else:
                axes[idx].text(0.5, 0.5, f'No data for {col}', ha='center', va='center', transform=axes[idx].transAxes)
        else:
            axes[idx].text(0.5, 0.5, f'{col} not found', ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].set_title(f'{title} — Data Unavailable')

    plt.tight_layout()
    if save:
        save_figure("operational_metrics.png")
    plt.show()


if __name__ == "__main__":
    print("📊 Visualization module loaded. Import functions in your notebooks.")
    print("Available functions:")
    print("  - plot_booking_trends(df)")
    print("  - plot_cancellation_analysis(df)")
    print("  - plot_revenue_analysis(df)")
    print("  - plot_rating_analysis(df)")
    print("  - plot_operational_metrics(df)")
    print("\nUse save=True to save figures to outputs/figures/")