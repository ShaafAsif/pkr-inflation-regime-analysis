import pandas as pd
import numpy as np
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR

df = pd.read_csv('data/processed/merged_monthly_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Recreate differenced/stationary series
df['cpi_yoy_diff'] = df['cpi_yoy'].diff()
df['remittances_diff'] = np.log(df['remittances']).diff() * 100
df['remittances_diff2'] = df['remittances_diff'].diff()
df['pkr_usd_diff'] = np.log(df['pkr_usd']).diff() * 100

model_df = df[['cpi_yoy_diff', 'pkr_usd_diff', 'remittances_diff2']].dropna()
model_df.columns = ['CPI', 'PKR_USD', 'Remittances']

# ---------- Johansen cointegration test (on RAW levels, not differenced) ----------
levels_df = df[['cpi_yoy', 'pkr_usd', 'remittances']].dropna()
johansen_result = coint_johansen(levels_df, det_order=0, k_ar_diff=1)

print("Johansen Cointegration Test")
print("Trace Statistic:", johansen_result.lr1)
print("Critical Values (90%, 95%, 99%):")
print(johansen_result.cvt)
print("\nIf Trace Statistic > 95% Critical Value, cointegration exists -> use VECM")
print("If not, no cointegration -> use VAR on differenced (stationary) data")

# ---------- Fit VAR on stationary/differenced data ----------
var_model = VAR(model_df)
lag_selection = var_model.select_order(maxlags=8)
print("\n\nOptimal lag order suggestions:")
print(lag_selection.summary())

# Fit VAR with lag=2
var_fitted = var_model.fit(2)
print(var_fitted.summary())

# Impulse Response Function - 12 months ahead
irf = var_fitted.irf(12)
irf.plot(orth=False)
import matplotlib.pyplot as plt
plt.savefig('outputs/figures/impulse_response.png', dpi=150)
plt.close()

print("\nImpulse response chart saved to outputs/figures/impulse_response.png")