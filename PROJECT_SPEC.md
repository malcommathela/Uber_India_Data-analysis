# Uber Data India (2024) — Capstone Project
## Project Specification & Review-1 Documentation

**Project Title:** Reducing Ride Cancellations and Improving Operational Efficiency: A Data Analysis of Uber Ride Bookings in India (2024)  
**Review Date:** 5/7/26 (Team 8–17)  
**Environment:** PyCharm + Python + Jupyter  
**Status:** Review-2 Eight-Stage Pipeline Refactor

---

## 1. Problem Statement

The rapid growth of ride-hailing platforms has transformed urban transportation in India. However, ride cancellations, inefficient fleet allocation, and inconsistent customer experiences remain critical operational challenges that directly impact revenue and customer retention.

This project analyzes the **Uber Data India (2024) dataset containing the actual records present in the submitted source dataset ride bookings** to uncover patterns in booking success, cancellations, vehicle usage, trip distances, payment methods, ratings, and revenue generation. The analysis aims to identify the root causes of cancellations, discover high-demand periods, evaluate vehicle category performance, and provide data-driven recommendations to reduce cancellations and improve operational efficiency.

**Core Research Question:** *What factors drive ride cancellations and operational inefficiencies in Uber's India operations, and how can data analytics inform strategies to reduce cancellations and optimize fleet allocation?*

---

## 2. Objectives

1. **Data Preparation & Quality Assurance**
   - Clean the Uber dataset (the actual records present in the submitted source dataset records) by handling missing values, duplicates, and inconsistent formatting.
   - Engineer features: booking success rate, cancellation flags, revenue per km, time-based bins (hour, day, month), waiting time categories.

2. **Exploratory Data Analysis (EDA)**
   - Analyse booking trends (daily, monthly, hourly, weekday vs. weekend).
   - Examine vehicle type popularity, average fares, and trip distances.
   - Visualise revenue distribution by vehicle and payment method.

3. **Cancellation Analysis**
   - Calculate overall cancellation rate and compare customer vs. driver cancellations.
   - Identify top cancellation reasons and vehicle types with highest cancellation rates.
   - Analyse temporal patterns of cancellations (peak hours, days).

4. **Revenue & Performance Analysis**
   - Determine which vehicle type generates the highest revenue.
   - Calculate average booking value and revenue contribution by payment method.
   - Evaluate revenue trends over time.

5. **Rating & Customer Satisfaction Analysis**
   - Analyse customer and driver rating distributions by vehicle type.
   - Examine correlation between trip distance, waiting time, and ratings.
   - Identify factors affecting customer satisfaction.

6. **Operational Efficiency Analysis**
   - Compute average ride distance, trip duration (CTAT), and driver arrival time (VTAT).
   - Identify high-demand pickup/drop locations and frequent routes.
   - Recommend strategies for fleet allocation and driver positioning.

---

## 3. Dataset Details

| Attribute | Value |
|-----------|-------|
| **Source** | Uber Data India (2024) — Kaggle / Internal Dataset |
| **Total Records** | the actual records present in the submitted source dataset ride bookings |
| **Time Period** | 2024 (full year) |
| **File Location** | `data/raw/uber_data_india_2024.csv` |

### Key Columns

| Column | Description | Type |
|--------|-------------|------|
| Date | Booking date | datetime |
| Time | Booking time | datetime |
| Booking ID | Unique identifier | string |
| Booking Status | Completed / Cancelled / Incomplete | categorical |
| Customer ID | Unique customer identifier | string |
| Vehicle Type | Auto, Sedan, SUV, Bike, etc. | categorical |
| Pickup Location | Origin location | string |
| Drop Location | Destination location | string |
| Avg VTAT | Average Vehicle Turnaround Time (driver arrival time) | numeric |
| Avg CTAT | Average Customer Turnaround Time (trip duration) | numeric |
| Customer Cancellation | Yes / No | boolean |
| Customer Cancellation Reason | Reason text | string |
| Driver Cancellation | Yes / No | boolean |
| Driver Cancellation Reason | Reason text | string |
| Incomplete Ride | Yes / No | boolean |
| Incomplete Ride Reason | Reason text | string |
| Booking Value | Ride fare amount | numeric |
| Ride Distance | Distance in km | numeric |
| Driver Rating | Rating given to driver (1–5) | numeric |
| Customer Rating | Rating given by driver (1–5) | numeric |
| Payment Method | Cash, UPI, Card, Wallet | categorical |

### Dataset Rationale
- **Operational Depth:** Covers complete ride lifecycle — booking, cancellation, completion, payment, and ratings.
- **Business Relevance:** Directly addresses real Uber operational challenges in the Indian market.
- **Analytical Richness:** Supports EDA, statistical analysis, geospatial analysis, and predictive modeling.

---

## 4. Tech Stack

