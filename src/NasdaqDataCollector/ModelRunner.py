from DecisionTreeModel import StockDecisionTree
from NeuralNetworkModel import NeuralNetworkModel
from RandomForestModel import RandomForestModel
from GBDTModel import GBDTModel
import datetime
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import DataBuilder
import json

class ModelRunner:
    @staticmethod
    def predict_year_target(prediction_symbol = "FDX", start_date = datetime.date(2017, 8, 30)):
        dc = DataBuilder()
        [ts, cl, td, tl, tss] = dc.get_training_and_test_data_sym(prediction_symbol, start_date)

        data = {}

        nn={}
        model1 = NeuralNetworkModel()
        model1.trainModel(ts, cl)
        nn['score'] = model1.model.score(td, tl)
        nn['mse'] = model1.model_mse(td, tl)
        nn['r2'] = model1.model_r2_score(td, tl)
        model1_prediction = model1.predict_symbol(prediction_symbol,
                                                  day_diff="year", scaler_filename= "training_test_scaler.scaler")
        nn['prediction'] = model1_prediction[0]
        data['nn_model'] = nn

        gbdt={}
        model2 = GBDTModel()
        model2.trainModel(ts, cl)
        gbdt['mse'] = model2.model_mse(td, tl)
        gbdt['r2'] = model2.model_r2_score(td, tl)
        model2_prediction = model2.predict_symbol(prediction_symbol,
                                                  day_diff="year", scaler_filename= "training_test_scaler.scaler")
        gbdt['prediction'] = model2_prediction[0]
        data['gbdt_model'] = gbdt

        rf={}
        model3 = RandomForestModel()
        model3.trainModel(ts, cl)
        rf['mse'] = model3.model_mse(td, tl)
        rf['r2'] = model3.model_r2_score(td, tl)
        model3_prediction = model3.predict_symbol(prediction_symbol,
                                                  day_diff="year", scaler_filename= "training_test_scaler.scaler")
        rf['prediction'] = model3_prediction[0]
        data['rf_model'] = rf


        dec_tree = {}
        model4 = StockDecisionTree()
        model4.trainModel(ts, cl)
        dec_tree['mse'] = model4.model_mse(td, tl)
        dec_tree['r2'] = model4.model_r2_score(td, tl)
        model4_prediction = model4.predict_symbol(prediction_symbol,
                                                  day_diff="year", scaler_filename= "training_test_scaler.scaler")
        dec_tree['prediction'] = model4_prediction[0]
        data['decision_tree_model'] = dec_tree



        data['final_predicted_year_target'] = (model1_prediction[0] +
                                                   model2_prediction[0] +
                                                   model3_prediction[0] +
                                                   model4_prediction[0])/4

        return json.dumps(data)

