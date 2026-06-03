import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mutual Fund Analytics Dashboard",
    layout="wide"
)

st.title("📊 Mutual Fund Analytics Dashboard")

conn = sqlite3.connect("mutual_fund.db")

# ======================
# SIDEBAR
# ======================

st.sidebar.header("Navigation")

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Market Overview",
        "Fund Performance",
        "Investor Demographics",
        "Benchmark Analysis"
    ]
)

# ======================
# MARKET OVERVIEW
# ======================

if page == "Market Overview":

    st.header("Market Overview")

    aum_df = pd.read_sql(
        """
        SELECT fund_house,
               aum_crore
        FROM fact_aum
        """,
        conn
    )

    fig = px.bar(
        aum_df,
        x="fund_house",
        y="aum_crore",
        title="AMC AUM Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# FUND PERFORMANCE
# ======================

elif page == "Fund Performance":

    st.header("Fund Performance")

    sharpe_df = pd.read_csv(
        "reports/fund_sharpe_ranks.csv"
    )

    st.dataframe(sharpe_df)

    fig = px.bar(
        sharpe_df.head(10),
        x="scheme_name",
        y="sharpe_ratio",
        title="Top Sharpe Ratio Funds"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# INVESTOR DEMOGRAPHICS
# ======================

elif page == "Investor Demographics":

    st.header("Investor Demographics")

    txn_df = pd.read_sql(
        """
        SELECT *
        FROM fact_transactions
        """,
        conn
    )

    age_chart = px.histogram(
        txn_df,
        x="age_group",
        title="Age Group Distribution"
    )

    st.plotly_chart(age_chart, use_container_width=True)

    state_chart = px.bar(
        txn_df["state"].value_counts().reset_index(),
        x="state",
        y="count",
        title="Top States by Transactions"
    )

    st.plotly_chart(state_chart, use_container_width=True)

# ======================
# BENCHMARK ANALYSIS
# ======================

elif page == "Benchmark Analysis":

    st.header("Benchmark Analysis")

    benchmark_df = pd.read_csv(
        "reports/benchmark_comparison.csv"
    )

    st.dataframe(benchmark_df)

    fig = px.bar(
        benchmark_df,
        x="amfi_code",
        y="outperformance_pct",
        title="Fund Outperformance vs NIFTY50"
    )

    st.plotly_chart(fig, use_container_width=True)

conn.close()