| Category | Tools / Libraries | Purpose |
|----------|------------------|---------|
| **IDE** | PyCharm (Professional Edition recommended) | Development environment |
| **Language** | Python 3.11+ | Core programming |
| **Notebook** | Jupyter (via PyCharm) | Interactive analysis |
| **Data Manipulation** | pandas, NumPy | Data loading, cleaning, transformation |
| **Visualisation** | matplotlib, seaborn, Plotly | Static & interactive charts |
| **Statistics** | scipy, statsmodels | Hypothesis testing, ANOVA, regression |
| **Machine Learning** | scikit-learn | Predictive models (stretch goal) |
| **Dashboard** | Plotly Dash / Streamlit | Interactive dashboard |
| **Environment** | venv | Dependency isolation |

**Working Environment:** PyCharm with Jupyter plugin, Python virtual environment activated.

---

## 5. Implementation Plan

```
Phase 1: Data Ingestion
    └── Load Uber dataset (the actual records present in the submitted source dataset records) into pandas DataFrame

Phase 2: Data Cleaning & Preprocessing
    └── Handle missing values → Remove duplicates → Fix data types
    └── Standardise timestamps → Extract temporal features (hour, day, month, weekday)
    └── Engineer features: cancellation flag, revenue per km, waiting time category

Phase 3: Exploratory Data Analysis (EDA)
    └── Booking trends: daily, monthly, hourly, weekday vs. weekend
    └── Vehicle analysis: popularity, average fare, trip distance
    └── Revenue analysis: by vehicle, payment method, over time
    └── Geographic analysis: top pickup/drop locations, frequent routes

Phase 4: Cancellation Analysis
    └── Overall cancellation rate → Customer vs. Driver comparison
    └── Cancellation reasons → Vehicle-type breakdown
    └── Temporal cancellation patterns → Peak hours/days

Phase 5: Rating & Satisfaction Analysis
    └── Customer & driver rating distributions
    └── Ratings by vehicle type → Correlation with distance, waiting time
    └── Identify satisfaction drivers

Phase 6: Operational Efficiency Analysis
    └── Average ride distance, CTAT, VTAT distributions
    └── High-demand location identification
    └── Fleet allocation recommendations

Phase 7: Predictive Modeling (Stretch Goal)
    └── Ride Cancellation Prediction (Classification)
    └── Booking Value Prediction (Regression)
    └── Demand Forecasting by Hour/Day

Phase 8: Dashboard & Reporting
    └── Interactive dashboard with key KPIs
    └── Publication-quality visualisations
    └── Final report with business recommendations
```

**Current Stage:** Phase 2 (Data Cleaning & Preprocessing) — initial data loading complete, missing value analysis in progress.

---

## 6. Work Completed So Far

| Task | Status | Notes |
|------|--------|-------|
| Project folder structure created | ✅ Complete | All directories and starter files ready |
| Dataset downloaded | ✅ Complete | the actual records present in the submitted source dataset records in `data/raw/` |
| Virtual environment set up | ✅ Complete | `venv` created, dependencies installed |
| Initial data loading script | ✅ Complete | `src/data_loader.py` loads the dataset |
| Missing value analysis | 🔄 In Progress | Preliminary findings: ~X% missing in VTAT/CTAT |
| Data cleaning pipeline | 🔄 In Progress | Handling outliers in booking value and distance |
| EDA visualisations | ⏳ Pending | To begin after cleaning completion |
| Cancellation analysis | ⏳ Pending | Scheduled for next sprint |
| Revenue analysis | ⏳ Pending | After EDA completion |
| Predictive modeling | ⏳ Pending | Stretch goal for Review 2 |
| Dashboard development | ⏳ Pending | Final phase before submission |

---

## 7. Individual Contributions

| Member | Role | Contribution |
|--------|------|-------------|
| **Member 1** | Team Leader | Problem statement refinement, project scope definition, presentation structure, business narrative |
| **Member 2** | Data & Tech Lead | Dataset acquisition, tech stack selection, data loading scripts, preprocessing pipeline |
| **Member 3** | Implementation Lead | Notebook development, EDA visualisations, cancellation analysis, workflow implementation |
| **Member 4** | QA & Strategy | Code review, challenge documentation, next-step planning, dashboard design, model evaluation strategy |

---

## 8. Challenges Faced

1. **Missing Values:** VTAT and CTAT columns have missing values for cancelled/incomplete rides. Strategy: impute with median for completed rides; flag as "N/A" for cancelled rides.
2. **Outliers in Booking Value:** Some extreme fare values distort averages. Strategy: use IQR method to cap outliers; report median alongside mean.
3. **Inconsistent Location Names:** Pickup/drop locations have spelling variations and inconsistent formatting. Strategy: standardise text, group similar locations, use fuzzy matching for top locations.
4. **Temporal Feature Extraction:** Date and Time columns need parsing and feature engineering. Strategy: convert to datetime, extract hour, day, month, weekday, and create time-of-day categories.
5. **Cancellation Reason Categorisation:** Free-text cancellation reasons need grouping into standard categories. Strategy: keyword-based grouping + manual review of top reasons.
6. **Computational Limits:** 148K records with geospatial analysis can be slow. Strategy: use vectorised pandas operations; sample for initial prototyping.

