from typing import Callable, Tuple
import sdg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB




def tf_idf(tokenizer: Callable[[str], str]) -> Tuple[MultinomialNB, TfidfVectorizer]:
    """Returns the NaiveBayes classifier and the vectorizer"""
    train_x, train_y, _, _ = sdg.dataset.load_sdg()
    train_corpus = [tokenizer(s) for s in train_x]
    vectorizer = sdg.utils.get_vectorizer(train_corpus)
    vectorized_train_x = vectorizer.fit_transform(train_corpus)
    clf = MultinomialNB()
    clf.fit(vectorized_train_x, train_y)
    return clf, vectorizer
