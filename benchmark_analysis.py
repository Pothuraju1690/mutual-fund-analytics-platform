import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("BENCHMARK ANALYSIS")
print("=" * 60)

conn = sqlite3.connect("mutual_fund.db")

# Load fund NAV data
nav_df = pd.read_sql(
    """
    SELECT *
    FROM fact_nav
    """,
    conn
)

# Load benchmark data
benchmark_df = pd.read_sql(
    """
    SELECT *
    FROM dim_benchmark
    WHERE index_name='NIFTY50'
    """,
    conn
)

# Convert dates
nav_df["date"] = pd.to_datetime(nav_df["date"])
benchmark_df["date"] = pd.to_datetime(benchmark_df["date"])

# Top 5 funds
top_funds = (
    nav_df.groupby("amfi_code")["nav"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .index
)

comparison_results = []

for fund in top_funds:

    fund_df = nav_df[nav_df["amfi_code"] == fund].copy()

    fund_return = (
        (fund_df["nav"].iloc[-1] - fund_df["nav"].iloc[0])
        / fund_df["nav"].iloc[0]
    ) * 100

    benchmark_return = (
        (
            benchmark_df["close_value"].iloc[-1]
            - benchmark_df["close_value"].iloc[0]
        )
        / benchmark_df["close_value"].iloc[0]
    ) * 100

    comparison_results.append(
        {
            "amfi_code": fund,
            "fund_return_pct": round(fund_return, 2),
            "benchmark_return_pct": round(benchmark_return, 2),
            "outperformance_pct": round(
                fund_return - benchmark_return,
                2
            )
        }
    )

comparison_df = pd.DataFrame(comparison_results)

comparison_df.to_csv(
    "reports/benchmark_comparison.csv",
    index=False
)

print("Generated : benchmark_comparison.csv")

# Chart
plt.figure(figsize=(10, 6))

plt.bar(
    comparison_df["amfi_code"].astype(str),
    comparison_df["outperformance_pct"]
)

plt.title("Fund Outperformance vs NIFTY50")
plt.xlabel("AMFI Code")
plt.ylabel("Outperformance (%)")

plt.tight_layout()

plt.savefig(
    "reports/benchmark_vs_fund.png"
)

plt.close()

print("Generated : benchmark_vs_fund.png")

conn.close()

print("\nSUCCESS")
print("Benchmark analysis completed")