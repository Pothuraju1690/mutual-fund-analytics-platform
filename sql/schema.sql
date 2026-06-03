-- ==========================================
-- MUTUAL FUND ANALYTICS DATABASE SCHEMA
-- ==========================================

CREATE TABLE dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    risk_grade TEXT,
    expense_ratio REAL
);

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    nav_date DATE,
    nav_value REAL,
    FOREIGN KEY (scheme_code)
        REFERENCES dim_fund(scheme_code)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amc_name TEXT,
    quarter_date TEXT,
    aum_crores REAL
);

CREATE TABLE fact_sip (
    sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month_year TEXT,
    sip_inflow_cr REAL,
    active_accounts REAL
);

CREATE TABLE fact_transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id INTEGER,
    scheme_code INTEGER,
    amount REAL,
    transaction_type TEXT,
    FOREIGN KEY (scheme_code)
        REFERENCES dim_fund(scheme_code)
);

CREATE TABLE dim_benchmark (
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_name TEXT,
    benchmark_date DATE,
    close_value REAL
);