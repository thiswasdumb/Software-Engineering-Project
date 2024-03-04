# Importing necessary libraries
from flask import Flask
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta
import yfinance as yf

# from database_connection import DataBaseConnection
# db = DataBaseConnection (
#         host="localhost",
#         user="root",
#         passwd="",
#         database="tradetalkerdb"
#     )

class Linear_Regression:
     # Calculate the dates of the last 7 days 
    global end_date 
    end_date = datetime.today().strftime("%Y-%m-%d")
    global start_date 
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    global company_symbol
    company_symbol = ""

    def __init__(self, company_symbol):
        self.model = LinearRegression()
        self.company_symbol = company_symbol

    # Function to fetch market data from API
    def get_data(self, url):
        # Our MarketStack API
        API_KEY = 'f22b6caa5edecd4bdcbc0b962fb54a71'

        # Parameters for the request (optional)
        params = {
            'access_key': API_KEY,
            'date_from': start_date,
            'date_to': end_date
        }
    
        try:
            # Endpoint URL for retrieving stock market data
            response = requests.get(url, params=params)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
            # Parse the JSON response
                data = response.json()
                # Process the data as needed
                print(data)
            else:
                print('Error:', response.status_code)
        
            # Extracting relevant information from the response
            if 'data' in data and len(data['data']) > 0:
                eod_data = data['data']['eod']
                close_prices = [day['close'] for day in eod_data]
                return np.array(close_prices)
            else:
                print("No data found for the given symbol.")
                return None
        except Exception as e:
            print("Error fetching data:", e)
            return None
        
    def calculate_CAPM(self):
        # Define the ticker symbol for the FTSE 100 index
        ticker_symbol = "^FTSE"

        # Fetch historical data
        ftse_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        x = pd.DataFrame(ftse_data)

        # calculate percentage change
        percentage_change = (x['Open']/x['Close']-1).to_numpy()

        company_data = self.get_data(f'http://api.marketstack.com/v1/tickers/{company_symbol}/eod')

        # Work out CAPM equation
        # Defining market_data and stock_data arrays using numpy arrays
        market_data = percentage_change
        stock_data = company_data

        if (market_data.size > stock_data.size):
            market_data = np.delete(market_data, 0)
        elif (stock_data.size > market_data.size):
            stock_data = np.delete(stock_data, 0)

        # Defining bond_yield, inflation, and calculating riskfree rate
        bond_yield = 5.307
        inflation = 4.0
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
        return capm, stock_data
    
    def create_dataframe(self, CAPM, stock_data):
        # Sample data for testing
        # Generate random data with a weak trend
        # np.random.seed(0)
        # num_samples = 1200
        # CAPM = np.linspace(-5, 5, num_samples) + np.random.normal(0, 0.5, num_samples)
        # Sentiment_Score = np.linspace(-0.8, 0.8, num_samples) + np.random.normal(0, 0.1, num_samples)
        # stock_price = 100 + 10 * CAPM + 50 * Sentiment_Score + np.random.normal(0, 20, num_samples)
        Sentiment_Score = np.array([0.1, 0.0087, 0.0123, -0.01, 0.001, -0.1222])
        stock_price = stock_data[-1] * CAPM * (Sentiment_Score + 1)

        # Access database and api to retrieve CAPM and Sentiment Score
        # Sentiment_Score = db. 

        # Create the dataset
        data = {
            'CAPM': CAPM,
            'Sentiment_Score': Sentiment_Score.tolist(),
            'stock_price': stock_price.tolist()
        }

        # Creating a DataFrame from the sample data
        df = pd.DataFrame(data)

        # Extracting features (independent variables) and target (dependent variables)
        X = df[['CAPM', 'Sentiment_Score']]
        y = df['stock_price']

        return X, y

    def create_test_data(self, X, y):
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

        return X_train, X_test, y_train, y_test
    
    def create_linear_model(self, X_train, X_test, y_train, y_test):
        # Creating a Linear Regression model
        model = LinearRegression()

        # Training the model on the training data
        model.fit(X_train, y_train)

        # Making predictions on the testing data
        predictions = model.predict(X_test)
        print(predictions)

        # predicted_stock_price = np.median(predictions)
        predicted_stock_price = predictions.mean()
        print('Predicted Stock Price: ', predicted_stock_price)
        # Store in database 

        # Calls Mean Absolute Evaluation method
        mae = self.MAE_evaluation(y_test, predictions)

        # Visualizing the actual vs predicted values using a scatter plot
        plt.scatter(X_test['Sentiment_Score'], y_test, color='black', label='Actual')

        # Sort X_test['Sentiment_Score'] and predictions to ensure the line of best fit is continuous
        sorted_indices = np.argsort(X_test['Sentiment_Score'])
        sorted_sentiment_score = X_test['Sentiment_Score'].iloc[sorted_indices]
        sorted_predictions = predictions[sorted_indices]

        # find line of best fit
        a, b = np.polyfit(sorted_sentiment_score, sorted_predictions, 1)
        model_equation = a*sorted_sentiment_score + b

        # Plot the line of best fit
        plt.plot(sorted_sentiment_score, model_equation, color = 'blue', linewidth=3, label="Predicted")
        plt.title('Linear Regression Model for Stock Price Prediction based on Sentiment Score')
        plt.xlabel('Sentiment Score and CAPM model')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.tight_layout()
        plt.show()

        return predicted_stock_price

    def MAE_evaluation(self, y_test, predictions):
        # Calculating Mean Absolute Error (MAE) to evaluate model performance
        mae = mean_absolute_error(y_test, predictions)
        print(f'Mean Absolute Error: {mae}')
        return mae
    
    def calculate_stock_price(self):
        capm, stock_data = self.calculate_CAPM()
        X, y = self.create_dataframe(capm, stock_data)
        X_train, X_test, y_train, y_test = self.create_test_data(X, y)
        predicted_stock_price = self.create_linear_model(X_train, X_test, y_train, y_test)
        # print(predicted_stock_price)

if __name__ == "__main__":
    company_symbol = 'AAPL'
    Linear_Regression(company_symbol).calculate_stock_price()  
