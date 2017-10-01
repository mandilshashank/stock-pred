import datetime
import mysql.connector
from sklearn import tree
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pickle
import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from NasdaqDataCollector.DataBuilder import DataBuilder


class StockDecisionTree:
    def __init__(self):
        self.model = ""

    def trainModel(self, training_samples, class_labels):
        clf = tree.DecisionTreeRegressor()
        self.model = clf.fit(training_samples, class_labels)

    def predict(self, test_data):
        if self.model != "":
            return self.model.predict(test_data)
        else:
            raise Exception("You must train the model before trying to predict the outcome")

    def predict_symbol(self, symbol, start_date=datetime.date(2017,8,30), day_diff=7):
        db = DataBuilder()
        test_data = db.get_symbol_data(start_date, symbol, day_diff)
        return self.model.predict(test_data)

    def model_mse(self, test_data, test_labels):
        if self.model != "":
            return mean_squared_error(test_labels, self.model.predict(test_data))
        else:
            raise Exception("You must train the model before trying to predict the outcome")

    def model_r2_score(self, test_data, test_labels):
        if self.model != "":
            return r2_score(test_labels, self.model.predict(test_data))
        else:
            raise Exception("You must train the model before trying to predict the outcome")

    def save_model(self, filename="decision_tree.model", train_range=7):
        script_dir = os.path.dirname(__file__)
        rel_path = "../models/"+str(train_range)+filename
        abs_file_path = os.path.join(script_dir, rel_path)
        if self.model != "":
            return pickle.dump(self.model, open(abs_file_path, 'wb'))
        else:
            raise Exception("You must train the model before trying to save it")

    def load_model(self, filename="decision_tree.model", train_range=7):
        script_dir = os.path.dirname(__file__)
        rel_path = "../models/"+str(train_range)+filename
        abs_file_path = os.path.join(script_dir, rel_path)
        self.model = pickle.load(open(abs_file_path, 'rb'))