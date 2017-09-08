import datetime
from random import randint
import mysql.connector


class DataBuilder:
    def __init__(self):
        pass

    def get_training_and_test_data(self, prediction_sym):
        cnx = mysql.connector.connect(user='root', database='stock_data', password='root')
        cursor = cnx.cursor()

        query = ("SELECT * FROM stocks_snaps where date_snap = '{}'")

        stocks_date = datetime.date(2017, 8, 30)
        final_query = query.format(stocks_date)
        cursor.execute(final_query)

        training_samples = []
        class_labels = []
        test_data = []
        test_labels = []
        test_stock_sym = []

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

            if (randint(0, 100)%5 == 0 or symbol == prediction_sym):
                test_data_point = [final_previous_close, final_dividend_yield, final_dividend_per_share,
                                   final_f2_wk_high, final_f2_wk_low, final_eps,final_book_value, final_price_per_sales,
                                   final_price_per_book,final_pe, final_peg, final_short_ratio]
                test_data.append(test_data_point)
                test_labels.append(final_one_yr_target_price)
                test_stock_sym.append(symbol)

            else:
                training_sample_point = [final_previous_close, final_dividend_yield, final_dividend_per_share,
                                         final_f2_wk_high, final_f2_wk_low, final_eps,final_book_value,
                                         final_price_per_sales,final_price_per_book,final_pe, final_peg,
                                         final_short_ratio]

                training_samples.append(training_sample_point)
                class_labels.append(final_one_yr_target_price)

        cursor.close()
        cnx.close()

        return [training_samples, class_labels, test_data, test_labels, test_stock_sym]

    def get_training_and_test_data(self, prediction_sym, start_date, end_date):
        cnx = mysql.connector.connect(user='root', database='stock_data', password='root')
        cursor = cnx.cursor()

        query = """
                    SELECT
                        a.*,
                        b.previous_close-a.previous_close as price_diff
                    FROM
                    (SELECT * FROM stocks_snaps where date_snap = '{}') a
                    JOIN 
                    (SELECT * FROM stocks_snaps where date_snap = '{}') b
                    ON a.symbol = b.symbol
                """
        stocks_date = start_date
        stocks_date_later = end_date

        final_query = query.format(stocks_date, stocks_date_later)
        cursor.execute(final_query)

        training_samples = []
        class_labels = []
        test_data = []
        test_labels = []
        test_stock_sym = []

        for (id, symbol, date_snap, previous_close, dividend_yield, dividend_per_share,
             one_yr_target_price, f2_wk_high, f2_wk_low, eps, book_value, price_per_sales,
             price_per_book, pe, peg, short_ratio, price_diff) in cursor:

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
            final_price_diff = price_diff

            #randint(0, 100)%5 == 0 or
            if (symbol == prediction_sym):
                test_data_point = [final_previous_close, final_dividend_yield, final_dividend_per_share,
                                   final_f2_wk_high, final_f2_wk_low, final_eps,final_book_value, final_price_per_sales,
                                   final_price_per_book,final_pe, final_peg, final_short_ratio]
                test_data.append(test_data_point)
                test_labels.append(final_price_diff)
                test_stock_sym.append(symbol)

            else:
                training_sample_point = [final_previous_close, final_dividend_yield, final_dividend_per_share,
                                         final_f2_wk_high, final_f2_wk_low, final_eps,final_book_value,
                                         final_price_per_sales,final_price_per_book,final_pe, final_peg,
                                         final_short_ratio]

                training_samples.append(training_sample_point)
                class_labels.append(final_price_diff)

        cursor.close()
        cnx.close()

        return [training_samples, class_labels, test_data, test_labels, test_stock_sym]