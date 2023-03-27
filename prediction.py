import numpy as np
import pandas as pd
import datetime
from configparser import ConfigParser
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import Adam
import matplotlib.pyplot as plt

# Import the Alpaca library
import alpaca_trade_api as tradeapi
# Grab configuration values.
config = ConfigParser()
config.read('config/config.ini')

api_key = config.get('main', 'API_KEY')
secret_key = config.get('main', 'SECRET_KEY')

# Initialize API
api = tradeapi.REST(api_key, secret_key)

# Get the historical data for Intel
symbol = "INTC"
timeframe = "1Day"
tz = datetime.timezone.utc
today = datetime.date.today()
start_time = datetime.date(today.year - 1, today.month, today.day)
end_time = None # Current Time

bars = api.get_bars(symbol, timeframe, start_time.isoformat())

# Create a list of closing prices
data = []
for bar in bars:
    data.append(bar.c)

# Load the stock data
#data = pd.read_csv('intel_stock.csv')

# Extract the closing price
prices = pd.DataFrame(data).to_numpy()
#prices.reshape(-1, 1)

# Scale the data
scaler = MinMaxScaler()
prices_scaled = scaler.fit_transform(prices)

# Define the number of time steps (days)
time_steps = 30

# Create training and test sets
X_train, y_train = [], []
for i in range(time_steps, len(prices_scaled)):
    X_train.append(prices_scaled[i-time_steps:i])
    y_train.append(prices_scaled[i])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape the data for the RNN
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Define the model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(1))

# Compile the model
model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=32)

# Create test set
X_test = []
for i in range(time_steps, len(prices_scaled)):
    X_test.append(prices_scaled[i-time_steps:i])
X_test = np.array(X_test)

# Reshape the data for the RNN
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Evaluate the model on the testing set
test_loss = model.evaluate(X_test)
print(f"Test Loss: {test_loss}")

# Make predictions
predictions = model.predict(X_test)

# Inverse transform the predictions
predictions = scaler.inverse_transform(predictions)

# Plot the predictions and the real data
plt.plot(prices, label='Real Data')
plt.plot(predictions, label='Predictions')
plt.legend()
plt.show()

# Print the predictions
#print(predictions)