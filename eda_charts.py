import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

print("=" * 60)
print("EDA CHART GENERATION")
print("=" * 60)

# Create reports folder if not exists
os.makedirs("reports", exist_ok=True)

conn = sqlite3.connect("mutual_fund.db")

# --------------------------------------------------
# Chart 1 : Top 10 AMCs by AUM
# --------------------------------------------------

aum_df = pd.read_sql(
    """
    SELECT fund_house,
           SUM(aum_crore) as total_aum
    FROM fact_aum
    GROUP BY fund_house
    ORDER BY total_aum DESC
    LIMIT 10
    """,
    conn
)

plt.figure(figsize=(10,6))
plt.bar(aum_df["fund_house"], aum_df["total_aum"])
plt.xticks(rotation=45)
plt.title("Top 10 Fund Houses by AUM")
plt.ylabel("AUM (Crore)")
plt.tight_layout()
plt.savefig("reports/top_10_amc_aum.png")
plt.close()

print("Generated : top_10_amc_aum.png")

# --------------------------------------------------
# Chart 2 : SIP Inflow Trend
# --------------------------------------------------

sip_df = pd.read_sql(
    """
    SELECT month,
           sip_inflow_crore
    FROM fact_sip
    """,
    conn
)

plt.figure(figsize=(10,6))
plt.plot(sip_df["month"], sip_df["sip_inflow_crore"])
plt.xticks(rotation=90)
plt.title("Monthly SIP Inflow Trend")
plt.ylabel("SIP Inflow (Crore)")
plt.tight_layout()
plt.savefig("reports/sip_inflow_trend.png")
plt.close()

print("Generated : sip_inflow_trend.png")

# --------------------------------------------------
# Chart 3 : Investor Age Distribution
# --------------------------------------------------

age_df = pd.read_sql(
    """
    SELECT age_group,
           COUNT(*) as total
    FROM fact_transactions
    GROUP BY age_group
    ORDER BY total DESC
    """,
    conn
)

plt.figure(figsize=(8,5))
plt.bar(age_df["age_group"], age_df["total"])
plt.title("Investor Age Distribution")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reports/age_distribution.png")
plt.close()

print("Generated : age_distribution.png")

# --------------------------------------------------
# Chart 4 : Transaction Type Distribution
# --------------------------------------------------

txn_df = pd.read_sql(
    """
    SELECT transaction_type,
           COUNT(*) as total
    FROM fact_transactions
    GROUP BY transaction_type
    """,
    conn
)

plt.figure(figsize=(6,6))
plt.pie(
    txn_df["total"],
    labels=txn_df["transaction_type"],
    autopct="%1.1f%%"
)
plt.title("Transaction Type Distribution")
plt.savefig("reports/transaction_distribution.png")
plt.close()

print("Generated : transaction_distribution.png")

# --------------------------------------------------
# Chart 5 : State Wise Investors
# --------------------------------------------------

state_df = pd.read_sql(
    """
    SELECT state,
           COUNT(*) as total
    FROM fact_transactions
    GROUP BY state
    ORDER BY total DESC
    LIMIT 10
    """,
    conn
)

plt.figure(figsize=(10,6))
plt.bar(state_df["state"], state_df["total"])
plt.xticks(rotation=45)
plt.title("Top States by Investor Activity")
plt.ylabel("Transactions")
plt.tight_layout()
plt.savefig("reports/state_distribution.png")
plt.close()

print("Generated : state_distribution.png")

conn.close()

print("\nSUCCESS")
print("All EDA charts generated in reports folder")