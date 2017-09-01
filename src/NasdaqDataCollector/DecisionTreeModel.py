from sklearn import tree


class StockDecisionTree:
    def __init__(self):
        self.model = ""

    def trainModel(self, training_samples, class_labels):
        clf = tree.DecisionTreeRegressor()
        self.model = clf.fit(training_samples, class_labels)

    def predict(self, test_data):
        return self.model.predict(test_data)