import joblib
import pandas as pd
import mysql.connector

class DataModelPredictor:
    def __init__(self, ticker, prediction_length):
        self.ticker = ticker
        self.prediction_length = prediction_length
        self.model_filename, self.window_size, self.mse, self.rmse = self.get_model_info_from_db()
        self.model = joblib.load(self.model_filename)

    def get_model_info_from_db(self):
        db_connection = mysql.connector.connect(
            host="localhost",
            user='root',
            database='stock_pred',
            password='root1234'
        )
        cursor = db_connection.cursor()

        query = """
        SELECT model_name, window_size, mse, rmse
        FROM model_info
        WHERE ticker = %s AND prediction_length = %s
        ORDER BY created_at DESC
        LIMIT 1
        """
        cursor.execute(query, (self.ticker, self.prediction_length))
        result = cursor.fetchone()

        cursor.close()
        db_connection.close()

        if result:
            return result[0], result[1], result[2], result[3]
        else:
            raise ValueError("No model found for the given ticker and prediction length")

    def get_last_x_days_data(self, x):
        db_connection = mysql.connector.connect(
            host="localhost",
            user='root',
            database='stock_pred',
            password='root1234'
        )
        cursor = db_connection.cursor(dictionary=True)

        query = """
        SELECT date, open, high, low, close, volume
        FROM stock_data
        WHERE ticker = %s
        ORDER BY date DESC
        LIMIT %s
        """
        cursor.execute(query, (self.ticker, x))
        data = cursor.fetchall()
        data.reverse()  # Reverse to maintain chronological order

        cursor.close()
        db_connection.close()

        return data

    def prepare_features(self, data):
        feature = []
        for day in data:
            feature.extend([day['open'], day['high'], day['low'], day['close'], day['volume']])
        return pd.DataFrame([feature])

    def predict_tomorrow(self):
        data = self.get_last_x_days_data(self.window_size)
        features = self.prepare_features(data)
        prediction = self.model.predict(features)
        return prediction[0], self.mse, self.rmse

if __name__ == '__main__':
    ticker = 'AAPL'
    prediction_length = '1week'
    predictor = DataModelPredictor(ticker, prediction_length)
    print(f"Model window size: {predictor.window_size}")
    prediction, mse, rmse = predictor.predict_tomorrow()
    print(f"Predicted closing price for {ticker} tomorrow: {prediction}")
    print(f"MSE: {mse}, RMSE: {rmse}")