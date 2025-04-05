import os
from urllib.request import urlopen
import ssl
import certifi
import json
from datetime import datetime, timedelta
import mysql.connector

def get_previous_year_stock_data(ticker):
    api_key = os.getenv("POLYGON_API_KEY")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1825)
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}?apiKey={api_key}"

    try:
        context = ssl.create_default_context(cafile=certifi.where())
        data = urlopen(url, context=context).read()

        # Parse the JSON object
        parsed_data = json.loads(data)
        return parsed_data['results']
    except (KeyError, TypeError, json.JSONDecodeError):
        return None

def save_to_db(data, ticker):
    db_connection = mysql.connector.connect(
        host="localhost",
        user='root',
        database='stock_pred',
        password='StockMarket1234!'
    )
    cursor = db_connection.cursor()

    # Create table if it doesn't exist
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS stock_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ticker VARCHAR(10),
        date DATE,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT
    )
    """)

    # Insert data into the table
    for day_data in data:
        cursor.execute(f"""
        INSERT INTO stock_data (ticker, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (ticker, datetime.fromtimestamp(day_data['t'] / 1000).strftime('%Y-%m-%d'), day_data['o'], day_data['h'], day_data['l'], day_data['c'], day_data['v']))

    db_connection.commit()
    cursor.close()
    db_connection.close()

# Example usage
if __name__ == '__main__':
    ticker = "WDAY"
    top_30 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'GOOG', 'INTC', 'VZ', 'ADBE', 'CSCO', 'KO', 'T', 'PFE', 'WMT',
              'ABT', 'MRK',
              'CVX']
    for stock in top_30:
        stock_data = get_previous_year_stock_data(stock)
        if stock_data:
            save_to_db(stock_data, stock)
            print(f"Data saved to database successfully for {stock}")
        else:
            print(f"Failed to retrieve data for {stock}")
    stock_data = get_previous_year_stock_data(ticker)