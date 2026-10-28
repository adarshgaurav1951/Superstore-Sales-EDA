# Product Requirements Document (PRD)
## Superstore Sales - Exploratory Data Analysis & Business Intelligence Dashboard

---

### 1. Document Control
- **Project Name:** Superstore Sales EDA & Executive BI Solution
- **Version:** 1.0.0
- **Status:** Approved / Active
- **Target Audience:** Executive Leadership, Category Managers, Regional Sales Directors, Logistics Team, Data Analysts

---

### 2. Executive Summary & Problem Statement
The Superstore retail enterprise manages a nationwide omnichannel sales network across 4 primary geographical regions (East, West, Central, South), serving 3 customer segments (Consumer, Corporate, Home Office) across 3 overarching product categories (Technology, Furniture, Office Supplies) comprising 17 sub-categories.

Despite generating over \$2.29M in gross revenue across 9,994 transaction records, management faces severe visibility deficits:
1. **Profit Hemorrhage:** Multiple sub-categories and customer accounts generate substantial revenue while delivering net losses due to excessive promotional discounting.
2. **Regional Margin Variance:** Sharp disparities in regional profitability (notably deep losses in specific states despite strong gross volume).
3. **Operational Drag:** High fulfillment lead times in select shipping modes with negligible margin uplift.
4. **Actionability Gap:** Existing raw transactional tabular data cannot quickly answer executive queries about discount thresholds, customer lifetime profitability, or product discontinuation triggers.

---

### 3. Business Goals & Success Metrics

#### 3.1 Primary Goals
- **Audit & Cleanse Data:** Establish a single source of truth with zero data integrity anomalies, properly parsed temporal datatypes, validated transaction values, and documented handling of missing attributes.
- **Formulate Behavioral Feature Layer:** Derive financial indicators (Profit Margin %, Shipping Duration, Discount Buckets, Loss-making Flags) and Customer Analytics (Recency, Frequency, Monetary - RFM).
- **Diagnose Profit Drivers & Leaks:** Pinpoint exactly where margin erosion occurs by cross-analyzing category, geography, discount level, and shipping logistics.
- **Deliver Executive Dashboard:** Deploy an interactive web application (Streamlit) that enables self-service slicing, diagnostics, KPI tracking, and scenario exploration.
- **Synthesize Actionable Playbook:** Produce quantifiable commercial recommendations to boost company-wide profitability by at least 15-25% without sacrificing healthy market share.

#### 3.2 Success Metrics (KPIs)
| Metric Name | Business Definition | Target Benchmark / Health Indicator |
|---|---|---|
| **Gross Sales** | Sum of transaction sales revenue | Maintain continuous YoY growth |
| **Net Profit** | Sum of net margin after cost & discounts | Positive margin across all categories |
| **Profit Margin %** | $\frac{\text{Total Profit}}{\text{Total Sales}} \times 100$ | Target $\ge 12.0\%$ aggregate margin |
| **Loss-Making Order Rate** | $\frac{\text{Loss Orders Count}}{\text{Total Orders}} \times 100$ | Reduce below $10\%$ (historically ~18-20%) |
| **Average Discount Level** | Mean discount rate applied per item | Guardrail under $15\%$ ceiling |
| **On-Time Fulfillment Lead Time** | Mean days from Order Date to Ship Date | $\le 4$ calendar days across standard modes |
| **Customer Retention & RFM Score** | Distribution across Champions, Loyal, At-Risk | Maximize Champions & At-Risk re-engagement |

---

### 4. User Personas & Use Cases

#### 4.1 Chief Commercial Officer (CCO) / VP of Sales
- *Needs:* High-level health of regional sales vs. profits, YoY and monthly seasonality, loss rate alerts.
- *Action:* Reallocate sales quotas, adjust annual promotional budgets, set regional sales targets.

#### 4.2 Category & Merchandising Managers
- *Needs:* Granular sub-category and SKU performance, discount elasticity, margin contribution.
- *Action:* Renegotiate vendor contracts on Tables & Bookcases, terminate chronic loss-making SKUs, eliminate discounts $>20\%$ on low-margin goods.

