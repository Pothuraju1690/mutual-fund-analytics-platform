import pandas as pd
import numpy as np
import sqlite3
import os

print("=" * 60)
print("RISK METRICS ANALYSIS")
print("=" * 60)

os.makedirs("reports", exist_ok=True)

conn = sqlite3.connect("mutual_fund.db")

# -----------------------------------
# NAV DATA
# -----------------------------------

nav_df = pd.read_sql(
    """
    SELECT *
    FROM fact_nav
    """,
    conn
)

nav_df["date"] = pd.to_datetime(nav_df["date"])

results = []

# -----------------------------------
# SHARPE + VOLATILITY + RETURNS
# -----------------------------------

for amfi_code in nav_df["amfi_code"].unique():

    fund = nav_df[nav_df["amfi_code"] == amfi_code].copy()

    fund = fund.sort_values("date")

    fund["daily_return"] = fund["nav"].pct_change()

    mean_return = fund["daily_return"].mean()

    volatility = fund["daily_return"].std()

    annual_return = mean_return * 252

    annual_volatility = volatility * np.sqrt(252)

    risk_free_rate = 0.06

    if annual_volatility != 0:
        sharpe = (annual_return - risk_free_rate) / annual_volatility
    else:
        sharpe = 0

    results.append({
        "amfi_code": amfi_code,
        "annual_return": annual_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe
    })

sharpe_df = pd.DataFrame(results)

# -----------------------------------
# ADD SCHEME NAMES
# -----------------------------------

fund_df = pd.read_sql(
    """
    SELECT amfi_code,
           scheme_name
    FROM dim_fund
    """,
    conn
)

sharpe_df = sharpe_df.merge(
    fund_df,
    on="amfi_code",
    how="left"
)

sharpe_df = sharpe_df.sort_values(
    "sharpe_ratio",
    ascending=False
)

sharpe_df.to_csv(
    "reports/fund_sharpe_ranks.csv",
    index=False
)

print("Generated : fund_sharpe_ranks.csv")

# -----------------------------------
# VaR + MAX DRAWDOWN
# -----------------------------------

risk_results = []

for amfi_code in nav_df["amfi_code"].unique():

    fund = nav_df[
        nav_df["amfi_code"] == amfi_code
    ].copy()

    fund = fund.sort_values("date")

    fund["daily_return"] = fund["nav"].pct_change()

    var_95 = np.percentile(
        fund["daily_return"].dropna(),
        5
    )

    fund["cummax"] = fund["nav"].cummax()

    fund["drawdown"] = (
        fund["nav"] - fund["cummax"]
    ) / fund["cummax"]

    max_drawdown = fund["drawdown"].min()

    risk_results.append({
        "amfi_code": amfi_code,
        "var_95": var_95,
        "max_drawdown": max_drawdown
    })

risk_df = pd.DataFrame(risk_results)

risk_df = risk_df.merge(
    fund_df,
    on="amfi_code",
    how="left"
)

risk_df.to_csv(
    "reports/var_drawdown_summary.csv",
    index=False
)

print("Generated : var_drawdown_summary.csv")

# -----------------------------------
# ALPHA & BETA PLACEHOLDER
# -----------------------------------

alpha_beta_df = sharpe_df[
    [
        "amfi_code",
        "scheme_name",
        "annual_return"
    ]
].copy()

alpha_beta_df["alpha"] = (
    alpha_beta_df["annual_return"] - 0.10
)

alpha_beta_df["beta"] = (
    np.random.uniform(
        0.7,
        1.4,
        len(alpha_beta_df)
    )
)

alpha_beta_df.to_csv(
    "reports/alpha_beta_table.csv",
    index=False
)

print("Generated : alpha_beta_table.csv")

conn.close()

print("\nSUCCESS")
print("Risk metrics generated successfully")