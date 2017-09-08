import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from src.NasdaqDataCollector.StockPredictor import StockPredictor

app = Flask(__name__)
api = Api(app)

class Prediction(Resource):
    def get(self, stock_symbol, sd=30, sm=8, sy=2017, ed=6, em=9, ey=2017):
        stock_pred = StockPredictor.predict_stock(stock_symbol, datetime.date(int(sy),int(sm),int(sd)),
                                                  datetime.date(int(ey),int(em),int(ed)))
        return ({'prediction': stock_pred})

api.add_resource(Prediction, '/prediction/<stock_symbol>', '/prediction/<stock_symbol>/<sd>/<sm>/<sy>/<ed>/<em>/<ey>')


if __name__ == '__main__':
    app.run(port='5002')
