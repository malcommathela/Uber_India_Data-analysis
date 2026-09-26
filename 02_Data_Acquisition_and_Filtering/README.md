# Stage 2 — Data Acquisition & Filtering

## Purpose
Document where the dataset came from and make every analytical filter explicit.

## Rules
- Never remove records merely to make the dataset match a documented count.
- Record the original row count before filtering.
- Document every filter and its reason.
- Invalid values are handled by Stage 4 validation; this stage is for acquisition-level selection only.
- If no analytical filtering is required, explicitly report that no rows were removed.

## Output
- Acquisition notes
- Filtering log
- Filtered dataset passed to Stage 3
