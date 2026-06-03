import sqlite3
import pandas as pd

print("=" * 60)
print("EDA ANALYSIS")
print("=" * 60)

conn = sqlite3.connect("mutual_fund.db")

tables = [
    "dim_fund",
    "fact_nav",
    "fact_aum",
    "fact_sip",
    "fact_transactions",
    "dim_benchmark"
]

for table in tables:

    print("\n" + "=" * 60)
    print(f"TABLE : {table}")
    print("=" * 60)

    df = pd.read_sql(
        f"SELECT * FROM {table}",
        conn
    )

    print("Rows    :", df.shape[0])
    print("Columns :", df.shape[1])

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nSample Data:")
    print(df.head())

conn.close()