import datetime
from functools import reduce

from src.NasdaqDataCollector.DecisionTreeModel import StockDecisionTree
from src.NasdaqDataCollector.NeuralNetworkModel import NeuralNetworkModel
from src.NasdaqDataCollector.RandomForestModel import RandomForestModel
from src.NasdaqDataCollector.GBDTModel import GBDTModel
from src.NasdaqDataCollector.DataBuilder import DataBuilder


class StockPredictor:
    @staticmethod
    def predict_stock3(stock_sym, start_date=datetime.date(2017, 8, 30), end_date=datetime.date(2017, 9, 6),
                       day_diff=7):
        prediction_symbol_list = [stock_sym, ]
        pricediff_iteration = []

        for prediction_symbol in prediction_symbol_list:
            for x in range(0, 3):
                dc = DataBuilder()
                [ts, cl, td, tl, tss] = dc.get_training_and_test_data_sym2(prediction_symbol, start_date,
                                                                           end_date, day_diff)

                model1 = NeuralNetworkModel()
                model1.trainModel(ts, cl)
                model1_prediction = model1.predict_symbol(prediction_symbol)

                model2 = GBDTModel()
                model2.trainModel(ts, cl)
                model2_prediction = model2.predict_symbol(prediction_symbol)

                model3 = RandomForestModel()
                model3.trainModel(ts, cl)
                model3_prediction = model3.predict_symbol(prediction_symbol)

                model4 = StockDecisionTree()
                model4.trainModel(ts, cl)
                model4_prediction = model4.predict_symbol(prediction_symbol)

                pricediff_iteration.append((model1_prediction[0] + model2_prediction[0] +
                                            model3_prediction[0] + model4_prediction[0]) / 4)

        return reduce(lambda x, y: x + y, pricediff_iteration) / float(len(pricediff_iteration))

    @staticmethod
    def predict_stock2(stock_sym, start_date=datetime.date(2017, 8, 30), predict_range=7):
        models = [
            NeuralNetworkModel(),
            GBDTModel(),
            RandomForestModel(),
            StockDecisionTree()
        ]

        predictions = []
        for model in models:
            model.load_model(train_range=predict_range)
            prediction = model.predict_symbol(stock_sym, start_date, predict_range)
            predictions.append(prediction[0])

        return sum(predictions) / len(predictions)

    @staticmethod
    def build_models(start_date=datetime.date(2023, 1, 1), end_date=datetime.date(2025, 1, 1), train_range=7):
        dc = DataBuilder()
        [ts, cl, td, tl, tss] = dc.get_training_and_test_data_sym2("all", start_date, end_date, train_range)

        models = [NeuralNetworkModel, GBDTModel, RandomForestModel, StockDecisionTree]

        for model_class in models:
            model = model_class()
            model.trainModel(ts, cl)
            model.save_model(train_range=train_range)
