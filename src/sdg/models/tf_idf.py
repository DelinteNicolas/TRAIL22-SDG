from typing import Callable, List
from sklearn.naive_bayes import MultinomialNB
import numpy as np

import sdg
from sdg.experiment import Classification
from .classifier import Classifier


class NaiveBayesClassifier(Classifier):
    def __init__(self, with_prior=True, random_state=None, tokenizer: Callable[[str], str] = None):
        Classifier.__init__(self, sdg.SDGS)
        if tokenizer is None:
            tokenizer = sdg.tokenizers.lemmatize_stem
        self.vectorizer = sdg.utils.get_vectorizer()
        self.clf = MultinomialNB(fit_prior=with_prior)
        self.tokenizer = tokenizer
        train_x, train_y, _, _ = sdg.dataset.load_sdg()
        self.train(train_x, train_y)
    
    def train(self, train_x: List[str], train_y: List[int]):
        train_corpus = [self.tokenizer(s) for s in train_x]
        vectorized_train_x = self.vectorizer.fit_transform(train_corpus)
        self.clf.fit(vectorized_train_x, train_y)

    def classify(self, s):
        if isinstance(s, str):
            s = [s]
        vectorized = self.vectorizer.transform([self.tokenizer(x) for x in s])
        res = []
        for probs, iinput in zip(self.clf.predict_proba(vectorized), s):
            res.append(Classification(iinput, probs))
        if len(res) == 1:
            return res[0]
        return res
