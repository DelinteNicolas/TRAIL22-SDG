from typing import Callable, List
import sdg
from sklearn.ensemble import RandomForestClassifier


def random_forest_classifier(tokenizer: Callable[[str], str]) -> Callable[[str], List[float]]:
    train_x, train_y, _, _ = sdg.dataset.load_sdg()
    vectorizer = sdg.utils.get_vectorizer()
    train_x = vectorizer.fit_transform([tokenizer(s) for s in train_x])
    classifier = RandomForestClassifier(n_estimators=100)
    classifier.fit(train_x, train_y)

    def classify(s: str):
        s = tokenizer(s)
        v = vectorizer.transform(s)
        return classifier.predict_proba(v)

    return classify