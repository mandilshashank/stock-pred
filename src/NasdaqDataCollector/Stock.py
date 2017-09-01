from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

class Stock :
    def __init__(self, symbol = "", description = ""):
        """ Create a new point at the origin """
        self.symbol = symbol
        self.description = description

class StockState:
    def __init__(self, symbol= "", date = "", previous_close="", dividend_yield="", dividend_per_share="",
                 one_yr_target_price="", f2_wk_high="", f2_wk_low="", eps="", book_value="", price_per_sales="",
                 price_per_book="", pe="", peg="", short_ratio=""):
        self.stock = Stock(symbol)
        self.date = date
        self.previous_close = previous_close

        self.dividend_yield = dividend_yield
        self.dividend_per_share = dividend_per_share

        self.one_yr_target_price = one_yr_target_price
        self.f2_wk_high = f2_wk_high
        self.f2_wk_low = f2_wk_low

        self.eps = eps
        self.book_value = book_value
        self.price_per_sales = price_per_sales
        self.price_per_book = price_per_book
        self.pe = pe
        self.peg = peg
        self.short_ratio = short_ratio

    def save_to_db(self):
        cnx = mysql.connector.connect(user='root', database='stock_data', password='root')
        cursor = cnx.cursor()

        today = datetime.now().date()

        add_stock = ("INSERT INTO stocks_snaps "
                        "(symbol, date_snap, previous_close, dividend_yield, dividend_per_share, one_yr_target_price,"
                        " f2_wk_high, f2_wk_low, eps, book_value, price_per_sales, price_per_book, pe, peg, short_ratio)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        data_stock = (self.stock.symbol, self.date, self.previous_close, self.dividend_yield, self.dividend_per_share,
                      self.one_yr_target_price, self.f2_wk_high, self.f2_wk_low, self.eps, self.book_value,
                      self.price_per_sales, self.price_per_book.strip(), self.pe, self.peg, self.short_ratio)

        # Insert new stock
        cursor.execute(add_stock, data_stock)
        id = cursor.lastrowid

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()