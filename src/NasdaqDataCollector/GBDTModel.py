from src.NasdaqDataCollector.DecisionTreeModel import StockDecisionTree
from sklearn import ensemble


class GBDTModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        params = {'n_estimators': 1000, 'max_depth': 4, 'min_samples_split': 10,
                  'learning_rate': 0.01, 'loss': 'ls'}
        clf = ensemble.GradientBoostingRegressor(**params)
        self.model = clf.fit(training_samples, class_labels)

    def save_model(self, filename="gbdt.model", train_range=7):
        StockDecisionTree.save_model(self, filename, train_range)

    def load_model(self, filename="gbdt.model", train_range=7):
        StockDecisionTree.load_model(self, filename, train_range)
