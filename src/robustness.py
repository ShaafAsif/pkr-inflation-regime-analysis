import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv('data/processed/merged_monthly_data.csv')
df['date'] = pd.to_datetime(df['date'])

df['cpi_yoy_diff'] = df['cpi_yoy'].diff()
df['pkr_usd_diff'] = np.log(df['pkr_usd']).diff() * 100
df['pkr_usd_diff_lag1'] = df['pkr_usd_diff'].shift(1)

plot_df = df[['date', 'pkr_usd_diff_lag1', 'cpi_yoy_diff']].dropna()

# Full sample regression (baseline, already done)
X_full = sm.add_constant(plot_df['pkr_usd_diff_lag1'])
y_full = plot_df['cpi_yoy_diff']
model_full = sm.OLS(y_full, X_full).fit()
print("=== FULL SAMPLE ===")
print(f"R-squared: {model_full.rsquared:.4f}")
print(f"PKR coefficient: {model_full.params['pkr_usd_diff_lag1']:.4f}, p-value: {model_full.pvalues['pkr_usd_diff_lag1']:.4f}")

# Excluding the 2022-2023 devaluation window
mask = ~plot_df['date'].between('2022-01-01', '2023-12-31')
excl_df = plot_df[mask]

X_excl = sm.add_constant(excl_df['pkr_usd_diff_lag1'])
y_excl = excl_df['cpi_yoy_diff']
model_excl = sm.OLS(y_excl, X_excl).fit()
print("\n=== EXCLUDING 2022-2023 ===")
print(f"R-squared: {model_excl.rsquared:.4f}")
print(f"PKR coefficient: {model_excl.params['pkr_usd_diff_lag1']:.4f}, p-value: {model_excl.pvalues['pkr_usd_diff_lag1']:.4f}")

# Split into pre-2022 (managed float) vs post-2022 (market-determined) regimes
pre_2022 = plot_df[plot_df['date'] < '2022-01-01']
post_2022 = plot_df[plot_df['date'] >= '2022-01-01']

for label, subset in [('PRE-2022 (managed regime)', pre_2022), ('POST-2022 (market regime)', post_2022)]:
    X = sm.add_constant(subset['pkr_usd_diff_lag1'])
    y = subset['cpi_yoy_diff']
    model = sm.OLS(y, X).fit()
    print(f"\n=== {label} (n={len(subset)}) ===")
    print(f"R-squared: {model.rsquared:.4f}")
    print(f"PKR coefficient: {model.params['pkr_usd_diff_lag1']:.4f}, p-value: {model.pvalues['pkr_usd_diff_lag1']:.4f}")

import matplotlib.pyplot as plt

labels = ['Full Sample', 'Pre-2022\n(Managed)', 'Post-2022\n(Market)']
r_squared = [0.1158, 0.0022, 0.2209]
colors = ['gray', 'lightcoral', 'darkgreen']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, r_squared, color=colors)
ax.set_ylabel('R-squared')
ax.set_title('PKR/USD → CPI Relationship Strength by Exchange Rate Regime')
for bar, val in zip(bars, r_squared):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.005, f'{val:.3f}', ha='center')
plt.tight_layout()
plt.savefig('outputs/figures/regime_comparison.png', dpi=150)
plt.close()
print("Regime comparison chart saved.")