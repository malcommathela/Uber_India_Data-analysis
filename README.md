# 🚗 Uber Data India (2024) — Data Analysis Capstone

**Project Title:** Reducing Ride Cancellations and Improving Operational Efficiency: A Data Analysis of Uber Ride Bookings in India (2024)

---

## 📋 Overview

This project analyzes **148,770 Uber ride bookings** from India (2024) to identify patterns in booking success, cancellations, vehicle usage, trip distances, payment methods, ratings, and revenue generation. The goal is to provide **data-driven recommendations** to reduce cancellations and improve operational efficiency.

---

## 🎯 Objectives

1. **Data Preparation & Quality Assurance** — Clean, integrate, and preprocess the dataset
2. **Exploratory Data Analysis (EDA)** — Booking trends, vehicle analysis, revenue patterns
3. **Cancellation Analysis** — Root cause analysis of ride cancellations
4. **Revenue & Performance Analysis** — Revenue by vehicle, payment method, and time
5. **Rating & Customer Satisfaction Analysis** — Driver/customer rating patterns
6. **Operational Efficiency Analysis** — VTAT, CTAT, distance, and fleet allocation insights
7. **Predictive Modeling** *(Stretch Goal)* — Cancellation prediction, booking value prediction

---

## 📁 Review-2 Eight-Stage Pipeline

The project is organized around the eight mandatory Capstone Review-2 stages:

```text
Uber_India_Data-analysis/
├── 01_Data_Loading_and_Reading/
├── 02_Data_Acquisition_and_Filtering/
├── 03_Data_Extraction/
├── 04_Data_Validation_and_Cleaning/
├── 05_Data_Aggregation_and_Representation/
├── 06_Data_Analysis/
├── 07_Data_Visualization/
├── 08_Results_and_Interpretation/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── outputs/
├── reports/
├── README.md
└── requirements.txt
```

### Pipeline order

1. **Data Loading & Reading** — establish the raw-data baseline.
2. **Data Acquisition & Filtering** — document provenance and explicit filters.
3. **Data Extraction** — derive temporal and analytical fields.
4. **Data Validation & Cleaning** — validate ranges, preserve structural missingness, and audit transformations.
5. **Data Aggregation & Representation** — produce reproducible KPI/summary tables.
6. **Data Analysis** — answer booking, cancellation, revenue, rating and operational questions.
7. **Data Visualization** — generate charts from the analytical tables.
8. **Results & Interpretation** — document evidence, interpretation, implications and limitations.

### Reproducibility rule

The actual dataset loaded from the raw-data directory is the source of truth. The repository previously contained a documentation discrepancy between **148,770** records and a notebook output of **150,000** rows. The refactored pipeline does not hard-code either value.

### Metric definitions

- **Cancellation:** customer or driver cancellation.
- **Unfulfilled:** `No Driver Found`; reported separately from cancellation.
- **Incomplete:** incomplete ride; reported separately.
- **Completion:** booking status indicates completed.
- **Rating metrics:** use observed ratings only; missing ratings are not median-imputed.
- **Revenue analysis:** completed rides are used for realized booking-value analysis.
- **Outliers:** flagged for review instead of silently capped.

---

## 🚀 Quick Start

### 1. Create Folder Structure

**Windows (Command Prompt):**
```cmd
mkdir uber-data-india-analysis\data\raw uber-data-india-analysis\data\processed uber-data-india-analysis\notebooks uber-data-india-analysis\src uber-data-india-analysis\outputs\figures uber-data-india-analysis\outputs\models uber-data-india-analysis\dashboard uber-data-india-analysis\reports
cd uber-data-india-analysis
echo.> src\__init__.py
```

**PowerShell:**
```powershell
$folders = "data/raw","data/processed","notebooks","src","outputs/figures","outputs/models","dashboard","reports"; $base = "uber-data-india-analysis"; New-Item -ItemType Directory -Path ($folders | ForEach-Object { Join-Path $base $_ }) -Force; New-Item -ItemType File -Path "$base/src/__init__.py" -Force
```

**Python (Any OS):**
```python
import os
folders = [
    "uber-data-india-analysis/data/raw",
    "uber-data-india-analysis/data/processed",
    "uber-data-india-analysis/notebooks",
    "uber-data-india-analysis/src",
    "uber-data-india-analysis/outputs/figures",
    "uber-data-india-analysis/outputs/models",
    "uber-data-india-analysis/dashboard",
    "uber-data-india-analysis/reports"
]
for f in folders: os.makedirs(f, exist_ok=True)
open("uber-data-india-analysis/src/__init__.py", 'a').close()
print("Done!")
```

### 2. Set Up Virtual Environment

```bash
cd uber-data-india-analysis
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Place Your Dataset

Copy your `uber_data_india_2024.csv` file into:
```
data/raw/uber_data_india_2024.csv
```

### 4. Run the Pipeline

```python
# In a Jupyter notebook or Python script
from src.data_loader import load_uber_data, inspect_data, save_processed_data
from src.preprocessing import clean_dataset
from src.feature_engineering import engineer_all_features

# Load
df = load_uber_data()

# Inspect
inspect_data(df)

