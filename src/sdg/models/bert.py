from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import sdg
from sdg.experiment import Classification
from .classifier import Classifier


class BertClassifier(Classifier):
    def __init__(self, filename: str = "DelinteNicolas/SDG_classifier_v0.0.2", device=-1):
        Classifier.__init__(self, ["Not SDG"] + sdg.SDGS)
        tk = AutoTokenizer.from_pretrained("bert-base-cased", device=device)
        model = AutoModelForSequenceClassification.from_pretrained(filename)
        self._classifier = pipeline("text-classification", model=model, tokenizer=tk, device=device, return_all_scores=True)

    def classify(self, x):
        if isinstance(x, str):
            x = [x]
        classifications = []
        for iinput, res in zip(x, self._classifier(x)):
            # TODO: Dirty trick: Trained with 18 classes while there are actually 17 -> remove the first one
            # Consequence: probabilities do not sum up to one !
            probs = [r["score"] for r in res]
            probs = probs[1:]
            classifications.append(Classification(iinput, probs))
        if len(classifications) == 1:
            return classifications[0]
        return classifications
