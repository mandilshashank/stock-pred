from DecisionTreeModel import StockDecisionTree
from sklearn.neural_network import MLPRegressor


class NeuralNetworkModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        clf = MLPRegressor()
        self.model = clf.fit(training_samples, class_labels)