import datetime
from flask import Flask, request
from flask_restful import Resource, Api
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from NasdaqDataCollector.StockPredictor import StockPredictor
from NasdaqDataCollector.ModelRunner import ModelRunner

app = Flask(__name__)
api = Api(app)

class Prediction(Resource):
    def get(self, stock_symbol, sd=30, sm=8, sy=2017, ed=6, em=9, ey=2017):
        stock_pred = StockPredictor.predict_stock3(stock_symbol, datetime.date(int(sy),int(sm),int(sd)),
                                                  datetime.date(int(ey),int(em),int(ed)))
        return ({'prediction': stock_pred})

class PredictionLearned(Resource):
    def get(self, stock_symbol, sd=30, sm=8, sy=2017):
        stock_pred = StockPredictor.predict_stock2(stock_symbol, datetime.date(int(sy),int(sm),int(sd)))
        return ({'prediction': stock_pred})

class PredictYearTarget(Resource):
    def get(self, stock_symbol, sd=30, sm=8, sy=2017):
        stock_pred = ModelRunner.predict_year_target(stock_symbol, datetime.date(int(sy),int(sm),int(sd)))
        return ({'data': stock_pred})

api.add_resource(Prediction, '/prediction/<stock_symbol>', '/prediction/<stock_symbol>/<sd>/<sm>/<sy>/<ed>/<em>/<ey>')
api.add_resource(PredictionLearned, '/prediction/<stock_symbol>/<sd>/<sm>/<sy>')
api.add_resource(PredictYearTarget, '/prediction_year/<stock_symbol>', '/prediction_year/<stock_symbol>/<sd>/<sm>/<sy>')

if __name__ == '__main__':
    app.run(port='5002')