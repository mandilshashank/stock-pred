import sys
import datetime
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from NasdaqDataCollector.StockPredictor import StockPredictor

if __name__ == "__main__":
    StockPredictor.build_models()
    StockPredictor.build_models(datetime.date(2017, 8, 30), datetime.date(2017, 9, 29), train_range=30)




