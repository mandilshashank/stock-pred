import datetime
from DecisionTreeModel import StockDecisionTree
from NeuralNetworkModel import NeuralNetworkModel
from RandomForestModel import RandomForestModel
from GBDTModel import GBDTModel
from DataBuilder import DataBuilder

class StockPredictor:
    @staticmethod
    def predict_stock(stock_sym, start_date = datetime.date(2017, 8, 30), end_date = datetime.date(2017, 9, 6)):
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





