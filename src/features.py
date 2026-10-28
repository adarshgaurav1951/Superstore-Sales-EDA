"""Feature Engineering Pipeline for Superstore Sales Dataset.

Calculates profit margins, shipping duration, temporal dimensions,
discount buckets, loss indicators, unit financials, and customer RFM segmentation.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def engineer_features(cleaned_path: str = "data/cleaned/superstore_cleaned.csv",
                       featured_path: str = "data/cleaned/superstore_featured.csv",
                       rfm_path: str = "data/cleaned/customer_rfm.csv") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Derive operational, financial, temporal, and customer-level features."""
    cleaned_file = Path(cleaned_path)
    if not cleaned_file.exists():
        raise FileNotFoundError(f"Cleaned file not found: {cleaned_file}")

    print(f"[1/4] Loading cleaned dataset from {cleaned_file}...")
    df = pd.read_csv(cleaned_file)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    # 1. Financial & Profitability Features
    print("[2/4] Engineering financial, operational, and temporal features...")
    df["Profit_Margin"] = np.where(df["Sales"] > 0, df["Profit"] / df["Sales"], 0.0)
    df["Is_Loss"] = df["Profit"] < 0
    df["Effective_Unit_Price"] = df["Sales"] / df["Quantity"]
    df["Effective_Unit_Cost"] = (df["Sales"] - df["Profit"]) / df["Quantity"]

    # Shipping Duration
    df["Shipping_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # Temporal features
    df["Order_Year"] = df["Order Date"].dt.year
    df["Order_Month"] = df["Order Date"].dt.month
    df["Order_Month_Name"] = df["Order Date"].dt.strftime("%B")
    df["Order_Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
    df["Order_Day_Name"] = df["Order Date"].dt.day_name()
    df["Year_Month"] = df["Order Date"].dt.to_period("M").astype(str)

    # Discount Bucketing
    def categorize_discount(disc: float) -> str:
        if disc == 0.0:
            return "0% (None)"
        elif disc <= 0.20:
            return "1-20% (Low)"
        elif disc <= 0.50:
            return "21-50% (Medium)"
        else:
            return "50%+ (High)"

    df["Discount_Bucket"] = df["Discount"].apply(categorize_discount)
    # Categorical ordering
    bucket_order = ["0% (None)", "1-20% (Low)", "21-50% (Medium)", "50%+ (High)"]
    df["Discount_Bucket"] = pd.Categorical(df["Discount_Bucket"], categories=bucket_order, ordered=True)

    # 2. Customer RFM Segmentation
    print("[3/4] Computing Customer RFM (Recency, Frequency, Monetary) metrics...")
    snapshot_date = df["Order Date"].max() + pd.Timedelta(days=1)

    customer_agg = df.groupby(["Customer ID", "Customer Name", "Segment"]).agg(
        Recency_Days=("Order Date", lambda x: (snapshot_date - x.max()).days),
        Frequency=("Order ID", "nunique"),
        Total_Items=("Row ID", "count"),
        Monetary_Sales=("Sales", "sum"),
        Monetary_Profit=("Profit", "sum"),
        Avg_Discount=("Discount", "mean"),
        Loss_Orders_Count=("Is_Loss", lambda x: int(x.sum())),
    ).reset_index()

    customer_agg["Profit_Margin"] = np.where(
        customer_agg["Monetary_Sales"] > 0,
        customer_agg["Monetary_Profit"] / customer_agg["Monetary_Sales"],
        0.0
    )

    # Calculate quintiles for R, F, M
    # Note: Recency lower is better -> reverse labels 5 down to 1
    customer_agg["R_Score"] = pd.qcut(
        customer_agg["Recency_Days"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop"
    ).astype(int)
    
    # Frequency & Monetary higher is better -> labels 1 to 5
    customer_agg["F_Score"] = pd.qcut(
        customer_agg["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]
    ).astype(int)
    customer_agg["M_Score"] = pd.qcut(
        customer_agg["Monetary_Sales"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

    customer_agg["RFM_Score"] = (
        customer_agg["R_Score"].astype(str) +
        customer_agg["F_Score"].astype(str) +
        customer_agg["M_Score"].astype(str)
    )

    def assign_rfm_segment(row) -> str:
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

    customer_agg["RFM_Segment"] = customer_agg.apply(assign_rfm_segment, axis=1)

    # 3. Merge RFM Segment back into transaction data
    print("[4/4] Merging RFM segments into transaction layer and persisting...")
    df = df.merge(
        customer_agg[["Customer ID", "RFM_Segment"]],
        on="Customer ID",
        how="left"
    )

    # Save files
    featured_file = Path(featured_path)
    featured_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(featured_file, index=False)

    rfm_file = Path(rfm_path)
    rfm_file.parent.mkdir(parents=True, exist_ok=True)
    customer_agg.to_csv(rfm_file, index=False)

    print(f"Successfully generated featured dataset: {featured_file} ({df.shape})")
    print(f"Successfully generated customer RFM dataset: {rfm_file} ({customer_agg.shape})")
    return df, customer_agg


if __name__ == "__main__":
    engineer_features()
