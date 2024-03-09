"""Uses linear regression to predict stock prices based on CAPM and sentiment score."""

from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from requests import RequestException
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

OK = 200

# start_date is set to 7 days before today's date
start_date = (datetime.now(UTC) - timedelta(days=7)).strftime("%Y-%m-%d")
# end_date is set to today's date in the format YYYY-MM-DD
end_date = datetime.now(UTC).strftime("%Y-%m-%d")


class TTLinearRegression:
    """Uses linear regression to predict stock prices based on CAPM and sentiment
    score.
    """

    def __init__(
        self,
        company_symbol: str,
        sentiment_score: list,
        company_data: list,
    ) -> None:
        """Initializes the TTLinearRegression class with the provided parameters."""
        # Constructor Method
        # Initialize the model as a Linear Regression model
        self.model = LinearRegression()
        # Assign the provided company_symbol to the instance variable
        self.company_symbol = company_symbol
        # Assign the provided sentiment_score to the instance variable
        self.sentiment_score = sentiment_score
        # Assign the provided company_data to the instance variable
        self.company_data = company_data

    def get_data(self, url: str) -> np.ndarray | None:
        """Fetches stock market data from the MarketStack API."""
        # Our MarketStack API
        api_key = "f22b6caa5edecd4bdcbc0b962fb54a71"

        # Parameters for the request (optional)
        params = {"access_key": api_key, "date_from": start_date, "date_to": end_date}

        try:
            # Endpoint URL for retrieving stock market data
            response = requests.get(url, params=params, timeout=10)

            # Check if the request was successful (status code 200)
            if response.status_code == OK:
                # Parse the JSON response
                data = response.json()
                # Process the data as needed
                print(data)
            else:
                print("Error:", response.status_code)

            # Extracting relevant information from the response
            if "data" in data and len(data["data"]) > 0:
                eod_data = data["data"]["eod"]
                close_prices = [day["close"] for day in eod_data]
                return np.array(close_prices)
        except RequestException as e:
            print("Error fetching data:", e)
            return None
        else:
            print("No data found for the given symbol.")
            return None

    def calculate_capm(self) -> tuple[float, np.ndarray]:
        """Calculates the Capital Asset Pricing Model (CAPM) using historical data."""
        # Define the ticker symbol for the FTSE 100 index
        ticker_symbol = "^FTSE"

        # Fetch historical data
        ftse_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        x = pd.DataFrame(ftse_data)

        # calculate percentage change
        percentage_change = (x["Open"] / x["Close"] - 1).to_numpy()

        # Work out CAPM equation
        # Defining market_data and stock_data arrays using numpy arrays
        market_data = percentage_change
        stock_data = np.array(self.company_data)

        if market_data.size > stock_data.size:
            market_data = np.delete(market_data, 0)
        elif stock_data.size > market_data.size:
            stock_data = np.delete(stock_data, 0)

        # Defining bond_yield, inflation, and calculating riskfree rate
        bond_yield = 5.307
        inflation = 4.0
        riskfree = bond_yield - inflation

        # Calculating covariance, variance, and mean of market_data
        # Covariance between market_data and stock_data
        cv: float = np.cov(market_data, stock_data)[0][1].item()

        # Variance of market_data
        mv = np.var(market_data).item()

        # Mean of market_data
        mr = np.mean(market_data).item()

        # Calculating beta using CAPM formula
        # Beta coefficient
        b = (mr * cv) / mv

        # Capital Asset Pricing Model (CAPM) calculation
        capm = riskfree + b * (mr - riskfree)

        # Percentage Change
        capm = capm / 100

        # Printing the calculated CAPM value
        return capm, stock_data

    def create_dataframe(self, capm: float, stock_data: np.ndarray) -> tuple:
        """Creates a dataframe using CAPM and stock data."""
        # Access database and api to retrieve sentiment score and CAPM
        print("CAPM: ", capm)
        sentiment = np.array(self.sentiment_score)
        if len(self.sentiment_score) == 0 or len(self.sentiment_score) == 1:
            sentiment = np.append(sentiment, [0, 0])

        # Calculate stock price with a scaling factor of 0.1 to not cause unnecessary
        # rapid increase
        stock_price = stock_data[-1] * (capm + 1) * ((sentiment * 0.1) + 1)

        # Create the dataset
        data = {
            "CAPM": capm,
            "sentiment_score": sentiment.tolist(),
            "stock_price": stock_price.tolist(),
        }

        # Creating a DataFrame from the sample data
        stocks_df = pd.DataFrame(data)

        # Extracting features (independent variables) and target (dependent variables)
        x = stocks_df[["CAPM", "sentiment_score"]]
        y = stocks_df["stock_price"]

        return x, y

    def create_test_data(self, x: tuple, y: tuple) -> tuple[list, list, list, list]:
        """Creates training and testing data for the model."""
        # Splitting the dataset into training and testing sets
        # test_size=0.2 implies that 20% of the data will be used for testing
        # random_state is set for reproducibility of results
        X_train, X_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.5,
            random_state=18,
        )

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

    def create_linear_model(
        self,
        X_train: list,
        X_test: list,
        y_train: list,
        y_test: list,
    ) -> float:
        """Creates a Linear Regression model and predicts stock prices."""
        # Creating a Linear Regression model
        model = LinearRegression()

        # Training the model on the training data
        model.fit(X_train, y_train)

        # Making predictions on the testing data
        predictions = model.predict(X_test)

        # predicted_stock_price = np.median(predictions)
        predicted_stock_price = predictions.mean()

        # Calls Mean Absolute Evaluation method
        mae = self.mae_evaluation(y_test, predictions)

        # Visualizing the actual vs predicted values using a scatter plot
        # plt.scatter(X_test["sentiment_score"], y_test, color="black", label="Actual")

        return predicted_stock_price

    def mae_evaluation(self, y_test: list, predictions: np.ndarray) -> float:
        """Calculates Mean Absolute Error (MAE) to evaluate model performance."""
        mae = mean_absolute_error(y_test, predictions)
        print(f"Mean Absolute Error: {mae}")
        return mae

    def calculate_stock_price(self) -> float:
        """Calculates the stock price using Linear Regression."""
        # Calculate CAPM and get historical stock data
        capm, stock_data = self.calculate_capm()
        # Create a dataframe using CAPM and stock data
        x, y = self.create_dataframe(capm, stock_data)
        # Split the dataset into training and testing data
        X_train, X_test, y_train, y_test = self.create_test_data(x, y)
        # Create a linear regression model and predict the stock price
        predicted_stock_price = self.create_linear_model(
            X_train,
            X_test,
            y_train,
            y_test,
        )
        # Print the predicted stock price
        print("Predicted Stock Price: ", predicted_stock_price)
        return predicted_stock_price


if __name__ == "__main__":
    comp_symbol = "UU.L"
    sent_score: list = []
    comp_data = [175.55, 176.887, 174.987, 179.555, 180.454]
    # Create an instance of the Linear_Regression class with provided parameters and
    # calculate the stock price
    pred_stock_price = TTLinearRegression(
        comp_symbol,
        sent_score,
        comp_data,
    ).calculate_stock_price()
