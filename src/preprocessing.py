import pandas as pd

def load_series(filepath, value_col_name, filter_series_name=None):
    df = pd.read_csv(filepath)
    
    # If multiple series are mixed in one file, filter to the one we want
    if filter_series_name:
        df = df[df['Series name'] == filter_series_name]
    
    df = df[['Observation Date', 'Observation Value']].copy()
    df.columns = ['date', value_col_name]
    
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%Y')
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

# Load each series
cpi = load_series(
    'data/raw/cpi_yoy_raw.csv',
    'cpi_yoy',
    filter_series_name='National CPI, an Inflation Measure (Year-on-Year basis)'
)

remittances = load_series('data/raw/remittances_raw.csv', 'remittances')
pkr_usd = load_series('data/raw/pkr_usd_raw.csv', 'pkr_usd')

# Merge all three on date
merged = cpi.merge(remittances, on='date', how='inner').merge(pkr_usd, on='date', how='inner')

print(merged.head())
print(merged.shape)
print(merged.isnull().sum())

merged.to_csv('data/processed/merged_monthly_data.csv', index=False)
print("\nSaved to data/processed/merged_monthly_data.csv")