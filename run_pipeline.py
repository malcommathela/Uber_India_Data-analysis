"""Run the Review-2 eight-stage pipeline in order.

Usage:
    python run_pipeline.py
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent

STAGES = [
    "01_Data_Loading_and_Reading/load_and_profile.py",
    "02_Data_Acquisition_and_Filtering/filter_dataset.py",
    "04_Data_Validation_and_Cleaning/validate_and_clean.py",
    "03_Data_Extraction/extract_features.py",
    "05_Data_Aggregation_and_Representation/aggregate.py",
    "06_Data_Analysis/analyze.py",
    "07_Data_Visualization/generate_visualizations.py",
    "08_Results_and_Interpretation/generate_results.py",
]

for stage in STAGES:
    print("\n" + "=" * 72)
    print(f"RUNNING: {stage}")
    print("=" * 72)
    runpy.run_path(str(ROOT / stage), run_name="__main__")

print("\nEight-stage Review-2 pipeline completed.")
