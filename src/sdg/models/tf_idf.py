from typing import Callable, Tuple, Union, List
import sdg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from .classifier import Classifier
from sdg.experiment import Classification


def tf_idf_classifier(tokenizer: Callable[[str], str]=None) -> Tuple[MultinomialNB, TfidfVectorizer]:
    """Returns the NaiveBayes classifier and the vectorizer"""
    if tokenizer is None:
        tokenizer = sdg.tokenizers.lemmatize_stem
    train_x, train_y, _, _ = sdg.dataset.load_sdg()
    train_corpus = [tokenizer(s) for s in train_x]
    vectorizer = sdg.utils.get_vectorizer()
    vectorized_train_x = vectorizer.fit_transform(train_corpus)
    clf = MultinomialNB()
    clf.fit(vectorized_train_x, train_y)

    def classify(s: Union[str, List[str]]):
        if isinstance(s, str):
            s = [s]
        s = vectorizer.transform([tokenizer(x) for x in s])
        return clf.predict_proba(s)

    return classify



class NaiveBayesClassifier(Classifier):
    def __init__(self, labels: List[str], tokenizer: Callable[[str], str]=None):
        Classifier.__init__(self, labels)
        if tokenizer is None:
            tokenizer = sdg.tokenizers.lemmatize_stem
        self.vectorizer = sdg.utils.get_vectorizer()
        self.clf = MultinomialNB()
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