---

## 9. Next Steps (Before Review 2)

- [ ] Complete data cleaning and feature engineering pipeline
- [ ] Finish EDA with booking trends, vehicle analysis, and revenue visualisations
- [ ] Complete cancellation analysis with customer vs. driver breakdown
- [ ] Perform rating and satisfaction analysis
- [ ] Conduct operational efficiency analysis (VTAT, CTAT, distance)
- [ ] Build baseline predictive models (Cancellation Prediction)
- [ ] Develop interactive dashboard (Plotly Dash / Streamlit)
- [ ] Prepare Review-2 presentation with live demo capability

---

## 10. File Structure

```
uber-data-india-analysis/
├── data/
│   ├── raw/
│   │   └── uber_data_india_2024.csv
│   └── processed/
│       └── cleaned_uber_data.csv
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_booking_trends.ipynb
│   ├── 03_cancellation_analysis.ipynb
│   ├── 04_revenue_and_ratings.ipynb
│   ├── 05_operational_efficiency.ipynb
│   └── 06_predictive_modeling.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── visualization.py
│   └── model_utils.py
├── outputs/
│   ├── figures/
│   └── models/
├── dashboard/
│   └── app.py
├── reports/
│   └── review1_presentation.pptx
├── requirements.txt
├── README.md
└── PROJECT_SPEC.md          ← You are here
```

---

## 11. Quick Commands (PyCharm Terminal)

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter in PyCharm
# Right-click any .ipynb file → "Open in" → "Jupyter"
# Or use PyCharm's built-in Jupyter notebook support

# Run data loader
python src/data_loader.py

# Launch dashboard (after development)
python dashboard/app.py
```

---

## 12. PyCharm Setup Guide

### Setting Up the Project in PyCharm

1. **Open Project:**
   - File → Open → Select `uber-data-india-analysis` folder

2. **Configure Python Interpreter:**
   - File → Settings → Project → Python Interpreter
   - Click gear icon → Add → Virtualenv Environment → Existing
   - Select `venv/Scripts/python.exe` (Windows) or `venv/bin/python` (Mac/Linux)

3. **Install Jupyter Plugin (if not present):**
   - File → Settings → Plugins → Search "Jupyter" → Install
   - Restart PyCharm

4. **Mark `src` as Sources Root:**
   - Right-click `src` folder → Mark Directory as → Sources Root
   - This allows `from src.data_loader import ...` to work

5. **Run Notebooks:**
   - Double-click any `.ipynb` file in the Project panel
   - PyCharm will open it with built-in Jupyter support
   - Select your venv kernel when prompted

6. **Run Python Scripts:**
   - Right-click any `.py` file → Run
   - Or use the green play button in the gutter

---

## 13. Expected Deliverables

| Deliverable | Description | Status |
|-------------|-------------|--------|
| Cleaned Dataset | Preprocessed, analysis-ready data | In Progress |
| EDA Report | 20–30 visualisations with insights | Pending |
| Statistical Summary | Descriptive stats, hypothesis tests | Pending |
| Cancellation Analysis Report | Root cause analysis of cancellations | Pending |
| Interactive Dashboard | KPI dashboard with filters | Pending |
| Predictive Models | Cancellation prediction, demand forecasting | Stretch Goal |
| Final Report | Business recommendations & insights | Pending |

---

*Document Version: 1.1*  
*Last Updated: 2026-08-01*  
*Project: Uber Data India (2024) Analysis*  
*IDE: PyCharm*


---

## 9. Review-2 Eight-Stage Dataset Pipeline

The implementation now follows the mandatory submission stages:

1. Data Loading & Reading
2. Data Acquisition & Filtering
3. Data Extraction
4. Data Validation & Cleaning
5. Data Aggregation & Representation
6. Data Analysis
7. Data Visualization
8. Results & Interpretation

### Data-quality decisions

- The actual source dataset is authoritative; record counts are never hard-coded.
- Customer cancellation, driver cancellation, no-driver-found and incomplete outcomes are reported separately.
- Ratings, VTAT and CTAT are not median-imputed because missingness can be structural.
- Booking Value and Ride Distance outliers are flagged rather than silently capped.
- Revenue analysis uses completed rides for realized booking-value summaries.
- Rating analysis reports observed-rating coverage.
- Every reported rate must state its denominator.

Run the complete pipeline from the repository root with:

```bash
python run_pipeline.py
```
