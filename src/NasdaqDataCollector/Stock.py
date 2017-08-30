class Stock :
    def __init__(self, symbol = "", description = ""):
        """ Create a new point at the origin """
        self.symbol = symbol
        self.description = description

class StockState:
    def __init__(self, symbol= "", date = "", f2_wk_low="", previous_close="", dividend_yield="", dividend_per_share="",
                 one_yr_target_price="", f2_wk_high="", eps="", book_value="", price_per_sales="", price_per_book="",
                 pe="", peg="", short_ratio=""):
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

