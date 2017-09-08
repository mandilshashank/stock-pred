from DecisionTreeModel import StockDecisionTree
from NeuralNetworkModel import NeuralNetworkModel
from RandomForestModel import RandomForestModel
from GBDTModel import GBDTModel
from src.NasdaqDataCollector.DataBuilder import DataBuilder

if __name__ == "__main__":
    prediction_symbol = "STX"

    dc = DataBuilder()
    [ts, cl, td, tl, tss] = dc.get_training_and_test_data(prediction_symbol)

    model1 = NeuralNetworkModel()
    model1.trainModel(ts, cl)
    print "Model 1 MSE : " + str(model1.model_mse(td,tl))
    model1_prediction = model1.predict_symbol(prediction_symbol)
    print "Model 1 : " + str(model1_prediction[0])

    model2 = GBDTModel()
    model2.trainModel(ts, cl)
    print "Model 2 MSE : " + str(model2.model_mse(td,tl))
    model2_prediction = model2.predict_symbol(prediction_symbol)
    print "Model 2 : " + str(model2_prediction[0])

    model3 = RandomForestModel()
    model3.trainModel(ts, cl)
    print "Model 3 MSE : " + str(model3.model_mse(td,tl))
    model3_prediction = model3.predict_symbol(prediction_symbol)
    print "Model 3 : " + str(model3_prediction[0])

    model4 = StockDecisionTree()
    model4.trainModel(ts, cl)
    print "Model 4 MSE : " + str(model4.model_mse(td,tl))
    model4_prediction = model4.predict_symbol(prediction_symbol)
    print "Model 4 : " + str(model4_prediction[0])


    print "Predicted test label values"
    print (model1_prediction[0] + model2_prediction[0] + model3_prediction[0] + model4_prediction[0])/4

    #print dtm.model.feature_importances_
    #print dtm.model.feature_importances_
    # print dtm.model.max_features_
    # print dtm.model.n_features_
    # print dtm.model.n_outputs_
    #
    # tree.export_graphviz(dtm.model,out_file='tree.dot')

    #print dtm.model.decision_path(td)





