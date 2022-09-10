from typing import Callable, List, Union
from sklearn import ensemble

import sdg
from sdg.experiment import Classification
from .classifier import Classifier


class RandomForestClassifier(Classifier):
    def __init__(self, labels: List[str], tokenizer: Callable[[str], str]=None):
        Classifier.__init__(self, labels)
        if tokenizer is None:
            tokenizer = sdg.tokenizers.lemmatize_stem
        self.tokenizer = tokenizer
        self.vectorizer = sdg.utils.get_vectorizer()
        self.classifier = ensemble.RandomForestClassifier(n_estimators=100)
        train_x, train_y, _, _ = sdg.dataset.load_sdg()
        self.train(train_x, train_y)
        

    def train(self, train_x, train_y):
        train_x = self.vectorizer.fit_transform([self.tokenizer(s) for s in train_x])
        self.classifier.fit(train_x, train_y)

    def classify(self, s):
        if isinstance(s, str):
            s = [s]
        tokenized = [self.tokenizer(item) for item in s]
        vectorized = self.vectorizer.transform(tokenized)
        results = []
        for iinput, probs in zip(s, self.classifier.predict_proba(vectorized)):
            results.append(Classification(iinput, probs))
        
        if len(results) == 1:
            return results[0]
        return results
    