from DecisionTreeModel import StockDecisionTree
from sklearn import ensemble


class GBDTModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        params = {'n_estimators': 1000, 'max_depth': 4, 'min_samples_split': 10,
                  'learning_rate': 0.01, 'loss': 'ls'}
        clf = ensemble.GradientBoostingRegressor(**params)
        self.model = clf.fit(training_samples, class_labels)

    def save_model(self, filename="gbdt.model"):
        StockDecisionTree.save_model(self, filename)

    def load_model(self, filename="gbdt.model"):
        StockDecisionTree.load_model(self, filename)
