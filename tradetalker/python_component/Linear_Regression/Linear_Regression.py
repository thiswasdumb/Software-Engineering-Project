# Importing necessary libraries
from flask import Flask
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from TradeTalker_DB import Database

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

db = Database(app)

# Reading the dataset (add path to dataset in quotes)
data = pd.read_csv("")

# Extracting features (independent variables) and target (dependent variables)
X = data[['CAPM', 'Sentiment_Score']]
y = data['stock_price']


# Splitting the dataset into training and testing sets
# test_size=0.2 implies that 20% of the data will be used for testing
# random_state is set for reproducibility of results
X_train, X_test, y_train, y_test = train_test_split(X, y, test_score=0.2, random_state=18)

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
plt.scatter(X_test, y_test, color='black')
plt.plot(X_test, predictions, color='blue', linewidth=3)
plt.title('Linear Regression Model for Stock Price Prediction based on Sentiment Score')
plt.xlabel('Sentiment Score and CAPM model')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
