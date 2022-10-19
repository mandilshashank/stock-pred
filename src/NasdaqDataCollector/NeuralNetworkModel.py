from src.NasdaqDataCollector.DecisionTreeModel import StockDecisionTree
from sklearn.neural_network import MLPRegressor


class NeuralNetworkModel(StockDecisionTree):
    def __init__(self):
        StockDecisionTree.__init__(self)

    def trainModel(self, training_samples, class_labels):
        clf = MLPRegressor(max_iter=10000000, solver='sgd', momentum=0.1, early_stopping=True)
        self.model = clf.fit(training_samples, class_labels)

    def save_model(self, filename="nn.model", train_range=7):
        StockDecisionTree.save_model(self, filename, train_range)

    def load_model(self, filename="nn.model", train_range=7):
        StockDecisionTree.load_model(self, filename, train_range)