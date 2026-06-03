import pandas as pd
import sqlite3

print("=" * 60)
print("ETL DATA LOAD")
print("=" * 60)

conn = sqlite3.connect("mutual_fund.db")

# ---------------------------
# DIM FUND
# ---------------------------
fund_df = pd.read_csv("data/processed/01_fund_master.csv")

fund_df.to_sql(
    "dim_fund",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded : dim_fund")

# ---------------------------
# FACT NAV
# ---------------------------
nav_df = pd.read_csv("data/processed/02_nav_history.csv")

nav_df.to_sql(
    "fact_nav",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded : fact_nav")

# ---------------------------
# FACT AUM
# ---------------------------
aum_df = pd.read_csv("data/processed/03_aum_by_fund_house.csv")

aum_df.to_sql(
    "fact_aum",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded : fact_aum")

# ---------------------------
# FACT SIP
# ---------------------------
sip_df = pd.read_csv("data/processed/04_monthly_sip_inflows.csv")

sip_df.to_sql(
    "fact_sip",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded : fact_sip")

# ---------------------------
# FACT TRANSACTIONS
# ---------------------------
txn_df = pd.read_csv("data/processed/08_investor_transactions.csv")

txn_df.to_sql(
    "fact_transactions",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded : fact_transactions")

# ---------------------------
# BENCHMARK
# ---------------------------
bench_df = pd.read_csv("data/processed/10_benchmark_indices.csv")

bench_df.to_sql(
    "dim_benchmark",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded : dim_benchmark")

conn.close()

print("\nSUCCESS")
print("All cleaned data loaded into SQLite database")