from typing import Callable, Tuple, List, Union
from sdg.constants import SDG_DICT
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from .classifier import Classifier
from sdg.experiment import Classification

    
class ZeroShotClassifier(Classifier):
    def __init__(self, labels: List[str], model_name: str="facebook/bart-large-mnli", multi_label=False, device: int=-1):
        Classifier.__init__(self, labels)
        self.label_indices = {label: i for i, label in enumerate(labels)}
        tk = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline("zero-shot-classification", model=model, tokenizer=tk, multi_label=multi_label, device=device)

    def classify(self, s):
        if isinstance(s, str):
            s = [s]
        classifications = []
        for iinput, res in zip(s, self.classifier(s, self.labels)):
            scores = [None] * len(self.labels)
            for label, score in zip(res["labels"], res["scores"]):
                label_index = self.label_indices[label]
                scores[label_index] = score
            classifications.append(Classification(iinput, scores))
        if len(classifications) == 1:
            return classifications[0]
        return classifications