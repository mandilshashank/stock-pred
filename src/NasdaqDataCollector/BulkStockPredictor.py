import datetime

from src.NasdaqDataCollector.ModelRunner import ModelRunner

if __name__ == '__main__':

    top_30 = ['TSLA', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'NVDA', 'HD', 'MA', 'PYPL', 'BAC', 'DIS', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'GOOG', 'INTC', 'VZ', 'ADBE', 'CSCO', 'KO', 'T', 'PFE', 'WMT', 'ABT', 'MRK',
              'CVX']

    for stock in top_30:
        sy = '2023'
        sm = '04'
        sd = '10'
        print('Getting data for ' + stock)
        stock_pred = ModelRunner.predict_year_target(stock, datetime.date(int(sy), int(sm), int(sd)))
        print({'data': stock_pred})