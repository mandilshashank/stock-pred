from __future__ import print_function
import mysql.connector


class StockPolygon:
    def __init__(self, ticker="", todays_change_percentage=0.0, todays_change=0.0, updated=0, day_open=0.0,
                 day_high=0.0, day_low=0.0, day_close=0.0, day_volume=0.0, day_vw=0.0, minute_open=0.0, minute_high=0.0,
                 minute_low=0.0, minute_close=0.0, minute_volume=0, minute_vw=0.0, previous_day_open=0.0,
                 previous_day_high=0.0, previous_day_low=0.0, previous_day_close=0.0, previous_day_volume=0.0,
                 previous_day_vw=0.0):
        self.ticker = ticker
        self.todays_change_percentage = todays_change_percentage
        self.todays_change = todays_change
        self.updated = updated
        self.day_open = day_open
        self.day_high = day_high
        self.day_low = day_low
        self.day_close = day_close
        self.day_volume = day_volume
        self.day_vw = day_vw
        self.minute_open = minute_open
        self.minute_high = minute_high
        self.minute_low = minute_low
        self.minute_close = minute_close
        self.minute_volume = minute_volume
        self.minute_vw = minute_vw
        self.previous_day_open = previous_day_open
        self.previous_day_high = previous_day_high
        self.previous_day_low = previous_day_low
        self.previous_day_close = previous_day_close
        self.previous_day_volume = previous_day_volume
        self.previous_day_vw = previous_day_vw


class StockStatePolygon:
    def __init__(self, ticker="", todays_change_percentage=0.0, todays_change=0.0, updated=0, day_open=0.0,
                 day_high=0.0, day_low=0.0, day_close=0.0, day_volume=0.0, day_vw=0.0, minute_open=0.0, minute_high=0.0,
                 minute_low=0.0, minute_close=0.0, minute_volume=0, minute_vw=0.0, previous_day_open=0.0,
                 previous_day_high=0.0, previous_day_low=0.0, previous_day_close=0.0, previous_day_volume=0.0,
                 previous_day_vw=0.0):
        self.stock_polygon = StockPolygon(ticker, todays_change_percentage, todays_change, updated, day_open, day_high,
                                          day_low, day_close, day_volume, day_vw, minute_open, minute_high, minute_low,
                                          minute_close, minute_volume, minute_vw, previous_day_open, previous_day_high,
                                          previous_day_low, previous_day_close, previous_day_volume, previous_day_vw)

    def save_to_db(self):
        cnx = mysql.connector.connect(user='root', database='stock_pred', password='StockMarket1234!')
        cursor = cnx.cursor()

        add_stock_polygon = ("INSERT INTO stocks_polygon "
                             "(ticker, todays_change_percentage, todays_change, updated, day_open, day_high, day_low, "
                             "day_close, day_volume, day_vw, minute_open, minute_high, minute_low, minute_close, "
                             "minute_volume, minute_vw, previous_day_open, previous_day_high, previous_day_low, "
                             "previous_day_close, previous_day_volume, previous_day_vw)"
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                             "%s, %s)")

        data_stock_polygon = (
            self.stock_polygon.ticker, self.stock_polygon.todays_change_percentage, self.stock_polygon.todays_change,
            self.stock_polygon.updated, self.stock_polygon.day_open, self.stock_polygon.day_high,
            self.stock_polygon.day_low, self.stock_polygon.day_close, self.stock_polygon.day_volume,
            self.stock_polygon.day_vw, self.stock_polygon.minute_open, self.stock_polygon.minute_high,
            self.stock_polygon.minute_low, self.stock_polygon.minute_close, self.stock_polygon.minute_volume,
            self.stock_polygon.minute_vw, self.stock_polygon.previous_day_open, self.stock_polygon.previous_day_high,
            self.stock_polygon.previous_day_low, self.stock_polygon.previous_day_close,
            self.stock_polygon.previous_day_volume, self.stock_polygon.previous_day_vw)

        cursor.execute(add_stock_polygon, data_stock_polygon)
        cnx.commit()

        cursor.close()
        cnx.close()
