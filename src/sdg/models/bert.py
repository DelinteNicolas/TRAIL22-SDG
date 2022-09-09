from typing import List, Tuple
import torch
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer, PreTrainedTokenizer

from .classifier import Classifier

def load_finetuned_bert(filename=None) -> Tuple[torch.nn.Module, PreTrainedTokenizer]:
    tk = AutoTokenizer.from_pretrained("bert-base-cased")
    if filename is None:
        filename = "DelinteNicolas/SDG_classifier_v0.0.1"
    model = AutoModelForSequenceClassification.from_pretrained(filename)
    return model, tk


class BertClassifier(Classifier):
    def __init__(self, labels: List[str], filename: str=None, device=-1):
        Classifier.__init__(self, labels)
        tk = AutoTokenizer.from_pretrained("bert-base-cased")
        if filename is None:
            filename = "DelinteNicolas/SDG_classifier_v0.0.1"
        model = AutoModelForSequenceClassification.from_pretrained(filename)
        self._classifier = pipeline("text-classification", model=model, tokenizer=tk, device=device)

    def classify(self, x):
        if isinstance(x, str):
            x = [x]
        res = self._classifier(x)
        if len(res) == 1:
            return res[0]
        return res
