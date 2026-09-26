# Stage 4 — Data Validation & Cleaning

## Purpose
Make the dataset analytically safe without manufacturing observations.

## Validation rules
- Parse dates/times and report unparseable values.
- Normalize text consistently.
- Normalize Yes/No/True/False cancellation flags.
- Validate ratings are within 1–5.
- Validate Booking Value and Ride Distance are non-negative.
- Preserve structural missingness for cancelled/incomplete rides.
- Do not median-impute ratings, VTAT, or CTAT.
- Do not cap outliers by default; create explicit outlier flags.
- Remove exact duplicate rows and report duplicate Booking IDs separately.
- Preserve an audit log of every transformation.

## Key principle
A missing rating on a cancelled ride is not a defective rating. It represents an event that did not occur.
