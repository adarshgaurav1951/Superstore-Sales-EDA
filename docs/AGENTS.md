# Agent Operational Guidelines (AGENTS.md)
## Superstore Sales - Exploratory Data Analysis & Modeling Standards

---

### 1. Repository Purpose & Architecture
This repository contains an end-to-end data analytics and business intelligence system for the classic **Superstore Sales** dataset. The objective is to produce reproducible data cleaning, rigorous feature engineering, comprehensive exploratory data analysis, and an executive-grade interactive Streamlit dashboard accompanied by strategic business recommendations.

---

### 2. File & Directory Conventions
- `data/raw/`: **Read-Only / Immutable.** Never mutate, overwrite, or reformat files in this directory.
- `data/cleaned/`: Houses processed datasets (`superstore_cleaned.csv`, `superstore_featured.csv`, `customer_rfm.csv`).
- `notebooks/`: Numbered, modular Jupyter notebooks (`01_cleaning.ipynb`, `02_features.ipynb`, `03_eda.ipynb`, `04_insights.ipynb`). Each notebook must be self-contained and run from top to bottom without errors.
- `dashboard/`: Streamlit dashboard code (`app.py`, components, styling).
- `visuals/`: High-resolution figures saved as PNGs (`300 DPI`) with transparent or themed backgrounds for reports and documentation.
- `docs/`: PRD, Database specification, Agent instructions, and project ideas.
- `reports/`: Executive and analytical reports in Markdown and PDF/HTML formats.

---

### 3. Data Science & Coding Standards

#### 3.1 Python Environment & Tooling
- Always execute Python within the local virtual environment: `.venv/bin/python`.
- Pin all packages in `requirements.txt`.
- Adhere to PEP 8 standards with descriptive variable and function naming.
- Use explicit type casting (e.g., `pd.to_datetime()`, `astype('category')`, `astype('int64')`).

#### 3.2 Data Integrity Rules
- **No Silent Dropping:** Never drop rows or columns without explicit justification and logging. For instance, do not drop rows with missing `Postal Code`; impute or flag them.
- **Handling Temporal Inconsistencies:** Validate that `Ship Date >= Order Date`. Flag or correct invalid instances.
- **Financial Metric Integrity:**
  - `Profit Margin = Profit / Sales` must guard against division by zero (e.g., `np.where(sales == 0, 0, profit / sales)`).
  - Clearly distinguish between gross revenue (`Sales`), net profit (`Profit`), and profit margin percentage.
- **Random State:** Always fix `random_state=42` across any statistical or machine learning operations (e.g., KMeans, train-test splits) for full reproducibility.

#### 3.3 Visual & Design Philosophy
- **Modern Palette:** Avoid default harsh colors. Use curated palettes:
  - Primary / Brand: Indigo (`#4F46E5`), Deep Navy (`#0F172A`), Slate (`#334155`)
  - Accent / Positive: Emerald (`#10B981`)
  - Warning / Attention: Amber (`#F59E0B`)
  - Negative / Loss: Rose / Crimson (`#EF4444`, `#DC2626`)
- **Chart Formatting:** Every chart must feature:
  - A clear, descriptive title stating the takeaway (not just the axis names).
  - Informative axis labels with appropriate units (\$, %, days).
  - Value annotations on key bars/points where readability is improved.
  - Consistent font families (e.g., Inter, sans-serif).

---

### 4. Interactive Dashboard Principles (Streamlit)
- Implement modular layouts with clear visual hierarchy:
  - KPI Cards on top with contextual delta values.
  - Interactive multi-select and slider filters in a collapsible sidebar.
  - Tabbed analytical views (Overview, Category & Product, Geography & Logistics, Customer RFM, Strategic Actions).
- Performance: Wrap data loading and expensive aggregations with `@st.cache_data`.
- Responsive UX: Support both dark and light modes cleanly via CSS styling.

---

### 5. Verification Checklist Before Marking Work Complete
- [ ] Raw data remains untouched in `data/raw/`.
- [ ] Cleaned and featured CSV files exist in `data/cleaned/` with validated row counts.
- [ ] All 4 notebooks run cleanly end-to-end without unhandled exceptions.
- [ ] Charts exported to `visuals/`.
- [ ] Streamlit dashboard runs smoothly on `localhost:8501` without rendering bugs.
- [ ] `README.md` documents setup, methodology, findings, and screenshots.
