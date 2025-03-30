import math
import os

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

        for i in range(len(self.data) - window_size - 5):  # 5 trading days in a week
            window_data = self.data[i:i + window_size]
            next_week_close = self.data[i + window_size + 5]['close']

            feature = []
            for day in window_data:
                feature.extend([day['open'], day['high'], day['low'], day['close'], day['volume']])

            features.append(feature)
            targets.append(next_week_close)

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

def train_and_evaluate_model(ticker, window_sizes):
    data = get_previous_year_stock_data_from_db(ticker)
    best_model = None
    lowest_mse = float('inf')
    best_window_size = None

    for window_size in window_sizes:
        builder = DataModelBuilder(data)
        features, targets = builder.generate_features(window_size)

        X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

        gbdt = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        gbdt.fit(X_train, y_train)

        y_pred = gbdt.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        if mse < lowest_mse:
            lowest_mse = mse
            best_model = gbdt
            best_window_size = window_size

    return best_model, best_window_size, lowest_mse

def create_model_info_table_if_not_exists():
    db_connection = mysql.connector.connect(
        host="localhost",
        user='root',
        database='stock_pred',
        password='root1234'
    )
    cursor = db_connection.cursor()

    # Check if the table exists
    cursor.execute("""
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_name = 'model_info'
    """)
    if cursor.fetchone()[0] == 0:
        # Create the table if it does not exist
        cursor.execute("""
        CREATE TABLE model_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model_name VARCHAR(255),
            ticker VARCHAR(10),
            window_size INT,
            mse FLOAT,
            rmse FLOAT,
            prediction_length VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        db_connection.commit()

    cursor.close()
    db_connection.close()

def save_model_info_to_db(model_filename, ticker, window_size, mse, rmse, prediction_length):
    db_connection = mysql.connector.connect(
        host="localhost",
        user='root',
        database='stock_pred',
        password='root1234'
    )
    cursor = db_connection.cursor()

    query = """
    INSERT INTO model_info (model_name, ticker, window_size, mse, rmse, prediction_length)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (model_filename, ticker, window_size, mse, rmse, prediction_length))
    db_connection.commit()

    cursor.close()
    db_connection.close()

if __name__ == '__main__':
    ticker = 'AAPL'
    window_sizes = [5, 10, 15, 20]
    prediction_length = '1week'

    best_model, best_window_size, lowest_mse = train_and_evaluate_model(ticker, window_sizes)
    print(f"Ticker: {ticker}, Best Window Size: {best_window_size}, Lowest Mean Squared Error: {lowest_mse}")

    # Create the models directory if it doesn't exist
    models_dir = '../models'
    os.makedirs(models_dir, exist_ok=True)

    # Save the best model to a file with ticker and window_size in the name
    model_filename = os.path.join(models_dir, f'best_gbdt_model_{ticker}_window{best_window_size}_{prediction_length}.pkl')
    joblib.dump(best_model, model_filename)
    print(f"Best model saved as {model_filename}")

    rmse = math.sqrt(lowest_mse)
    print(f"Ticker: {ticker}, Root Mean Squared Error: {rmse}")

    # Call the function to ensure the table is created
    create_model_info_table_if_not_exists()

    # Save model information to the database
    save_model_info_to_db(model_filename, ticker, best_window_size, lowest_mse, rmse, prediction_length)