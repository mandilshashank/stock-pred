# File: create_stocks_polygon_table.py

import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    'user': 'root',
    'password': 'StockMarket1234!',
    'host': '127.0.0.1'
}

# SQL query to create the stocks_pred database
create_database_query = "CREATE DATABASE IF NOT EXISTS stocks_pred"

# SQL query to create the stocks_polygon table
create_table_query = """
CREATE TABLE IF NOT EXISTS stocks_polygon (
    ticker VARCHAR(10) NOT NULL,
    todays_change_percentage DOUBLE,
    todays_change DOUBLE,
    updated BIGINT,
    day_open DOUBLE,
    day_high DOUBLE,
    day_low DOUBLE,
    day_close DOUBLE,
    day_volume DOUBLE,
    day_vw DOUBLE,
    minute_open DOUBLE,
    minute_high DOUBLE,
    minute_low DOUBLE,
    minute_close DOUBLE,
    minute_volume INT,
    minute_vw DOUBLE,
    previous_day_open DOUBLE,
    previous_day_high DOUBLE,
    previous_day_low DOUBLE,
    previous_day_close DOUBLE,
    previous_day_volume DOUBLE,
    previous_day_vw DOUBLE,
    PRIMARY KEY (ticker, updated)
);
"""

try:
    # Connect to the MySQL server
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Create the stocks_pred database if it does not exist
    cursor.execute(create_database_query)
    print("Database `stocks_pred` checked/created successfully.")

    # Connect to the stocks_pred database
    cnx.database = 'stocks_pred'

    # Execute the SQL query to create the table
    cursor.execute(create_table_query)
    print("Table `stocks_polygon` created successfully in the `stocks_pred` database.")

    # Close the cursor and connection
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist and could not be created")
    else:
        print(err)