#### 4.3 Supply Chain & Logistics Director
- *Needs:* Shipping mode utilization, lead times by region, shipping cost to margin impact.
- *Action:* Optimize carrier agreements and rationalize Same Day / First Class premium logistics.

---

### 5. Functional Requirements

#### 5.1 Data Pipeline & Ingestion
- Ingest raw dataset (`Sample - Superstore.csv`) containing 9,994 records and 21 columns.
- Preserve immutable raw file in `data/raw/`.
- Validate schema, columns, non-negative quantities, realistic dates, and verify postal code nullity.
- Store cleaned version in `data/cleaned/superstore_cleaned.csv`.

#### 5.2 Feature Engineering Layer
- Create `Profit_Margin`: $\frac{\text{Profit}}{\text{Sales}}$ with safeguards for division-by-zero.
- Create `Shipping_Days`: Difference in calendar days between `Ship Date` and `Order Date`.
- Create `Order_Year`, `Order_Month`, `Order_Quarter`, `Order_Day_Name`, `Year_Month` temporal dimensions.
- Create `Discount_Bucket`: Categorized into `0% (None)`, `1-20% (Low)`, `20-50% (Medium)`, `50%+ (High)`.
- Create `Is_Loss`: Binary boolean indicator (`True` if Profit < 0 else `False`).
- Compute Customer RFM metrics:
  - **Recency ($R$):** Days since latest purchase relative to dataset snapshot.
  - **Frequency ($F$):** Total distinct orders placed by customer.
  - **Monetary ($M$):** Total sales or profit contributed by customer.
  - **RFM Segment:** Classified into Champions, Loyal Customers, Potential Loyalists, At Risk, and Hibernating.
- Store enriched data in `data/cleaned/superstore_featured.csv` and `data/cleaned/customer_rfm.csv`.

#### 5.3 Analytical Core (Jupyter Notebooks)
1. `01_cleaning.ipynb`: Missing value treatment, type casting, duplicate verification, distribution sanity check.
2. `02_features.ipynb`: Temporal extraction, margin computation, discounting categorization, customer RFM synthesis.
3. `03_eda.ipynb`: Statistical univariate distributions, bivariate cross-tabs, correlation matrix, geospatial mapping, lead time analysis.
4. `04_insights.ipynb`: Business questions resolution, discount tipping point analysis, deep dive into loss-generating states and sub-categories.

#### 5.4 Executive Dashboard Specification (Streamlit)
- **Design Standard:** Executive dark/modern theme, rich typography, responsive layout, glassmorphic cards, custom CSS styling.
- **Global Filters:** Year multi-select/slider, Region, Customer Segment, Category, State.
- **View 1: Executive KPI Overview:**
  - 5 KPI summary cards: Total Revenue, Total Profit, Profit Margin %, Total Orders, Loss Ratio %.
  - Monthly Sales & Profit dual trend chart with rolling average.
  - Category & Sub-category margin performance bar/treemap.
- **View 2: Discount & Profit Diagnostics:**
  - Interactive scatter plot: Discount vs. Profit Margin with category color coding and loss boundary line.
  - Profitability distribution by Discount Bucket.
- **View 3: Regional & State Performance:**
  - Interactive US Map / State breakdown highlighting top profit champions and bottom loss-hemorrhaging states.
  - Regional comparison breakdown.
- **View 4: Customer RFM & Products:**
  - Top 10 Most Profitable vs. Bottom 10 Loss-Making Products table with search and conditional formatting.
  - RFM customer segmentation matrix and high-value customer ledger.
- **View 5: Strategic Action Plan:**
  - Direct answers to the 8 Core Business Questions with quantifiable impact estimates.

---

### 6. Non-Functional Requirements
- **Reproducibility:** Single command setup using virtual environment and `requirements.txt`.
- **Modularity:** Reusable cleaning and feature scripts alongside interactive notebooks.
- **Performance:** Streamlit dashboard cached with `@st.cache_data` for sub-second filter updates.
- **Documentation:** Fully documented code, markdown headers in all notebooks, and executive summary report.
