# Stage 1 — Data Loading & Reading

## Purpose
Load the raw Uber India 2024 dataset and establish a reproducible baseline before any transformation.

## Required checks
- Confirm the source file exists at `data/raw/uber_data_india_2024.csv`.
- Record row and column counts from the actual file.
- Inspect column names and data types.
- Profile missing values and exact duplicate rows.
- Profile categorical distributions and numeric ranges.
- Save the raw profile for later comparison.

**Important:** The pipeline does not hard-code the expected record count. The actual dataset loaded is the source of truth.

## Output
The stage produces a baseline data profile used by Stages 2–4.
