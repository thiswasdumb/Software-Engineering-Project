# Importing necessary libraries
from flask import Flask
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
# from TradeTalker_DB import Database

# Initialising Flask application 
app = Flask(__name__)

# Configuration for MySQL database connection
# 'TradeTalkerDB' is the name of the MySQL database
# 'DictCursor' returns rows as dictionaries, making them easier to work with
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'TradeTalkerDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# db = Database(app)
# Reading the dataset (add path to dataset in quotes)
# data = pd.read_csv("")

# Sample data for testing
data = {
    'CAPM': [1.5, 2.0, 3.0, 4.0, 5.0, 1.5, 2.0, 3.0, 4.0, 5.0, 1.5, 2.0, 3.0, 4.0, 5.0, 1.0], 
    'Sentiment_Score': [0.7, 0.8, 0.6, 0.4, 0.2, 0.34, 0.85, 0.98, 0.65, 0.56, 0.67, 0.93, 0.48, 0.78, 0.56, 0.23], 
    'stock_price': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
}
# change in stock price percentage positive and negative, ask chatgpt 

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
plt.plot(X_test['Sentiment_Score'], predictions, color='blue', linewidth=3, label='Predicted')
plt.title('Linear Regression Model for Stock Price Prediction based on Sentiment Score')
plt.xlabel('Sentiment Score and CAPM model')
plt.ylabel('Stock Price')
plt.legend()
plt.tight_layout()
plt.show()
