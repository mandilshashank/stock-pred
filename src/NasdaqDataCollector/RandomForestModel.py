from DecisionTreeModel import StockDecisionTree
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


class RandomForestModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2}
        clf = RandomForestRegressor(**params)
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