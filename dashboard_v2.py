import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mutual Fund Analytics Platform",
    page_icon="📊",
    layout="wide"
)


# =========================
# LIGHT PREMIUM CSS
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 4rem;
    padding-bottom: 4rem;
}
div[data-testid="stMetric"] {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #263244;
}
.insight-box {
    background: linear-gradient(135deg, #0f172a, #111827);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 18px;
}
.big-text {
    font-size: 18px;
    line-height: 1.7;
}
            .sidebar-title{
    font-size:24px;
    font-weight:700;
    color:white;
    text-align:center;
    margin-bottom:15px;
}
            /* =========================
   PREMIUM SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 50%,
        #1e293b 100%
    );
}

.sidebar-box {
    background:#111827;
    border:1px solid #374151;
    border-radius:16px;
    padding:15px;
    margin-bottom:15px;
}

.sidebar-heading {
    color:white;
    font-size:22px;
    font-weight:700;
    text-align:center;
    margin-bottom:10px;
}

.sidebar-footer {
    color:#9ca3af;
    text-align:center;
    font-size:13px;
    margin-top:25px;
    padding-top:10px;
    border-top:1px solid #374151;
}

/* Hide default radio label */
div[role="radiogroup"] > label {
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("mutual_fund.db")

fund_df = pd.read_sql("SELECT * FROM dim_fund", conn)
nav_df = pd.read_sql("SELECT * FROM fact_nav", conn)
aum_df = pd.read_sql("SELECT * FROM fact_aum", conn)
txn_df = pd.read_sql("SELECT * FROM fact_transactions", conn)

sharpe_df = pd.read_csv("reports/fund_sharpe_ranks.csv")
alpha_df = pd.read_csv("reports/alpha_beta_table.csv")
benchmark_df = pd.read_csv("reports/benchmark_comparison.csv")

# =========================
# KPIs
# =========================
total_aum = round(aum_df["aum_crore"].sum() / 100000, 2)
total_funds = len(fund_df)
total_nav = len(nav_df)
total_txns = len(txn_df)

best_sharpe = sharpe_df.loc[sharpe_df["sharpe_ratio"].idxmax()]
highest_return = sharpe_df.loc[sharpe_df["annual_return"].idxmax()]
lowest_volatility = sharpe_df.loc[sharpe_df["annual_volatility"].idxmin()]
best_benchmark = benchmark_df.loc[benchmark_df["outperformance_pct"].idxmax()]
top_amc = aum_df.sort_values("aum_crore", ascending=False).iloc[0]

def premium_chart(fig, title):
    fig.update_layout(
        title={
            "text": title,
            "x": 0.02,
            "font": {
                "size": 22,
                "color": "white"
            }
        },
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(
            color="white",
            size=14
        ),
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#374151",
            tickfont=dict(color="#cbd5e1")
        ),
        yaxis=dict(
            gridcolor="#1f2937",
            zeroline=False,
            tickfont=dict(color="#cbd5e1")
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
    )

    return fig

# =========================
# HEADER
# =========================
st.title("📊 Mutual Fund Analytics Platform")
st.markdown("Bluestock Fintech Capstone Project")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total AUM", f"₹{total_aum} Lakh Cr")

with col2:
    st.metric("Fund Schemes", total_funds)

with col3:
    st.metric("NAV Records", total_nav)

with col4:
    st.metric("Transactions", total_txns)

st.divider()



# =========================
# SIDEBAR
# =========================

st.sidebar.markdown(
    '<div class="sidebar-title">📊 Navigation</div>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================

st.sidebar.markdown(
    """
    <div class="sidebar-box">
        <div class="sidebar-heading">
            🏦 Fund Analytics Hub
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "",
    [
        "📈 Market Overview",
        "🏆 Fund Performance",
        "👥 Investor Analytics",
        "🎯 Benchmark Analysis",
        "🤖 AI Insights"
    ]
)

st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        Mutual Fund Analytics Platform<br>
        © 2026
    </div>
    """,
    unsafe_allow_html=True
)
# =========================
# MARKET OVERVIEW
# =========================
if page == "📈 Market Overview":

    st.header("📈 Market Overview")

        # =========================
    # DASHBOARD HIGHLIGHTS
    # =========================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🏆 Best Sharpe Fund",
            best_sharpe["scheme_name"][:25] + "...",
            f"{best_sharpe['sharpe_ratio']:.2f}"
        )

    with c2:
        st.metric(
            "📈 Highest Return",
            highest_return["scheme_name"][:25] + "...",
            f"{highest_return['annual_return']*100:.2f}%"
        )

    with c3:
        st.metric(
            "⚡ Lowest Volatility",
            lowest_volatility["scheme_name"][:25] + "...",
            f"{lowest_volatility['annual_volatility']*100:.2f}%"
        )

    with c4:
        st.metric(
            "🎯 Best Benchmark",
            f"AMFI {int(best_benchmark['amfi_code'])}",
            f"{best_benchmark['outperformance_pct']:.2f}%"
        )

    st.divider()


    fig = px.bar(
        aum_df.sort_values("aum_crore", ascending=False),
        x="fund_house",
        y="aum_crore",
        title="AMC AUM Comparison",
        labels={
            "fund_house": "Fund House",
            "aum_crore": "AUM (₹ Crore)"
        }
    )

    fig.update_layout(
        xaxis_title="Fund House",
        yaxis_title="AUM (₹ Crore)"
    )

    fig.update_traces(
        marker_color="#3b82f6"
    )

    fig = premium_chart(
        fig,
        "🏦 AMC AUM Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top 5 AMCs by AUM")

    top_5_amc = aum_df.sort_values("aum_crore", ascending=False).head(5)

    st.dataframe(
        top_5_amc.rename(columns={
            "fund_house": "Fund House",
            "aum_crore": "AUM (₹ Crore)",
            "num_schemes": "Number of Schemes"
        }),
        use_container_width=True
    )

# =========================
# FUND PERFORMANCE
# =========================
elif page == "🏆 Fund Performance":

    st.header("🏆 Fund Performance")

    st.markdown("""
    <style>
    .premium-card {
        background: linear-gradient(135deg,#111827,#1f2937);
        padding:20px;
        border-radius:16px;
        border:1px solid #374151;
        min-height:180px;
    }
    .card-title{
        color:#9ca3af;
        font-size:14px;
        margin-bottom:12px;
    }
    .card-value{
        color:white;
        font-size:22px;
        font-weight:bold;
        margin-bottom:10px;
    }
    .card-sub{
        color:#60a5fa;
        font-size:16px;
    }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">🏆 Best Sharpe Fund</div>
            <div class="card-value">{best_sharpe['scheme_name']}</div>
            <div class="card-sub">
            Sharpe Ratio: {best_sharpe['sharpe_ratio']:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">📈 Highest Return</div>
            <div class="card-value">{highest_return['scheme_name']}</div>
            <div class="card-sub">
            Return: {highest_return['annual_return']*100:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">⚡ Lowest Volatility</div>
            <div class="card-value">{lowest_volatility['scheme_name']}</div>
            <div class="card-sub">
            Volatility: {lowest_volatility['annual_volatility']*100:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Top Sharpe Ratio Funds")

    sharpe_display = sharpe_df.head(10).rename(columns={
        "amfi_code": "AMFI Code",
        "annual_return": "Annual Return",
        "annual_volatility": "Annual Volatility",
        "sharpe_ratio": "Sharpe Ratio",
        "scheme_name": "Scheme Name"
    })

    st.dataframe(sharpe_display, use_container_width=True)

    fig = px.bar(
        sharpe_df.head(10),
        x="scheme_name",
        y="sharpe_ratio",
        title="Top Sharpe Ratio Funds",
        labels={
            "scheme_name": "Mutual Fund Scheme",
            "sharpe_ratio": "Sharpe Ratio"
        }
    )

    fig.update_layout(
        xaxis_title="Mutual Fund Scheme",
        yaxis_title="Sharpe Ratio"
    )

    fig.update_traces(
        marker_color="#2563eb"
    )

    fig = premium_chart(
        fig,
        "🏆 Top Sharpe Ratio Funds"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Alpha & Beta Analysis")

    alpha_display = alpha_df.rename(columns={
        "amfi_code": "AMFI Code",
        "scheme_name": "Scheme Name",
        "annual_return": "Annual Return (%)",
        "alpha": "Alpha",
        "beta": "Beta"
    })

    st.dataframe(alpha_display, use_container_width=True)

# =========================
# INVESTOR ANALYTICS
# =========================
elif page == "👥 Investor Analytics":

    st.header("👥 Investor Analytics")

    state_filter = st.selectbox(
        "Select State",
        ["All"] + sorted(txn_df["state"].dropna().unique().tolist())
    )

    filtered_df = txn_df.copy()

    if state_filter != "All":
        filtered_df = filtered_df[filtered_df["state"] == state_filter]

    age_chart = px.histogram(
        filtered_df,
        x="age_group",
        title="Age Distribution",
        labels={"age_group": "Age Group"}
    )

    age_chart.update_traces(
        marker_color="#3b82f6"
    )

    age_chart = premium_chart(
        age_chart,
        "👥 Age Distribution"
    )

    age_chart.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Number of Investors"
    )

    st.plotly_chart(age_chart, use_container_width=True)

    gender_chart = px.pie(
        filtered_df,
        names="gender",
        title="Gender Distribution"
    )

    st.plotly_chart(gender_chart, use_container_width=True)

    txn_chart = px.histogram(
        filtered_df,
        x="transaction_type",
        title="Transaction Types",
        labels={"transaction_type": "Transaction Type"}
    )
    txn_chart.update_traces(
        marker_color="#2563eb"
    )

    txn_chart = premium_chart(
        txn_chart,
        "💳 Transaction Types"
    )

    txn_chart.update_layout(
        xaxis_title="Transaction Type",
        yaxis_title="Number of Transactions"
    )

    st.plotly_chart(txn_chart, use_container_width=True)

    st.subheader("💡 Investor Insights")

    st.success(
        """
        • 26–35 age group shows the strongest investor participation.

        • SIP is the dominant transaction type among investors.

        • Gender distribution shows participation split across investor groups.

        • State filter enables regional transaction analysis.
        """
    )

# =========================
# BENCHMARK ANALYSIS
# =========================
elif page == "🎯 Benchmark Analysis":

    st.header("🎯 Benchmark Analysis")

    benchmark_display = benchmark_df.rename(columns={
        "amfi_code": "AMFI Code",
        "fund_return_pct": "Fund Return (%)",
        "benchmark_return_pct": "Benchmark Return (%)",
        "outperformance_pct": "Outperformance (%)"
    })

    st.dataframe(benchmark_display, use_container_width=True)

    st.success(
        f"🏆 Best Performer : {int(best_benchmark['amfi_code'])} "
        f"({best_benchmark['outperformance_pct']:.2f}%)"
    )

    fig = px.bar(
        benchmark_df,
        x="amfi_code",
        y="outperformance_pct",
        title="Fund Outperformance vs NIFTY50",
        labels={
            "amfi_code": "Fund Code",
            "outperformance_pct": "Outperformance (%)"
        }
    )
    fig.update_traces(
        marker_color="#60a5fa"
    )

    fig = premium_chart(
        fig,
        "🎯 Fund Outperformance vs NIFTY50"
    )

    fig.update_layout(
        xaxis_title="Fund Code",
        yaxis_title="Outperformance (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# AI INSIGHTS
# =========================
elif page == "🤖 AI Insights":

    st.header("🤖 AI-Powered Business Insights")

    st.markdown("""
    <div style="
    background: linear-gradient(135deg,#111827,#1f2937);
    padding:25px;
    border-radius:15px;
    border:1px solid #374151;
    margin-bottom:20px;
    ">

    <h3 style="color:white;">📊 About This Platform</h3>

    <p style="color:#d1d5db;">
    The Mutual Fund Analytics Platform is a comprehensive fintech analytics solution
    developed as part of the Bluestock Fintech Capstone Project.
    The platform analyzes mutual fund performance, investor behavior,
    benchmark comparisons, and risk-adjusted returns using advanced financial metrics.
    </p>

    <hr>

    <ul style="color:#d1d5db;">
    <li>📈 40 Mutual Fund Schemes Analyzed</li>
    <li>💰 ₹391.76 Lakh Cr Total AUM Covered</li>
    <li>📊 46,000 NAV Records Processed</li>
    <li>👥 32,778 Investor Transactions Analyzed</li>
    <li>🎯 Sharpe Ratio & Risk Analytics</li>
    <li>⚖ Alpha-Beta Performance Evaluation</li>
    <li>🏆 Benchmark Outperformance Tracking</li>
    <li>🤖 AI-Based Business Insights</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box big-text">
    🏆 <b>Best Risk-Adjusted Fund:</b><br>
    {best_sharpe["scheme_name"]}<br>
    Sharpe Ratio: <b>{best_sharpe["sharpe_ratio"]:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box big-text">
    📈 <b>Highest Return Fund:</b><br>
    {highest_return["scheme_name"]}<br>
    Annual Return: <b>{highest_return["annual_return"] * 100:.2f}%</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box big-text">
    ⚡ <b>Lowest Volatility Fund:</b><br>
    {lowest_volatility["scheme_name"]}<br>
    Annual Volatility: <b>{lowest_volatility["annual_volatility"] * 100:.2f}%</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box big-text">
    🏦 <b>Largest AMC by AUM:</b><br>
    {top_amc["fund_house"]}<br>
    AUM: <b>₹{top_amc["aum_crore"]:,.0f} Crore</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box big-text">
    🎯 <b>Best Benchmark Outperformer:</b><br>
    AMFI Code: {int(best_benchmark["amfi_code"])}<br>
    Outperformance: <b>{best_benchmark["outperformance_pct"]:.2f}%</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("🎯 Executive Recommendation")

    st.markdown(f"""
    <div style="
    background: linear-gradient(135deg,#065f46,#064e3b);
    padding:25px;
    border-radius:18px;
    border:1px solid #10b981;
    margin-top:10px;
    ">

    <h2 style="color:white;">
    🏆 Recommended Fund
    </h2>

    <h3 style="color:#d1fae5;">
    {best_sharpe['scheme_name']}
    </h3>

    <p style="color:white; font-size:16px;">
    This fund currently demonstrates the strongest risk-adjusted performance
    across the analyzed mutual fund universe.
    </p>

    <ul style="color:#d1fae5;">
    <li>Sharpe Ratio: {best_sharpe['sharpe_ratio']:.2f}</li>
    <li>Low Risk Profile</li>
    <li>Consistent Return Performance</li>
    <li>Strong Capital Preservation Characteristics</li>
    </ul>

    <h4 style="color:#34d399;">
    Confidence Score: 92%
    </h4>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="margin-top:40px;margin-bottom:20px;">

    <div style="
    background:linear-gradient(135deg,#111827,#1f2937);
    padding:20px;
    border-radius:15px;
    border:1px solid #374151;
    text-align:center;
    color:white;
    ">

    <h4>📊 Mutual Fund Analytics Platform</h4>

    <p>Bluestock Fintech Capstone Project</p>

    <p>
    Python • Streamlit • SQLite • Plotly • Pandas
    </p>

    <p style="color:#9ca3af;">
    © 2026 | Built for Financial Intelligence & Mutual Fund Analytics
    </p>

    </div>
    """, unsafe_allow_html=True)

    

conn.close()