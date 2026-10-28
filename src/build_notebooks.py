"""Notebook Generation and Execution Engine for Superstore Sales EDA.

Creates and executes 4 professional, modular Jupyter notebooks:
- 01_cleaning.ipynb
- 02_features.ipynb
- 03_eda.ipynb
- 04_insights.ipynb
"""

from pathlib import Path
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook
from nbclient import NotebookClient


def execute_and_save(nb, filepath: Path, run_dir: Path):
    """Execute all cells in notebook and save populated notebook to disk."""
    print(f"Executing notebook: {filepath.name} in {run_dir}...")
    client = NotebookClient(
        nb, 
        timeout=300, 
        kernel_name="python3",
        resources={"metadata": {"path": str(run_dir.resolve())}}
    )
    client.execute()
    with open(filepath, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Successfully wrote executed notebook to: {filepath}\n")


def build_cleaning_notebook(notebooks_dir: Path, repo_root: Path):
    """Build and execute 01_cleaning.ipynb."""
    nb = new_notebook()

    nb.cells.append(new_markdown_cell("""# Superstore Sales EDA: 01. Data Ingestion & Cleaning
---
**Objective:** Ingest raw transactional data, perform systematic schema validation, identify and address data quality anomalies (missing values, formatting, invalid types), and produce an immutable cleaned baseline for downstream analysis.

### Workflow:
1. Environment setup and library imports
2. Raw data loading and dimension audit
3. Missing value & duplicate detection
4. Postal code & geographic standardization
5. Temporal type casting & chronological validity checks
6. Numeric boundary & sanity constraints
7. Export cleaned dataset to `data/cleaned/superstore_cleaned.csv`
"""))

    nb.cells.append(new_code_cell("""import os
from pathlib import Path
import numpy as np
import pandas as pd

# Dynamic path resolution (supports both running from repo root or notebooks/)
def get_path(rel_path):
    for candidate in [Path(rel_path), Path("..") / rel_path, Path("/home/adarsh/Documents/Superstore Sales EDA") / rel_path]:
        if candidate.exists():
            return candidate
    return Path(rel_path)

raw_path = get_path("data/raw/Sample - Superstore.csv")
if not raw_path.exists():
    raw_path = get_path("data/raw/Superstore.csv")

print(f"Loading raw data from: {raw_path}")
"""))

    nb.cells.append(new_markdown_cell("""## 1. Load Raw Dataset & Inspect Structure
We load the raw CSV with `windows-1252` encoding to properly handle special characters in product names.
"""))

    nb.cells.append(new_code_cell("""try:
    df_raw = pd.read_csv(raw_path, encoding="windows-1252")
except UnicodeDecodeError:
    df_raw = pd.read_csv(raw_path, encoding="utf-8")

print(f"Total Transactions: {df_raw.shape[0]:,}")
print(f"Total Columns: {df_raw.shape[1]}")
df_raw.head(3)
"""))

    nb.cells.append(new_markdown_cell("""## 2. Schema & Data Types Inspection
Examine columns, non-null counts, and data types across all 21 raw features.
"""))

    nb.cells.append(new_code_cell("""df_raw.info()
"""))

    nb.cells.append(new_markdown_cell("""## 3. Duplicate Records Audit
We check for exact duplicate rows as well as duplicate primary key indicators (`Row ID`).
"""))

    nb.cells.append(new_code_cell("""exact_dupes = df_raw.duplicated().sum()
row_id_dupes = df_raw["Row ID"].duplicated().sum()

print(f"Exact row duplicates: {exact_dupes}")
print(f"Duplicate Row IDs: {row_id_dupes}")
assert exact_dupes == 0, "Warning: Duplicate rows detected!"
assert row_id_dupes == 0, "Warning: Duplicate Row IDs detected!"
"""))

    nb.cells.append(new_markdown_cell("""## 4. Missing Value Audit & Postal Code Treatment
In retail datasets, missing ZIP codes or geographic nulls can distort regional reporting.
We check for nulls and format postal codes as standardized 5-digit strings.
"""))

    nb.cells.append(new_code_cell("""null_summary = df_raw.isnull().sum()
print("Missing values per column:")
print(null_summary[null_summary > 0] if (null_summary > 0).any() else "No NaN values detected.")

df_clean = df_raw.copy()

# Standardize Postal Code
# Impute Burlington, VT if missing or 0
burlington_mask = (df_clean["City"] == "Burlington") & (df_clean["State"] == "Vermont")
df_clean.loc[burlington_mask & df_clean["Postal Code"].isnull(), "Postal Code"] = 5401

df_clean["Postal Code"] = (
    df_clean["Postal Code"]
    .fillna(0)
    .astype(int)
    .astype(str)
    .str.zfill(5)
)
df_clean.loc[df_clean["Postal Code"] == "00000", "Postal Code"] = "Unknown"

print("Postal code formatted sample:")
print(df_clean[['City', 'State', 'Postal Code']].head(4))
"""))

    nb.cells.append(new_markdown_cell("""## 5. Temporal Conversions & Logical Validation
Convert `Order Date` and `Ship Date` to `datetime64[ns]`.
Verify the business rule: **`Ship Date >= Order Date`** (no orders shipped prior to purchase).
"""))

    nb.cells.append(new_code_cell("""df_clean["Order Date"] = pd.to_datetime(df_clean["Order Date"], format="mixed")
df_clean["Ship Date"] = pd.to_datetime(df_clean["Ship Date"], format="mixed")

# Validation check
invalid_lead_times = (df_clean["Ship Date"] < df_clean["Order Date"]).sum()
print(f"Orders with Ship Date < Order Date: {invalid_lead_times}")
assert invalid_lead_times == 0, "Temporal anomaly: Dispatch date precedes order date!"

print(f"Earliest Order Date: {df_clean['Order Date'].min().strftime('%Y-%m-%d')}")
print(f"Latest Order Date:   {df_clean['Order Date'].max().strftime('%Y-%m-%d')}")
"""))

    nb.cells.append(new_markdown_cell("""## 6. Financial & Numeric Bounds Validation
Check for impossible business values:
- `Sales > 0`
- `Quantity >= 1`
- `0.0 <= Discount <= 1.0`
"""))

    nb.cells.append(new_code_cell("""sales_check = (df_clean["Sales"] <= 0).sum()
quantity_check = (df_clean["Quantity"] <= 0).sum()
discount_check = ((df_clean["Discount"] < 0) | (df_clean["Discount"] > 1.0)).sum()

print(f"Invalid Sales (<=0): {sales_check}")
print(f"Invalid Quantity (<=0): {quantity_check}")
print(f"Invalid Discount (<0 or >1): {discount_check}")

assert sales_check == 0 and quantity_check == 0 and discount_check == 0, "Numeric integrity violation!"

# Summary statistics of numerical columns
df_clean[["Sales", "Quantity", "Discount", "Profit"]].describe().T
"""))

    nb.cells.append(new_markdown_cell("""## 7. Categorical Standardization & Export
Strip extraneous whitespace from string/categorical dimensions and persist cleaned dataset.
"""))

    nb.cells.append(new_code_cell("""str_cols = ["Order ID", "Customer ID", "Customer Name", "Country", 
            "City", "State", "Region", "Product ID", "Category", 
            "Sub-Category", "Product Name", "Ship Mode", "Segment"]

for col in str_cols:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].astype(str).str.strip()

out_dir = Path("data/cleaned") if Path("data").exists() else Path("../data/cleaned")
out_dir.mkdir(parents=True, exist_ok=True)
out_clean = out_dir / "superstore_cleaned.csv"

df_clean.to_csv(out_clean, index=False)
print(f"Successfully cleaned and exported {len(df_clean):,} records to: {out_clean}")
"""))

    execute_and_save(nb, notebooks_dir / "01_cleaning.ipynb", repo_root)


def build_features_notebook(notebooks_dir: Path, repo_root: Path):
    """Build and execute 02_features.ipynb."""
    nb = new_notebook()

    nb.cells.append(new_markdown_cell("""# Superstore Sales EDA: 02. Feature Engineering & Customer RFM
---
**Objective:** Derive rich financial, temporal, operational, and customer behavioral metrics from the cleaned dataset.

### Engineered Dimensions:
1. **Financial:** Profit Margin %, Effective Unit Price, Effective Unit Cost, Is_Loss flag.
2. **Operational:** Shipping Lead Time in days (`Shipping_Days`).
3. **Temporal:** Year, Month, Month Name, Quarter, Day of Week, Year-Month period.
4. **Commercial:** Discount Buckets (`0% (None)`, `1-20% (Low)`, `21-50% (Medium)`, `50%+ (High)`).
5. **Customer Analytics (RFM):** Recency, Frequency, Monetary Value, and RFM Customer Segments.
"""))

    nb.cells.append(new_code_cell("""import os
from pathlib import Path
import numpy as np
import pandas as pd

def get_path(rel_path):
    for candidate in [Path(rel_path), Path("..") / rel_path, Path("/home/adarsh/Documents/Superstore Sales EDA") / rel_path]:
        if candidate.exists():
            return candidate
    return Path(rel_path)

clean_path = get_path("data/cleaned/superstore_cleaned.csv")
df = pd.read_csv(clean_path)
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
print(f"Loaded cleaned dataset with {df.shape[0]:,} rows and {df.shape[1]} columns.")
"""))

    nb.cells.append(new_markdown_cell("""## 1. Financial & Operational Feature Engineering
Calculate Profit Margin (with zero division safeguard), Unit Financials, and Lead Times.
"""))

    nb.cells.append(new_code_cell("""# Profit Margin %
df["Profit_Margin"] = np.where(df["Sales"] > 0, df["Profit"] / df["Sales"], 0.0)

# Unprofitable Order Flag
df["Is_Loss"] = df["Profit"] < 0

# Unit Economics
df["Effective_Unit_Price"] = df["Sales"] / df["Quantity"]
df["Effective_Unit_Cost"] = (df["Sales"] - df["Profit"]) / df["Quantity"]

# Shipping Lead Time (Calendar Days)
df["Shipping_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("Financial & Operational Feature Summary:")
df[["Profit_Margin", "Shipping_Days", "Effective_Unit_Price", "Effective_Unit_Cost"]].describe().T
"""))

    nb.cells.append(new_markdown_cell("""## 2. Temporal Decomposition
Extract calendar dimensions to support monthly seasonality, quarterly performance, and day-of-week analysis.
"""))

    nb.cells.append(new_code_cell("""df["Order_Year"] = df["Order Date"].dt.year
df["Order_Month"] = df["Order Date"].dt.month
df["Order_Month_Name"] = df["Order Date"].dt.strftime("%B")
df["Order_Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
df["Order_Day_Name"] = df["Order Date"].dt.day_name()
df["Year_Month"] = df["Order Date"].dt.to_period("M").astype(str)

print("Orders per Year:")
print(df["Order_Year"].value_counts().sort_index())
"""))

    nb.cells.append(new_markdown_cell("""## 3. Discount Bucketing
Discounts in Superstore range from 0% to 80%. We categorize them into actionable business tiers:
- **0% (None):** Full retail price transactions
- **1-20% (Low):** Standard retail promotions
- **21-50% (Medium):** Aggressive promotional discounting
- **50%+ (High):** Heavy clearance discounting
"""))

    nb.cells.append(new_code_cell("""def categorize_discount(d: float) -> str:
    if d == 0.0:
        return "0% (None)"
    elif d <= 0.20:
        return "1-20% (Low)"
    elif d <= 0.50:
        return "21-50% (Medium)"
    else:
        return "50%+ (High)"

df["Discount_Bucket"] = df["Discount"].apply(categorize_discount)
bucket_order = ["0% (None)", "1-20% (Low)", "21-50% (Medium)", "50%+ (High)"]
df["Discount_Bucket"] = pd.Categorical(df["Discount_Bucket"], categories=bucket_order, ordered=True)

df["Discount_Bucket"].value_counts().sort_index()
"""))

    nb.cells.append(new_markdown_cell("""## 4. Customer RFM Segmentation
We synthesize Customer Recency (days since last purchase), Frequency (order count), and Monetary Value (lifetime revenue and profit).
"""))

    nb.cells.append(new_code_cell("""snapshot_date = df["Order Date"].max() + pd.Timedelta(days=1)

rfm = df.groupby(["Customer ID", "Customer Name", "Segment"]).agg(
    Recency_Days=("Order Date", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Order ID", "nunique"),
    Total_Items=("Row ID", "count"),
    Monetary_Sales=("Sales", "sum"),
    Monetary_Profit=("Profit", "sum"),
    Avg_Discount=("Discount", "mean"),
    Loss_Orders_Count=("Is_Loss", lambda x: int(x.sum())),
).reset_index()

rfm["Profit_Margin"] = np.where(
    rfm["Monetary_Sales"] > 0,
    rfm["Monetary_Profit"] / rfm["Monetary_Sales"],
    0.0
)

# Quintile Scoring (1 to 5)
rfm["R_Score"] = pd.qcut(rfm["Recency_Days"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary_Sales"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

def segment_customer(row) -> str:
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif f >= 3 and m >= 3:
        return "Loyal Customers"
    elif r >= 3 and f >= 2:
        return "Potential Loyalists"
    elif r >= 4 and f <= 2:
        return "Recent / New Customers"
    elif r <= 2 and (f >= 3 or m >= 3):
        return "At Risk / Needs Attention"
    elif r <= 2 and f <= 2 and m <= 2:
        return "Hibernating / Lost"
    else:
        return "Promising Customers"

rfm["RFM_Segment"] = rfm.apply(segment_customer, axis=1)

print("Customer RFM Segment Distribution:")
rfm["RFM_Segment"].value_counts()
"""))

    nb.cells.append(new_markdown_cell("""## 5. Enrich Transaction Layer & Persist Deliverables
Merge `RFM_Segment` back into order items and write both datasets to `data/cleaned/`.
"""))

    nb.cells.append(new_code_cell("""df = df.merge(
    rfm[["Customer ID", "RFM_Segment"]],
    on="Customer ID",
    how="left"
)

out_dir = Path("data/cleaned") if Path("data").exists() else Path("../data/cleaned")
out_featured = out_dir / "superstore_featured.csv"
out_rfm = out_dir / "customer_rfm.csv"

df.to_csv(out_featured, index=False)
rfm.to_csv(out_rfm, index=False)

print(f"Exported feature-engineered dataset: {out_featured} ({df.shape})")
print(f"Exported customer RFM dataset:        {out_rfm} ({rfm.shape})")
"""))

    execute_and_save(nb, notebooks_dir / "02_features.ipynb", repo_root)


def build_eda_notebook(notebooks_dir: Path, repo_root: Path):
    """Build and execute 03_eda.ipynb."""
    nb = new_notebook()

    nb.cells.append(new_markdown_cell("""# Superstore Sales EDA: 03. Exploratory Data Analysis
---
**Objective:** Deep statistical exploration across univariate distributions, category economics, promotional discount sensitivity, regional profit polarizations, fulfillment lead times, and time series seasonality.
"""))

    nb.cells.append(new_code_cell("""import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120

def get_path(rel_path):
    for candidate in [Path(rel_path), Path("..") / rel_path, Path("/home/adarsh/Documents/Superstore Sales EDA") / rel_path]:
        if candidate.exists():
            return candidate
    return Path(rel_path)

data_path = get_path("data/cleaned/superstore_featured.csv")
df = pd.read_csv(data_path)
df["Order Date"] = pd.to_datetime(df["Order Date"])
print(f"Loaded featured dataset: {df.shape[0]:,} rows, {df.shape[1]} columns.")
"""))

    nb.cells.append(new_markdown_cell("""## 1. High-Level Portfolio Performance & Univariate Summary
Inspect top-level commercial KPIs: Total Sales, Total Profit, Aggregate Margin %, and Loss Order Share.
"""))

    nb.cells.append(new_code_cell("""total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
overall_margin = (total_profit / total_sales) * 100
loss_orders = df["Is_Loss"].sum()
loss_rate = (loss_orders / len(df)) * 100

print(f"Total Revenue:       ${total_sales:,.2f}")
print(f"Total Net Profit:    ${total_profit:,.2f}")
print(f"Overall Margin:      {overall_margin:.2f}%")
print(f"Loss-Making Orders:  {loss_orders:,} of {len(df):,} ({loss_rate:.2f}%)")
"""))

    nb.cells.append(new_markdown_cell("""## 2. Category & Sub-Category Performance
Analyze gross sales vs net profit across Categories and identify chronic loss-generating sub-categories.
"""))

    nb.cells.append(new_code_cell("""cat_df = df.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Order_Count=("Row ID", "count")
).reset_index()
cat_df["Margin%"] = (cat_df["Profit"] / cat_df["Sales"]) * 100
print(cat_df.sort_values(by="Profit", ascending=False))
"""))

    nb.cells.append(new_code_cell("""sub_df = df.groupby(["Category", "Sub-Category"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Row ID", "count"),
    Avg_Discount=("Discount", "mean")
).reset_index()
sub_df["Margin%"] = (sub_df["Profit"] / sub_df["Sales"]) * 100
sub_df = sub_df.sort_values(by="Profit", ascending=False)

print("Top 5 Profit Generating Sub-Categories:")
print(sub_df.head(5))

print("\\nBottom 5 Sub-Categories (Loss Makers):")
print(sub_df.tail(5))
"""))

    nb.cells.append(new_markdown_cell("""## 3. Promotional Discount Analysis: The 20% Profit Cliff
Investigate how discount rates directly correlate with margin erosion and order unprofitability.
"""))

    nb.cells.append(new_code_cell("""disc_perf = df.groupby("Discount_Bucket", observed=False).agg(
    Orders=("Row ID", "count"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Loss_Orders=("Is_Loss", "sum")
).reset_index()

disc_perf["Margin%"] = (disc_perf["Total_Profit"] / disc_perf["Total_Sales"]) * 100
disc_perf["Loss_Rate%"] = (disc_perf["Loss_Orders"] / disc_perf["Orders"]) * 100
print(disc_perf)
"""))

    nb.cells.append(new_markdown_cell("""## 4. Geographic & State-Level Polarization
Identify top-earning states (California, New York) and chronic loss states (Texas, Ohio, Pennsylvania, Illinois).
"""))

    nb.cells.append(new_code_cell("""state_perf = df.groupby("State").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Row ID", "count"),
    Avg_Discount=("Discount", "mean")
).reset_index()
state_perf["Margin%"] = (state_perf["Profit"] / state_perf["Sales"]) * 100

print("Top 5 Profitable States:")
print(state_perf.sort_values(by="Profit", ascending=False).head(5))

print("\\nBottom 5 Loss States:")
print(state_perf.sort_values(by="Profit", ascending=True).head(5))
"""))

    nb.cells.append(new_markdown_cell("""## 5. Shipping Modes & Logistics Lead Times
Examine fulfillment lead times and profitability across fulfillment tiers.
"""))

    nb.cells.append(new_code_cell("""ship_perf = df.groupby("Ship Mode").agg(
    Mean_Days=("Shipping_Days", "mean"),
    Median_Days=("Shipping_Days", "median"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Row ID", "count")
).reset_index()
ship_perf["Margin%"] = (ship_perf["Total_Profit"] / ship_perf["Total_Sales"]) * 100
print(ship_perf)
"""))

    nb.cells.append(new_markdown_cell("""## 6. Time Series & Seasonality Analysis
Resample monthly sales and profit to visualize annual Q4 surges and growth trajectories.
"""))

    nb.cells.append(new_code_cell("""monthly_trend = df.set_index("Order Date").resample("ME").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
monthly_trend["Margin%"] = (monthly_trend["Profit"] / monthly_trend["Sales"]) * 100

print("Annual Summary:")
annual = df.groupby("Order_Year").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
annual["Margin%"] = (annual["Profit"] / annual["Sales"]) * 100
annual["YoY_Sales_Growth%"] = annual["Sales"].pct_change() * 100
print(annual)
"""))

    execute_and_save(nb, notebooks_dir / "03_eda.ipynb", repo_root)


def build_insights_notebook(notebooks_dir: Path, repo_root: Path):
    """Build and execute 04_insights.ipynb."""
    nb = new_notebook()

    nb.cells.append(new_markdown_cell("""# Superstore Sales EDA: 04. Strategic Business Insights & Recommendations
---
**Objective:** Deliver direct, quantifiable answers to the 8 Core Business Questions, run financial sensitivity simulations (capping discounts, fixing Tables), and outline an executive action plan.
"""))

    nb.cells.append(new_code_cell("""import os
from pathlib import Path
import numpy as np
import pandas as pd

def get_path(rel_path):
    for candidate in [Path(rel_path), Path("..") / rel_path, Path("/home/adarsh/Documents/Superstore Sales EDA") / rel_path]:
        if candidate.exists():
            return candidate
    return Path(rel_path)

featured_path = get_path("data/cleaned/superstore_featured.csv")
rfm_path = get_path("data/cleaned/customer_rfm.csv")

df = pd.read_csv(featured_path)
df["Order Date"] = pd.to_datetime(df["Order Date"])
rfm = pd.read_csv(rfm_path)
print(f"Loaded featured dataset ({df.shape}) and customer RFM ({rfm.shape}).")
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 1: Which categories & sub-categories generate profit, and which lose money?
"""))

    nb.cells.append(new_code_cell("""sub_summary = df.groupby(["Category", "Sub-Category"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Row ID", "count")
).reset_index()
sub_summary["Margin%"] = (sub_summary["Profit"] / sub_summary["Sales"]) * 100
sub_summary = sub_summary.sort_values(by="Profit", ascending=False)

print("Champion Sub-Categories (Profit > $30K):")
print(sub_summary[sub_summary["Profit"] > 30000])

print("\\nLoss-Making Sub-Categories:")
print(sub_summary[sub_summary["Profit"] < 0])
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 2: How do discounts affect profit and margin?
"""))

    nb.cells.append(new_code_cell("""disc_analysis = df.groupby("Discount_Bucket", observed=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Row ID", "count"),
    Loss_Orders=("Is_Loss", "sum")
).reset_index()
disc_analysis["Margin%"] = (disc_analysis["Profit"] / disc_analysis["Sales"]) * 100
disc_analysis["Loss_Rate%"] = (disc_analysis["Loss_Orders"] / disc_analysis["Orders"]) * 100
print(disc_analysis)
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 3: Which regions and states underperform?
"""))

    nb.cells.append(new_code_cell("""reg_analysis = df.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
reg_analysis["Margin%"] = (reg_analysis["Profit"] / reg_analysis["Sales"]) * 100
print("Regional Overview:")
print(reg_analysis.sort_values(by="Profit", ascending=False))

loss_states = df.groupby("State").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Avg_Discount=("Discount", "mean")
).reset_index()
loss_states["Margin%"] = (loss_states["Profit"] / loss_states["Sales"]) * 100
loss_states = loss_states[loss_states["Profit"] < 0].sort_values(by="Profit")
print(f"\\nTotal Loss-Making States: {len(loss_states)} states totaling ${loss_states['Profit'].sum():,.2f} in losses:")
print(loss_states)
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 4: Who are the most valuable customers and segments?
"""))

    nb.cells.append(new_code_cell("""rfm_overview = rfm.groupby("RFM_Segment").agg(
    Customer_Count=("Customer ID", "count"),
    Total_Sales=("Monetary_Sales", "sum"),
    Total_Profit=("Monetary_Profit", "sum")
).reset_index()
rfm_overview["Sales_Share%"] = (rfm_overview["Total_Sales"] / rfm_overview["Total_Sales"].sum()) * 100
rfm_overview["Profit_Share%"] = (rfm_overview["Total_Profit"] / rfm_overview["Total_Profit"].sum()) * 100
rfm_overview["Margin%"] = (rfm_overview["Total_Profit"] / rfm_overview["Total_Sales"]) * 100
print(rfm_overview.sort_values(by="Total_Profit", ascending=False))
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 5: Monthly, quarterly, and yearly seasonality trends
"""))

    nb.cells.append(new_code_cell("""quarter_analysis = df.groupby(["Order_Year", "Order_Quarter"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
quarter_analysis["Margin%"] = (quarter_analysis["Profit"] / quarter_analysis["Sales"]) * 100
print(quarter_analysis.tail(8))
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 6: Shipping mode impact on lead time & profit
"""))

    nb.cells.append(new_code_cell("""ship_summary = df.groupby("Ship Mode").agg(
    Lead_Time_Days=("Shipping_Days", "mean"),
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).assign(Margin_Pct=lambda x: (x["Profit"] / x["Sales"]) * 100)
print(ship_summary)
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 7: Chronic loss-making products
Identify individual SKUs with the largest aggregate net losses.
"""))

    nb.cells.append(new_code_cell("""product_losses = df.groupby(["Product ID", "Product Name", "Category", "Sub-Category"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Row ID", "count"),
    Avg_Discount=("Discount", "mean")
).reset_index()
product_losses = product_losses.sort_values(by="Profit", ascending=True)

print("Top 10 Chronic Loss-Making Products:")
print(product_losses.head(10))
"""))

    nb.cells.append(new_markdown_cell("""## Business Question 8 & Scenario Simulations: How to Increase Profit
What is the quantified impact of eliminating discounts > 20%?
"""))

    nb.cells.append(new_code_cell("""# Current Baseline
baseline_sales = df["Sales"].sum()
baseline_profit = df["Profit"].sum()
baseline_margin = (baseline_profit / baseline_sales) * 100

# Simulation 1: Eliminate transactions with Discount > 20%
df_capped = df[df["Discount"] <= 0.20]
sim1_sales = df_capped["Sales"].sum()
sim1_profit = df_capped["Profit"].sum()
sim1_margin = (sim1_profit / sim1_sales) * 100

# Simulation 2: Eliminate unprofitable Tables sub-category
df_no_loss_tables = df[df["Sub-Category"] != "Tables"]
sim2_sales = df_no_loss_tables["Sales"].sum()
sim2_profit = df_no_loss_tables["Profit"].sum()
sim2_margin = (sim2_profit / sim2_sales) * 100

sim_summary = pd.DataFrame([
    {"Scenario": "Baseline (Current)", "Sales": baseline_sales, "Profit": baseline_profit, "Margin%": baseline_margin},
    {"Scenario": "Sim 1: Cap Discounts at 20%", "Sales": sim1_sales, "Profit": sim1_profit, "Margin%": sim1_margin},
    {"Scenario": "Sim 2: Exclude Tables Sub-Category", "Sales": sim2_sales, "Profit": sim2_profit, "Margin%": sim2_margin},
    {"Scenario": "Sim 3: Cap Discounts at 20% & Optimize Tables", 
     "Sales": df[(df["Discount"] <= 0.20) | (df["Sub-Category"] != "Tables")]["Sales"].sum(),
     "Profit": df_capped[df_capped["Sub-Category"] != "Tables"]["Profit"].sum(),
     "Margin%": (df_capped[df_capped["Sub-Category"] != "Tables"]["Profit"].sum() / df_capped[df_capped["Sub-Category"] != "Tables"]["Sales"].sum()) * 100}
])

sim_summary["Profit_Lift ($)"] = sim_summary["Profit"] - baseline_profit
sim_summary["Profit_Growth (%)"] = (sim_summary["Profit_Lift ($)"] / baseline_profit) * 100
print(sim_summary)
"""))

    execute_and_save(nb, notebooks_dir / "04_insights.ipynb", repo_root)


def main():
    repo_root = Path("/home/adarsh/Documents/Superstore Sales EDA")
    notebooks_dir = repo_root / "notebooks"
    notebooks_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== Building & Executing All 4 Jupyter Notebooks ===")
    build_cleaning_notebook(notebooks_dir, repo_root)
    build_features_notebook(notebooks_dir, repo_root)
    build_eda_notebook(notebooks_dir, repo_root)
    build_insights_notebook(notebooks_dir, repo_root)
    print("=== All 4 notebooks built and executed successfully! ===")


if __name__ == "__main__":
    main()
