"""Data Cleaning Pipeline for Superstore Sales Dataset.

Loads raw data, performs validation, type casting, handles missing values,
checks duplicates and logical constraints, and saves cleaned dataset.
"""

from pathlib import Path
import pandas as pd


def load_and_clean_data(raw_path: str = "data/raw/Sample - Superstore.csv",
                        output_path: str = "data/cleaned/superstore_cleaned.csv") -> pd.DataFrame:
    """Load raw dataset, clean columns, enforce data types, validate integrity, and save."""
    raw_file = Path(raw_path)
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw data file not found at: {raw_file}")

    print(f"[1/5] Loading raw data from {raw_file}...")
    try:
        df = pd.read_csv(raw_file, encoding="windows-1252")
    except UnicodeDecodeError:
        df = pd.read_csv(raw_file, encoding="utf-8")

    initial_shape = df.shape
    print(f"      Initial shape: {initial_shape[0]} rows, {initial_shape[1]} columns")

    # 1. Clean column names
    print("[2/5] Standardizing column names...")
    df.columns = df.columns.str.strip()

    # 2. Check for duplicate records
    duplicate_rows = df.duplicated().sum()
    print(f"      Exact duplicate rows found: {duplicate_rows}")
    duplicate_row_ids = df["Row ID"].duplicated().sum()
    print(f"      Duplicate Row IDs: {duplicate_row_ids}")

    # 3. Handle Missing Values
    print("[3/5] Handling missing values and postal code formatting...")
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) > 0:
        print(f"      Found null columns:\n{null_cols}")
    else:
        print("      No standard null values found across the dataset.")

    # Format Postal Code as 5-digit string (handling any floats/ints and imputing known missing Burlington, VT)
    if "Postal Code" in df.columns:
        # Impute Burlington, VT postal code if null or 0
        burlington_mask = (df["City"] == "Burlington") & (df["State"] == "Vermont")
        df.loc[burlington_mask & df["Postal Code"].isnull(), "Postal Code"] = 5401
        
        # Format as 5-digit string with leading zero
        df["Postal Code"] = (
            df["Postal Code"]
            .fillna(0)
            .astype(int)
            .astype(str)
            .str.zfill(5)
        )
        # If filled with 00000, label as 'Unknown'
        df.loc[df["Postal Code"] == "00000", "Postal Code"] = "Unknown"

    # 4. Parse Dates & Validate Temporal Logic
    print("[4/5] Parsing dates and verifying temporal consistency...")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed")

    # Logical verification: Ship Date must be on or after Order Date
    invalid_dates = df[df["Ship Date"] < df["Order Date"]]
    if len(invalid_dates) > 0:
        raise ValueError(f"Found {len(invalid_dates)} records where Ship Date precedes Order Date!")
    print(f"      Validated {len(df)} records: Ship Date >= Order Date holds true.")

    # 5. Numerical Validations
    print("[5/5] Validating numerical bounds...")
    assert (df["Sales"] > 0).all(), "Found non-positive Sales values!"
    assert (df["Quantity"] > 0).all(), "Found non-positive Quantity values!"
    assert ((df["Discount"] >= 0) & (df["Discount"] <= 1.0)).all(), "Found invalid Discount values!"

    # Ensure correct typing for categoricals and strings
    string_cols = ["Order ID", "Customer ID", "Customer Name", "Country", 
                   "City", "State", "Region", "Product ID", "Category", 
                   "Sub-Category", "Product Name", "Ship Mode", "Segment"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Save cleaned dataset
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_file, index=False)
    print(f"Successfully cleaned and saved dataset to: {out_file}")
    print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df


if __name__ == "__main__":
    load_and_clean_data()
