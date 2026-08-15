import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/processed/merged_monthly_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Recreate the differenced series
df['cpi_yoy_diff'] = df['cpi_yoy'].diff()
df['remittances_diff'] = np.log(df['remittances']).diff() * 100
df['remittances_diff2'] = df['remittances_diff'].diff()
df['pkr_usd_diff'] = np.log(df['pkr_usd']).diff() * 100

# ---------- CHART 1: Raw series overlay ----------
fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

axes[0].plot(df['date'], df['cpi_yoy'], color='crimson')
axes[0].set_title('CPI Inflation (YoY %)')

axes[1].plot(df['date'], df['pkr_usd'], color='navy')
axes[1].set_title('PKR/USD Exchange Rate')

axes[2].plot(df['date'], df['remittances'], color='darkgreen')
axes[2].set_title('Workers\' Remittances (Million USD)')

plt.tight_layout()
plt.savefig('outputs/figures/raw_series_overlay.png', dpi=150)
plt.close()

# ---------- CHART 2: Granger p-values per lag (PKR/USD -> CPI) ----------
lags = [1, 2, 3, 4, 5, 6]
pvalues = [0.0004, 0.0033, 0.0049, 0.0017, 0.0041, 0.0026]  # from your F-test results

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(lags, pvalues, color=['green' if p < 0.05 else 'gray' for p in pvalues])
ax.axhline(y=0.05, color='red', linestyle='--', label='Significance threshold (p=0.05)')
ax.set_xlabel('Lag (months)')
ax.set_ylabel('p-value')
ax.set_title('Granger Causality: Does PKR/USD Predict CPI Inflation?')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/figures/granger_pvalues_pkr_to_cpi.png', dpi=150)
plt.close()

# ---------- CHART 3: Scatter — PKR/USD change vs CPI change (1-month lag) ----------
plot_df = df[['pkr_usd_diff', 'cpi_yoy_diff']].copy()
plot_df['pkr_usd_diff_lag1'] = plot_df['pkr_usd_diff'].shift(1)
plot_df = plot_df.dropna()

fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(plot_df['pkr_usd_diff_lag1'], plot_df['cpi_yoy_diff'], alpha=0.6, color='purple')
ax.set_xlabel('PKR/USD % Change (previous month)')
ax.set_ylabel('CPI YoY Change (this month)')
ax.set_title('PKR/USD Depreciation (t-1) vs CPI Inflation Change (t)')

# add trend line
z = np.polyfit(plot_df['pkr_usd_diff_lag1'], plot_df['cpi_yoy_diff'], 1)
p = np.poly1d(z)
ax.plot(plot_df['pkr_usd_diff_lag1'], p(plot_df['pkr_usd_diff_lag1']), color='red', linestyle='--')

plt.tight_layout()
plt.savefig('outputs/figures/pkr_cpi_scatter_lag1.png', dpi=150)
plt.close()

print("All 3 charts saved to outputs/figures/")

import statsmodels.api as sm

X = sm.add_constant(plot_df['pkr_usd_diff_lag1'])
y = plot_df['cpi_yoy_diff']
model = sm.OLS(y, X).fit()
print(model.summary())