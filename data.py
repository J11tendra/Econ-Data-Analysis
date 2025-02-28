import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from fredapi import Fred
fred_key = '570646936c180a3d8189b37127c78cb2'
fred = Fred(api_key=fred_key)

# Fetch economic data from FRED
inflation = fred.get_series('CPIAUCSL')  # Consumer Price Index (Inflation Proxy)
unemployment = fred.get_series('UNRATE')  # Unemployment Rate
sp500 = fred.get_series('SP500')  # S&P 500 Index
interest_rates = fred.get_series('FEDFUNDS')  # Federal Funds Rate

# Combine data into a DataFrame
df = pd.DataFrame({
    'Inflation': inflation,
    'Unemployment': unemployment,
    'S&P 500': sp500,
    'Interest Rates': interest_rates
})
df.dropna(inplace=True)
df.index = pd.to_datetime(df.index)

# Normalize data for better visualization
df_normalized = (df - df.min()) / (df.max() - df.min())

# Plot time-series trends
plt.figure(figsize=(12, 6))
df_normalized.plot(ax=plt.gca())
plt.title('Economic Indicators Over Time')
plt.ylabel('Normalized Values')
plt.xlabel('Year')
plt.legend()
plt.grid(True)
plt.show()

# Correlation heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(df.corr().round(2), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Between Economic Indicators')
plt.show()

# Regression Analysis: Predicting S&P 500 Performance
X = df[['Inflation', 'Unemployment', 'Interest Rates']]
X = sm.add_constant(X)  # Adds constant term to regression
y = df['S&P 500']
model = sm.OLS(y, X).fit()
print(model.summary())

# Granger Causality Test - Does Inflation or Interest Rates Granger Cause S&P 500?
from statsmodels.tsa.stattools import grangercausalitytests
granger_test = grangercausalitytests(df[['S&P 500', 'Inflation']], maxlag=5, verbose=True)
granger_test = grangercausalitytests(df[['S&P 500', 'Interest Rates']], maxlag=5, verbose=True)
