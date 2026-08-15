import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

df = pd.read_csv('data/processed/merged_monthly_data.csv')

df['cpi_yoy_diff'] = df['cpi_yoy'].diff()
df['remittances_diff'] = (df['remittances'].apply(lambda x: __import__('numpy').log(x))).diff() * 100
df['remittances_diff2'] = df['remittances_diff'].diff()
df['pkr_usd_diff'] = (df['pkr_usd'].apply(lambda x: __import__('numpy').log(x))).diff() * 100

test_df = df[['remittances_diff2', 'pkr_usd_diff', 'cpi_yoy_diff']].dropna()

max_lag = 6

print("="*50)
print("Does REMITTANCES Granger-cause PKR/USD?")
print("="*50)
grangercausalitytests(test_df[['pkr_usd_diff', 'remittances_diff2']], maxlag=max_lag)

print("\n" + "="*50)
print("Does PKR/USD Granger-cause REMITTANCES?")
print("="*50)
grangercausalitytests(test_df[['remittances_diff2', 'pkr_usd_diff']], maxlag=max_lag)

print("\n" + "="*50)
print("Does REMITTANCES Granger-cause CPI?")
print("="*50)
grangercausalitytests(test_df[['cpi_yoy_diff', 'remittances_diff2']], maxlag=max_lag)

print("\n" + "="*50)
print("Does PKR/USD Granger-cause CPI?")
print("="*50)
grangercausalitytests(test_df[['cpi_yoy_diff', 'pkr_usd_diff']], maxlag=max_lag)