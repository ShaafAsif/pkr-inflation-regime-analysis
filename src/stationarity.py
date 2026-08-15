import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

df = pd.read_csv('data/processed/merged_monthly_data.csv')

def adf_test(series, name):
    result = adfuller(series.dropna())
    print(f"\n--- {name} ---")
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4f}")
    if result[1] < 0.05:
        print(f"=> {name} is STATIONARY (p < 0.05)")
    else:
        print(f"=> {name} is NOT stationary (p >= 0.05) — needs differencing")

adf_test(df['cpi_yoy'], 'CPI YoY')
adf_test(df['remittances'], 'Remittances')
adf_test(df['pkr_usd'], 'PKR/USD')

# Difference each series
df['cpi_yoy_diff'] = df['cpi_yoy'].diff()
df['remittances_diff'] = np.log(df['remittances']).diff() * 100
df['pkr_usd_diff'] = np.log(df['pkr_usd']).diff() * 100

# Re-test stationarity on differenced series
adf_test(df['cpi_yoy_diff'], 'CPI YoY (differenced)')
# Second difference for remittances (removes remaining seasonal/trend structure)
df['remittances_diff2'] = df['remittances_diff'].diff()
adf_test(df['remittances_diff2'], 'Remittances (2nd diff)')

# Save the differenced data for the next step (Granger causality)
df.to_csv('data/processed/merged_monthly_data_diff.csv', index=False)