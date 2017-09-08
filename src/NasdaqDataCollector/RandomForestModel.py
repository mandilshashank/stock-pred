from DecisionTreeModel import StockDecisionTree
from sklearn.ensemble import RandomForestRegressor


class RandomForestModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2}
        clf = RandomForestRegressor(**params)
        self.model = clf.fit(training_samples, class_labels)

    def save_model(self, filename="rf.model"):
        StockDecisionTree.save_model(self, filename)

    def load_model(self, filename="rf.model"):
        StockDecisionTree.load_model(self, filename)