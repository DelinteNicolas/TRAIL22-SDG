import os
import numpy as np
from sdg.experiment import Classification
from sdg import SDGS
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from .classifier import Classifier



class Binary17Classifier(Classifier):
    """
    Combination of 17 different binary classifiers.
    The result of the classification depends on the threshold:
        - If any of the classifiers has a cond=fidence >= threshold, then the sentence is classified as such
        - Otherwise, the result is classified as "Not an SDG"
    """
    def __init__(self, threshold: float=0.7, device: int=-1):
        labels = ["Not an SDG"] + SDGS
        Classifier.__init__(self, labels)
        self.threshold = threshold
        self.models = []
        tk = AutoTokenizer.from_pretrained("bert-base-uncased", device=device)
        for i in range(17):
            model = AutoModelForSequenceClassification.from_pretrained(os.path.join("binary17", f"model_sdg_{i}"))
            self.models.append(pipeline("text-classification", model=model, tokenizer=tk, device=device, return_all_scores=True))
        

    def classify(self, x):
        if isinstance(x, str):
            x = [x]
        scores = np.empty((len(x), self.n_classes), dtype=np.float32)
        for j, clf in enumerate(self.models):
            scores[0][j] = 0
            for i, res in enumerate(clf(x)):
                scores[i][j+1] = res["score"][1]
        
        classifications = []
        for iinput, score in zip(x, scores):
            argmax = np.argmax(score)
            probs = np.zeros(self.n_classes, dtype=np.float32)
            if score[argmax] >= self.threshold:
                probs[argmax] = 1.
            else:
                probs[0] = 1.
            classifications.append(Classification(iinput, probs))

        if len(classifications) == 1:
            return classifications[0]
        return classifications
