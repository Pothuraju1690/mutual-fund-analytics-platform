import pandas as pd
import os

print("=" * 70)
print("DATA CLEANING PROCESS")
print("=" * 70)

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file in files:

    print("\n" + "=" * 70)
    print(f"Processing: {file}")
    print("=" * 70)

    file_path = os.path.join(RAW_PATH, file)

    df = pd.read_csv(file_path)

    print(f"Original Shape : {df.shape}")

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"Duplicates Removed : {before - after}")

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Strip spaces from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Fill missing values
    for col in df.columns:

        if df[col].dtype == "object":
            df[col] = df[col].fillna("Unknown")

        else:
            df[col] = df[col].fillna(df[col].median())

    output_path = os.path.join(PROCESSED_PATH, file)

    df.to_csv(output_path, index=False)

    print(f"Cleaned Shape : {df.shape}")
    print(f"Saved To : {output_path}")

print("\n")
print("=" * 70)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 70)