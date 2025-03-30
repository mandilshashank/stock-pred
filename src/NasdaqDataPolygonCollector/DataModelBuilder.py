import math

import joblib
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class DataModelBuilder:
    def __init__(self, data):
        self.data = data

    def generate_features(self, window_size=10):
        features = []
        targets = []

        for i in range(len(self.data) - window_size):
            window_data = self.data[i:i + window_size]
            next_day_close = self.data[i + window_size]['close']

            feature = []
            for day in window_data:
                feature.extend([day['open'], day['high'], day['low'], day['close'], day['volume']])

            features.append(feature)
            targets.append(next_day_close)

        return pd.DataFrame(features), pd.Series(targets)


def generate_features(data, window_size=10):
    features = []
    targets = []

    for i in range(len(data) - window_size):
        window_data = data[i:i + window_size]
        next_day_close = data[i + window_size]['close']

        feature = []
        for day in window_data:
            feature.extend([day['open'], day['high'], day['low'], day['close'], day['volume']])

        features.append(feature)
        targets.append(next_day_close)

    return pd.DataFrame(features), pd.Series(targets)


def get_previous_year_stock_data_from_db(ticker):
    db_connection = mysql.connector.connect(
        host="localhost",
        user='root',
        database='stock_pred',
        password='root1234'
    )
    cursor = db_connection.cursor(dictionary=True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    query = f"""
    SELECT date, open, high, low, close, volume
    FROM stock_data
    WHERE ticker = %s AND date BETWEEN %s AND %s
    ORDER BY date ASC
    """
    cursor.execute(query, (ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    data = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return data


def train_and_evaluate_model(ticker, window_size):
    data = get_previous_year_stock_data_from_db(ticker)
    features, targets = generate_features(data, window_size)

    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

    gbdt = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    gbdt.fit(X_train, y_train)

    y_pred = gbdt.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return gbdt, mse


if __name__ == '__main__':
    top_30 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'GOOG', 'INTC', 'VZ', 'ADBE', 'CSCO', 'KO', 'T', 'PFE', 'WMT',
              'ABT', 'MRK', 'CVX']
    window_sizes = [5, 10, 15, 20]

    for ticker in top_30:
        best_window_size = None
        lowest_mse = float('inf')
        best_model = None

        for window_size in window_sizes:
            model, mse = train_and_evaluate_model(ticker, window_size)
            print(f"Ticker: {ticker}, Window Size: {window_size}, Mean Squared Error: {mse}")
            if mse < lowest_mse:
                lowest_mse = mse
                best_window_size = window_size
                best_model = model

        print(f"Ticker: {ticker}, Best Window Size: {best_window_size}, Lowest Mean Squared Error: {lowest_mse}")

        # Save the best model to a file with ticker and window_size in the name
        model_filename = f'best_gbdt_model_{ticker}_window{best_window_size}.pkl'
        joblib.dump(best_model, model_filename)
        print(f"Best model saved as {model_filename}")

        rmse = math.sqrt(lowest_mse)
        print(f"Ticker: {ticker}, Root Mean Squared Error: {rmse}")
