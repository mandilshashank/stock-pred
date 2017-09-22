import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from NasdaqDataCollector.StockPredictor import StockPredictor

if __name__ == "__main__":
    StockPredictor.build_models()




