# Data Dictionary

All data sourced from the State Bank of Pakistan's Easy Data portal (easydata.sbp.org.pk), monthly frequency, July 2016 – July 2026.

## merged_monthly_data.csv

| Column | Description | Source Series | Unit | Notes |
|---|---|---|---|---|
| `date` | Observation month (end-of-month date) | — | Date | Common index across all series |
| `cpi_yoy` | National CPI inflation, Year-on-Year basis | Inflation Snapshot (New Base: 2015-16), National CPI (YoY) | Percent | PBS-compiled, republished via SBP |
| `remittances` | Total workers' remittances inflow | Country-wise Workers' Remittances, "Total inflow of Workers' Remittances in Pakistan" | Million USD | Raw (not seasonally adjusted) |
| `pkr_usd` | PKR/USD exchange rate | Bank Floating Average Exchange Rates (PKR per National Currency), USD series | PKR per 1 USD | Monthly average, not month-end |

## merged_monthly_data_diff.csv

Same as above, with additional transformed (stationary) columns used for causality/VAR modeling:

| Column | Transformation | Reason |
|---|---|---|
| `cpi_yoy_diff` | First difference of `cpi_yoy` | Raw CPI YoY series was non-stationary (ADF p=0.18) |
| `remittances_diff` | Log first difference of `remittances` × 100 | Raw series non-stationary; log-diff approximates % change |
| `remittances_diff2` | Second difference of `remittances_diff` | Single log-difference still non-stationary (likely due to seasonality); second difference achieved stationarity (ADF p<0.001) |
| `pkr_usd_diff` | Log first difference of `pkr_usd` × 100 | Raw series non-stationary; log-diff achieved stationarity (ADF p<0.001) |

## Known Limitations
- Remittances reflect official banking-channel transfers only; informal (hundi/hawala) flows are unobserved
- CPI base year changed to 2015–16 in this series; earlier base-year data is not directly comparable and was excluded
- PKR/USD is a monthly average, which smooths out intra-month volatility
