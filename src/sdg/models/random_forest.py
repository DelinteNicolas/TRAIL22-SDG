from typing import Callable
import sdg
from sklearn.ensemble import RandomForestClassifier


def random_forest_classifier(tokenizer: Callable[[str], str]) -> RandomForestClassifier:
    train_x, train_y, _, _ = sdg.dataset.load_sdg()
    vectorizer = sdg.utils.get_vectorizer()
    train_x = vectorizer.fit_transform([tokenizer(s) for s in train_x])
    classifier = RandomForestClassifier(n_estimators=100)
    classifier.fit(train_x, train_y)
    return classifier, vectorizer