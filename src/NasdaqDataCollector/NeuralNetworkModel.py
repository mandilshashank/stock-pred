from DecisionTreeModel import StockDecisionTree
from sklearn.neural_network import MLPRegressor


class NeuralNetworkModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        clf = MLPRegressor(max_iter=100000)
        self.model = clf.fit(training_samples, class_labels)

    def save_model(self, filename="nn.model"):
        StockDecisionTree.save_model(self, filename)

    def load_model(self, filename="nn.model"):
        StockDecisionTree.load_model(self, filename)