import datetime
from DecisionTreeModel import StockDecisionTree
from NeuralNetworkModel import NeuralNetworkModel
from RandomForestModel import RandomForestModel
from GBDTModel import GBDTModel
from DataBuilder import DataBuilder
import pickle
import os

class StockPredictor:
    @staticmethod
    def predict_stock3(stock_sym, start_date = datetime.date(2017, 8, 30), end_date = datetime.date(2017, 9, 6)):
        prediction_symbol_list = [stock_sym,]
        pricediff_iteration = []

        for prediction_symbol in prediction_symbol_list:
            for x in range(0, 3):
                dc = DataBuilder()
                [ts, cl, td, tl, tss] = dc.get_training_and_test_data(prediction_symbol, start_date,
                                                                      end_date)

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
                                           model3_prediction[0] + model4_prediction[0])/4)


        return reduce(lambda x, y: x + y, pricediff_iteration) / float(len(pricediff_iteration))

    @staticmethod
    def build_models(start_date = datetime.date(2017, 8, 30), end_date = datetime.date(2017, 9, 6)):
        dc = DataBuilder()
        [ts, cl, td, tl, tss] = dc.get_training_and_test_data("all", start_date,
                                                              end_date)

        model1 = NeuralNetworkModel()
        model1.trainModel(ts, cl)
        model1.save_model()

        model2 = GBDTModel()
        model2.trainModel(ts, cl)
        model2.save_model()

        model3 = RandomForestModel()
        model3.trainModel(ts, cl)
        model3.save_model()

        model4 = StockDecisionTree()
        model4.trainModel(ts, cl)
        model4.save_model()

    @staticmethod
    def predict_stock2(stock_sym, start_date = datetime.date(2017, 8, 30)):
        model1 = NeuralNetworkModel()
        model1.load_model()
        model1_prediction = model1.predict_symbol(stock_sym, start_date)

        model2 = GBDTModel()
        model2.load_model()
        model2_prediction = model2.predict_symbol(stock_sym, start_date)

        model3 = RandomForestModel()
        model3.load_model()
        model3_prediction = model3.predict_symbol(stock_sym, start_date)

        model4 = StockDecisionTree()
        model4.load_model()
        model4_prediction = model4.predict_symbol(stock_sym, start_date)

        return (model1_prediction[0] + model2_prediction[0] +
                model3_prediction[0] + model4_prediction[0])/4



