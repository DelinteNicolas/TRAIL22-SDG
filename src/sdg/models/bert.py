from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import sdg
from sdg.experiment import Classification
from .classifier import Classifier


class BertClassifier(Classifier):
    def __init__(self, filename: str=None, device=-1):
        Classifier.__init__(self, sdg.SDGS)
        tk = AutoTokenizer.from_pretrained("bert-base-cased", device=device)
        if filename is None:
            filename = "DelinteNicolas/SDG_classifier_v0.0.1"
        model = AutoModelForSequenceClassification.from_pretrained(filename)
        self._classifier = pipeline("text-classification", model=model, tokenizer=tk, device=device, return_all_scores=True)

    def classify(self, x):
        if isinstance(x, str):
            x = [x]
        scores = []
        for iinput, res in zip(x, self._classifier(x)):
            scores.append(Classification(iinput, [r["score"] for r in res]))
        if len(scores) == 1:
            return scores[0]
        return scores
