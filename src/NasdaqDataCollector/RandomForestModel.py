from src.NasdaqDataCollector.DecisionTreeModel import StockDecisionTree
from sklearn.ensemble import RandomForestRegressor


class RandomForestModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2}
        clf = RandomForestRegressor(**params)
        self.model = clf.fit(training_samples, class_labels)

    def save_model(self, filename="rf.model", train_range=7):
        StockDecisionTree.save_model(self, filename, train_range)

    def load_model(self, filename="rf.model", train_range=7):
        StockDecisionTree.load_model(self, filename, train_range)