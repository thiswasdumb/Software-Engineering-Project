import numpy as np

market_data = np.array([-0.685,-0.438,-0.302,0.015,-0.623])
stock_data = np.array([-0.419,-6.791,-0.635,-2.737,1.278])
bond_yield = 4.65
inflation = 4.2
riskfree = bond_yield - inflation


cv = np.cov(market_data, stock_data)[0][1].item()
mv = np.var(market_data).item()
mr = np.mean(market_data).item()
b = (mr * cv) / mv
capm = riskfree + b * (mr - riskfree)

print(capm)