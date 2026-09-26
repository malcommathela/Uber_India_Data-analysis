"""Stage 7: generate visualizations from the engineered analytical dataset."""
from pathlib import Path
import pandas as pd
from src.visualization import (
    plot_booking_trends,
    plot_cancellation_analysis,
    plot_revenue_analysis,
    plot_rating_analysis,
    plot_operational_metrics,
)

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "03_Data_Extraction" / "extracted_dataset.csv"

df = pd.read_csv(INPUT)
plot_booking_trends(df, save=True)
plot_cancellation_analysis(df, save=True)
plot_revenue_analysis(df, save=True)
plot_rating_analysis(df, save=True)
plot_operational_metrics(df, save=True)
print("Visualization stage complete.")
