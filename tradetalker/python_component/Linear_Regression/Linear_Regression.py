# Importing necessary libraries
from flask import Flask
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# from database_connection import DataBaseConnection
# db = DataBaseConnection (
#     host="localhost",
#         user="root",
#         passwd="",
#         database="tradetalkerdb"
#     )

# Work out CAPM equation
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

# Sample data for testing
# Generate random data with a weak trend
np.random.seed(0)
num_samples = 100
CAPM = np.linspace(-5, 5, num_samples) + np.random.normal(0, 0.5, num_samples)
Sentiment_Score = np.linspace(-0.8, 0.8, num_samples) + np.random.normal(0, 0.1, num_samples)
stock_price = 100 + 10 * CAPM + 50 * Sentiment_Score + np.random.normal(0, 20, num_samples)

# Create the dataset
data = {
    'CAPM': CAPM.tolist(),
    'Sentiment_Score': Sentiment_Score.tolist(),
    'stock_price': stock_price.tolist()
}

# Creating a DataFrame from the sample data
df = pd.DataFrame(data)

# Extracting features (independent variables) and target (dependent variables)
X = df[['CAPM', 'Sentiment_Score']]
y = df['stock_price']

# Splitting the dataset into training and testing sets
# test_size=0.2 implies that 20% of the data will be used for testing
# random_state is set for reproducibility of results
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=18)

# Check the shapes of the training and testing data
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

min_stock_price = y_test.min()
max_stock_price = y_test.max()

print("Minimum stock price:", min_stock_price)
print("Maximum stock price:", max_stock_price)

# Creating a Linear Regression model
model = LinearRegression()

# Training the model on the training data
model.fit(X_train, y_train)

# Making predictions on the testing data
predictions = model.predict(X_test)

# Calculating Mean Absolute Error (MAE) to evaluate model performance
mae = mean_absolute_error(y_test, y_train)
print(f'Mean Absolute Error: {mae}')

# Visualizing the actual vs predicted values using a scatter plot
plt.scatter(X_test['Sentiment_Score'], y_test, color='black', label='Actual')

# Sort X_test['Sentiment_Score'] and predictions to ensure the line of best fit is continuous
sorted_indices = np.argsort(X_test['Sentiment_Score'])
sorted_sentiment_score = X_test['Sentiment_Score'].iloc[sorted_indices]
sorted_predictions = predictions[sorted_indices]

# find line of best fit
a, b = np.polyfit(sorted_sentiment_score, sorted_predictions, 1)




# First attempt 
# plt.plot(X_test['Sentiment_Score'], predictions, color='blue', linewidth=3, label='Predicted')

# Second Attempt could work 
# plt.plot(sorted_sentiment_score, sorted_predictions, color='blue', linewidth=3, label='Predicted')

# Third Attempt
# Calculate the endpoints of the line of best fit
# x_min = X_test['Sentiment_Score'].min()
# x_max = X_test['Sentiment_Score'].max()
# y_min = model.predict([[x_min, 0]])[0]
# y_max = model.predict([[x_max, 0]])[0]
# plt.plot([x_min, x_max], [y_min, y_max], color='blue', linewidth=3, label='Predicted')

# Fourth Attempt
# Calculate the endpoints of the line of best fit
# x_min = sorted_sentiment_score.min()
# x_max = sorted_sentiment_score.max()
# y_min = sorted_predictions.min()
# y_max = sorted_predictions.max()
# Check if it is a negative or positive trend
# if x_min == Sentiment_Score[np.argmax(stock_price)]:
# plt.plot([x_max, x_min], [y_max, y_min], color='blue', linewidth=3, label='Predicted')
# else:
# plt.plot([x_min, x_max], [y_min, y_max], color='blue', linewidth=3, label='Predicted')




# Plot the line of best fit
plt.plot(sorted_sentiment_score, a*sorted_sentiment_score + b, color = 'blue', linewidth=3, label="Predicted")
plt.title('Linear Regression Model for Stock Price Prediction based on Sentiment Score')
plt.xlabel('Sentiment Score and CAPM model')
plt.ylabel('Stock Price')
plt.legend()
plt.tight_layout()
plt.show()
