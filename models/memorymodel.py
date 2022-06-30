from sklearn.ensemble import RandomForestClassifier

class MemoryModel:
    def __init__(self, pos, neg):
        # Create model
        self.clf = RandomForestClassifier(n_estimators=100)
        # Preprocessing
        dataset = {}
        for state in neg:
            dataset[state] = 0
        for state in pos:
            dataset[state] = 1
        X = []
        Y = []
        for k, v in dataset.items():
            X.append(k)
            Y.append(v)
        # Training
        self.clf = self.clf.fit(X, Y)
    
    def test(self, state):
        return self.clf.predict([state])[0] == 1