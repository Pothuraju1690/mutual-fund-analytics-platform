# Mutual Fund Analytics - Data Quality Report

## Dataset Summary

Total Datasets Analysed: 10

Datasets:

1. Fund Master
2. NAV History
3. AUM by Fund House
4. Monthly SIP Inflows
5. Category Inflows
6. Industry Folio Count
7. Scheme Performance
8. Investor Transactions
9. Portfolio Holdings
10. Benchmark Indices

---

## Missing Values Analysis

Only one column contains missing values:

Dataset:
04_monthly_sip_inflows.csv

Column:
yoy_growth_pct

Missing Records:
12

Observation:
These missing values are expected because Year-over-Year growth cannot be calculated for the earliest months.

---

## Duplicate Records Analysis

No duplicate records were found in any dataset.

Duplicate Rows Found:
0

---

## AMFI Validation

Validation Result:
SUCCESS

All 40 AMFI codes present in fund_master.csv exist in nav_history.csv.

Fund Master Codes:
40

NAV History Codes:
40

---

## Overall Assessment

Data quality is good.

Findings:

- All datasets loaded successfully.
- No duplicate records found.
- AMFI code integrity verified.
- Missing values are minimal and expected.
- Datasets are ready for analysis and dashboard development.
