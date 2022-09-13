from functools import lru_cache

from .classifier import Classifier
from .bert import BertClassifier
from .random_forest import RandomForestClassifier
from .tf_idf import NaiveBayesClassifier


MODEL_NAMES = [
    "Fine tuned BERT v0.0.1",
    "Fine tuned BERT v0.0.2",
    "Fine tuned BERT v0.0.3",
    "Fine tuned BERT v0.0.4",
    "Random Forest",
    "Naive Bayes (TF/IDF)"
]

@lru_cache()
def get_model(model_name: str) -> Classifier:
    if model_name not in MODEL_NAMES:
        return None
    if model_name in MODEL_NAMES[0:4]:
        version = model_name.split()[-1]
        filename = f"DelinteNicolas/SDG_classifier_{version}"
        return BertClassifier(filename)
    if model_name == MODEL_NAMES[4]:
        return RandomForestClassifier()
    if model_name == MODEL_NAMES[5]:
        return NaiveBayesClassifier()
    raise ValueError("Should never arrive here !")
