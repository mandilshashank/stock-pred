from flask import Flask
from flask_restful import Resource, Api
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.NasdaqDataPolygonCollector.DataModelPredictor import DataModelPredictor

app = Flask(__name__)
api = Api(app)

class DataStockPredict(Resource):
    def get(self, stock_symbol, predict_length):
        predictor = DataModelPredictor(stock_symbol, predict_length)
        prediction, mse, rmse = predictor.predict_tomorrow()
        return {'prediction': prediction, 'mse': mse, 'rmse': rmse}

api.add_resource(DataStockPredict, '/datapredict/<stock_symbol>/<predict_length>')

if __name__ == '__main__':
    app.run(port=5003)