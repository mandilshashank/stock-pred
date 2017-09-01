from DecisionTreeModel import StockDecisionTree
import numpy as np
import matplotlib.pyplot as plt

from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error


class GBDTModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
                  'learning_rate': 0.01, 'loss': 'ls'}
        clf = ensemble.GradientBoostingRegressor(**params)
        self.model = clf.fit(training_samples, class_labels)


    def predict(self, test_data):
        if self.model != "":
            return self.model.predict(test_data)
        else:
            raise Exception("You must train the model before trying to predict the outcome")

    def model_mse(self, test_data, test_labels):
        if self.model != "":
            return mean_squared_error(test_labels, self.model.predict(test_data))
        else:
            raise Exception("You must train the model before trying to predict the outcome")