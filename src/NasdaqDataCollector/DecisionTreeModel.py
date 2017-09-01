import datetime
import mysql.connector
from sklearn import tree
from sklearn.metrics import mean_squared_error


class StockDecisionTree:
    def __init__(self):
        self.model = ""

    def trainModel(self, training_samples, class_labels):
        clf = tree.DecisionTreeRegressor()
        self.model = clf.fit(training_samples, class_labels)

    def predict(self, test_data):
        if self.model != "":
            return self.model.predict(test_data)
        else:
            raise Exception("You must train the model before trying to predict the outcome")

    def predict_symbol(self, symbol):
        cnx = mysql.connector.connect(user='root', database='stock_data', password='root')
        cursor = cnx.cursor()

        query = ("SELECT * FROM stocks_snaps where date_snap = '{}' and symbol='{}'")

        stocks_date = datetime.date(2017, 8, 30)
        final_query = query.format(stocks_date, symbol)
        cursor.execute(final_query)

        test_data = []

        for (id, symbol, date_snap, previous_close, dividend_yield, dividend_per_share,
             one_yr_target_price, f2_wk_high, f2_wk_low, eps, book_value, price_per_sales,
             price_per_book, pe, peg, short_ratio) in cursor:

            final_previous_close = 0 if previous_close.find('N') > -1 else float(previous_close)
            final_dividend_yield = 0 if dividend_yield.find('N') > -1 else float(dividend_yield)
            final_dividend_per_share = 0 if dividend_per_share.find('N') > -1 else float(dividend_per_share)
            final_f2_wk_high = 0 if f2_wk_high.find('N') > -1 else float(f2_wk_high)
            final_f2_wk_low = 0 if f2_wk_low.find('N') > -1 else float(f2_wk_low)
            final_eps = 0 if eps.find('N') > -1 else float(eps)
            final_book_value = 0 if book_value.find('N') > -1 else float(book_value)
            final_price_per_sales = 0 if price_per_sales.find('N') > -1 else float(price_per_sales)
            final_price_per_book = 0 if price_per_book.find('N') > -1 else float(price_per_book)
            final_pe = 0 if pe.find('N') > -1 else float(pe)
            final_peg = 0 if peg.find('N') > -1 else float(peg)
            final_short_ratio = 0 if short_ratio.find('N') > -1 else float(short_ratio)
            final_one_yr_target_price = final_previous_close if one_yr_target_price.find('N') > -1 \
                else float(one_yr_target_price)


            test_data_point = [final_previous_close, final_dividend_yield, final_dividend_per_share,
                               final_f2_wk_high, final_f2_wk_low, final_eps,final_book_value, final_price_per_sales,
                               final_price_per_book,final_pe, final_peg, final_short_ratio]
            test_data.append(test_data_point)

        cursor.close()
        cnx.close()

        return self.model.predict(test_data)

    def model_mse(self, test_data, test_labels):
        if self.model != "":
            return mean_squared_error(test_labels, self.model.predict(test_data))
        else:
            raise Exception("You must train the model before trying to predict the outcome")