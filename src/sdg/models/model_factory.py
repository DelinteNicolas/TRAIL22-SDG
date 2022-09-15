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
    "Fine tuned BERT v0.0.5",
    "Random Forest",
    "Naive Bayes (TF/IDF)",
    "Naive Bayes without pior (TF/IDF)"
]

@lru_cache()
def get_model(model_name: str) -> Classifier:
    if model_name not in MODEL_NAMES:
        return None
    if model_name in MODEL_NAMES[0:5]:
        version = model_name.split()[-1]
        filename = f"DelinteNicolas/SDG_classifier_{version}"
        return BertClassifier(filename)
    if model_name == MODEL_NAMES[5]:
        return RandomForestClassifier()
    if model_name == MODEL_NAMES[6]:
        return NaiveBayesClassifier()
    if model_name == MODEL_NAMES[7]:
        return NaiveBayesClassifier(with_prior=False)
    raise ValueError("Should never arrive here !")
