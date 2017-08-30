import urllib2
import datetime
import Stock

attributes_map = {
    "previous_close":"p",
    "dividend_yield":"y",
    "dividend_per_share":"d",
    "one_yr_target_price":"t8",
    "f2_wk_high":"k",
    "f2_wk_low":"j",
    "eps":"e",
    "book_value":"b4",
    "price_per_sales":"p5",
    "price_per_book":"p6",
    "pe":"r2",
    "peg":"r5",
    "short_ratio":"s7"
}

def getUrl(stock, attributes):
    return "http://finance.yahoo.com/d/quotes.csv?s={}&f={}".format(stock, attributes)

def getStockData(stock):
    attributes = ""
    for value in attributes_map.values():
        attributes += value
    url = getUrl(stock, attributes)
    data = urllib2.urlopen(url).read()
    todays_date = datetime.date.today()

    stock_state = data.split(",")

    return [Stock.StockState(stock, todays_date, *stock_state)]

if __name__ == '__main__':
    stock_list = ["FDX", "VLO", "MSFT"]

    for stock in stock_list:
        print getStockData(stock)