# Clean
df_clean = clean_dataset(df)

# Engineer features
df_engineered = engineer_all_features(df_clean)

# Save
save_processed_data(df_engineered, "data/processed/engineered_uber_data.csv")
```

### 5. Generate Visualisations

```python
from src.visualization import *

plot_booking_trends(df_engineered, save=True)
plot_cancellation_analysis(df_engineered, save=True)
plot_revenue_analysis(df_engineered, save=True)
plot_rating_analysis(df_engineered, save=True)
plot_operational_metrics(df_engineered, save=True)
```

### 6. Train Models (Stretch Goal)

```python
from src.model_utils import train_cancellation_predictor, train_booking_value_predictor

# Cancellation prediction
results = train_cancellation_predictor(df_engineered, save_model=True)

# Booking value prediction
results = train_booking_value_predictor(df_engineered, save_model=True)
```

---

## 🛠️ PyCharm Setup Guide

### Step 1: Open the Project
- Launch PyCharm → **File → Open** → Select the `uber-data-india-analysis` folder

### Step 2: Configure Python Interpreter
- **File → Settings → Project: uber-data-india-analysis → Python Interpreter**
- Click the gear icon ⚙️ → **Add → Virtualenv Environment → Existing**
- Browse and select:
  - **Windows:** `venv\Scripts\python.exe`
  - **Mac/Linux:** `venv/bin/python`
- Click **OK**

### Step 3: Mark `src` as Sources Root
- In the Project panel (left side), right-click the `src` folder
- Select **Mark Directory as → Sources Root**
- This ensures PyCharm recognises imports like `from src.data_loader import ...`

### Step 4: Install Jupyter Plugin (if needed)
- **File → Settings → Plugins**
- Search for **"Jupyter"** → Install if not present
- Restart PyCharm

### Step 5: Working with Notebooks
- Double-click any `.ipynb` file in the Project panel
- PyCharm opens it with built-in Jupyter support
- When prompted, select your project interpreter (the venv you configured)
- Run cells using the green play button next to each cell

### Step 6: Working with Python Scripts
- Open any `.py` file in the editor
- Right-click in the editor → **Run** (or press the green play button ▶️ in the top-right)
- Output appears in the **Run** tool window at the bottom

### Step 7: Terminal Access
- Open the built-in terminal: **View → Tool Windows → Terminal** (or press `Alt+F12`)
- The terminal automatically activates your virtual environment
- Use it for pip installs, git commands, etc.

---

## 📊 Key Analyses

| Analysis | Description | Notebook |
|----------|-------------|----------|
| Booking Trends | Daily/monthly/hourly demand, weekday vs weekend | `02_eda_booking_trends.ipynb` |
| Cancellation Analysis | Rates, reasons, customer vs driver, by vehicle | `03_cancellation_analysis.ipynb` |
| Revenue Analysis | By vehicle, payment method, time trends | `04_revenue_and_ratings.ipynb` |
| Ratings Analysis | Customer/driver ratings, satisfaction drivers | `04_revenue_and_ratings.ipynb` |
| Operational Metrics | VTAT, CTAT, distance distributions | `05_operational_efficiency.ipynb` |
| Predictive Modeling | Cancellation & value prediction | `06_predictive_modeling.ipynb` |

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| IDE | PyCharm (Professional recommended for Jupyter support) |
| Language | Python 3.11+ |
| Notebooks | Jupyter (via PyCharm built-in support) |
| Data | pandas, NumPy |
| Visualisation | matplotlib, seaborn, Plotly |
| Statistics | scipy, statsmodels |
| ML | scikit-learn |
| Dashboard | Plotly Dash / Streamlit |

---

## 📈 Expected Deliverables

- [x] Cleaned dataset
- [ ] EDA with 20–30 visualisations
- [ ] Statistical summary & hypothesis tests
- [ ] Cancellation analysis report
- [ ] Interactive dashboard
- [ ] Predictive models *(Stretch Goal)*
- [ ] Final business recommendations report
- [ ] Review 1 & Review 2 presentations

---

## 👥 Team Roles (Review 1)

| Member | Role | Responsibility |
|--------|------|----------------|
| Member 1 | Team Leader | Problem statement, objectives, business narrative |
| Member 2 | Data & Tech Lead | Dataset, tech stack, preprocessing pipeline |
| Member 3 | Implementation Lead | EDA, visualisations, analysis notebooks |
| Member 4 | QA & Strategy | Challenges, next steps, dashboard, model evaluation |

---

## 📅 Timeline

| Phase | Status | Deadline |
|-------|--------|----------|
| Data Cleaning | 🔄 In Progress | Before Review 1 |
| EDA | ⏳ Pending | Before Review 2 |
| Cancellation Analysis | ⏳ Pending | Before Review 2 |
| Revenue & Ratings | ⏳ Pending | Before Review 2 |
| Operational Analysis | ⏳ Pending | Before Review 2 |
| Dashboard | ⏳ Pending | Final Submission |
| Predictive Models | ⏳ Pending | Stretch Goal |

---

## 📄 License

Academic project for Data Analysis Essentials Capstone.

---

*Last Updated: 2026-08-01*  
*IDE: PyCharm*
