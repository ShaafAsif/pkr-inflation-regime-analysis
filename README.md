# PKR/USD Exchange Rate & Inflation: A Regime-Dependent Relationship

## The Question
Does Pakistani Rupee depreciation actually drive CPI inflation? And do workers' remittances play a role in that relationship, given how central they are to Pakistan's forex supply?

## TL;DR
The relationship exists — but it's not constant. PKR/USD depreciation has **no significant effect on inflation** under Pakistan's pre-2022 managed exchange rate regime (R²=0.002), but becomes a **strong, statistically significant driver** (R²=0.221, p<0.001) once the rate became market-determined after 2022. Workers' remittances, despite the intuitive appeal, show no significant direct effect on either PKR/USD or CPI in this analysis.

## Data
All data sourced from the State Bank of Pakistan's Easy Data portal, monthly, July 2016–July 2026:
- **CPI (National, YoY basis)** — Pakistan Bureau of Statistics via SBP
- **PKR/USD Exchange Rate** — Bank Floating Average Exchange Rates
- **Workers' Remittances** — Total monthly inflow, Country-wise Remittances series

Raw data is not redistributed in this repo (see `data/raw/` — excluded via `.gitignore`); download instructions are in `data/data_dictionary.md`.

## Methodology
1. **Stationarity testing** (Augmented Dickey-Fuller) — all three series required differencing/log-differencing before further analysis
2. **Granger causality testing** — tested directional predictability across 1–6 month lags
3. **VAR(2) modeling** — joint system model of CPI, PKR/USD, and Remittances, lag order selected via BIC/HQIC
4. **Impulse response analysis** — traced how a shock to each variable propagates through the system over 12 months
5. **Robustness testing** — re-ran the core CPI~PKR/USD regression excluding the 2022–2023 devaluation period, then split the sample into pre-/post-2022 regimes

## Key Findings

| Test | Result |
|---|---|
| Granger causality: PKR/USD → CPI | Significant at all lags 1–6 (p<0.005) |
| Granger causality: Remittances → CPI or PKR/USD | Not significant at any lag |
| Full-sample regression (PKR/USD → CPI) | R²=0.116, p<0.001 |
| Excluding 2022–2023 | R²=0.005, p=0.496 (relationship disappears) |
| Pre-2022 (managed regime) | R²=0.002, p=0.714 (no relationship) |
| Post-2022 (market regime) | R²=0.221, p<0.001 (strong relationship) |

**The core insight:** exchange rate pass-through to inflation in Pakistan isn't a stable macroeconomic constant — it's regime-dependent. Under a managed/pegged rate, PKR movements were disconnected from real market pressure and didn't transmit to prices. Once the rate floated in 2022, pass-through became immediate and substantial.

## Visuals
- `outputs/figures/raw_series_overlay.png` — CPI, PKR/USD, and Remittances over time
- `outputs/figures/granger_pvalues_pkr_to_cpi.png` — significance across lags
- `outputs/figures/pkr_cpi_scatter_lag1.png` — relationship scatter, full sample
- `outputs/figures/impulse_response.png` — 12-month shock propagation across the VAR system
- `outputs/figures/regime_comparison.png` — R² by exchange rate regime

## Limitations
- Remittance data reflects official banking channels only; informal (hundi/hawala) transfers are unobserved and could bias the true remittance-forex relationship
- Sample size (~120 months) limits VAR lag order and statistical power, particularly for the regime-split subsamples (n=64 and n=55)
- CPI base-year rebasing (2015–16 base) means pre-2016 data isn't directly comparable and was excluded
- Findings are associative, not proof of a single causal mechanism — other macro variables (oil prices, fiscal policy, global rates) aren't controlled for here

## Tools
Python, pandas, statsmodels (ADF, Granger causality, VAR, Johansen cointegration), matplotlib

## Project Structure
See `data/data_dictionary.md` for data sourcing details and `reports/findings_writeup.md` for the narrative summary.
