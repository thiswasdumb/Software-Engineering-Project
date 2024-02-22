# Importing numpy library and aliasing it as np for ease of use
import numpy as np

# Defining market_data and stock_data arrays using numpy arrays
market_data = np.array([-0.685,-0.438,-0.302,0.015,-0.623])
stock_data = np.array([-0.419,-6.791,-0.635,-2.737,1.278])

# Defining bond_yield, inflation, and calculating riskfree rate
bond_yield = 4.65
inflation = 4.2
riskfree = bond_yield - inflation

# Calculating covariance, variance, and mean of market_data
# Covariance between market_data and stock_data
cv = np.cov(market_data, stock_data)[0][1].item()

# Variance of market_data
mv = np.var(market_data).item()

# Mean of market_data
mr = np.mean(market_data).item()

# Calculating beta using CAPM formula
# Beta coefficient
b = (mr * cv) / mv

 # Capital Asset Pricing Model (CAPM) calculation
capm = riskfree + b * (mr - riskfree)

# Printing the calculated CAPM value
print(capm)