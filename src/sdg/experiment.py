from dataclasses import dataclass
from typing import List, Any
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.metrics import ConfusionMatrixDisplay, precision_score, recall_score, f1_score


@dataclass
class Classification:
    """This structure represents a classification result"""
    input_data: str
    """The classifier input"""
    class_predictions: List[float]
    """The probability for every class"""

    @property
    def label(self) -> int:
        """The predicted label"""
        return np.argmax(self.class_predictions)

    @property
    def confidence(self) -> float:
        """The considence score of the label"""
        return self.class_predictions[self.label]

    def assigned_sdgs(self, max_labels=2) -> List[int]:
        """
        The smallest set of SDGs for which the sum of predictions is greater than or equal to the sum of predictions of the other SDGs.
        Return an empty list the length exceeds max_labels.
        """
        for n in range(1, max_labels+1):
            assigned = self.top_n_labels(n)
            unassigned = [i for i in range(len(self.class_predictions)) if i not in assigned]
            assigned_predictions = [self.class_predictions[i] for i in assigned]
            unassigned_predictions = [self.class_predictions[i] for i in unassigned]
            if sum(assigned_predictions) >= sum(unassigned_predictions):
                return [self.__to_sdg(i) for i in assigned]
        return []

    @property
    def confidence(self) -> float:
        """The confidence of the prediction"""
        return self.class_predictions[self.label]

    def __to_sdg(self, label: int) -> int:
        if self.n_classes == 17:
            return label + 1
        return label

    @property
    def sdg(self) -> int:
        """The SDG corresponding to the label"""
        return self.__to_sdg(self.label)

    @property
    def n_classes(self) -> int:
        """The number of classes"""
        return len(self.class_predictions)

    def top_n_labels(self, n: int) -> List[int]:
        """Retrieve the top n labels (unordered)"""
        return list(np.argpartition(self.class_predictions, -n)[-n:])

    def __repr__(self):
        return f"SDG {self.sdg} -- Label {self.label}  ({self.class_predictions[self.label] * 100:.2f}%)"
            
    def to_json(self):
        return {
            "inputData": self.input_data,
            "classPredictions": list(self.class_predictions),
            "confidence": self.confidence,
            "label": int(self.label),
            "sdg": int(self.sdg)
        }
        

@dataclass
class Experiment:
    results: List[Classification]
    ground_truths: List[int]
    clf: Any

    def __init__(self, classifier) -> None:
        self.results = []
        self.clf = classifier
        self.ground_truths = []

    def run(self, dataset: List[str], labels: List[int], batch_size: int=1):
        """Run the classification on the given dataset"""
        assert len(dataset) == len(labels)
        self.ground_truths = labels
        for i in tqdm(range(0, len(dataset), batch_size)):
            res = self.clf(dataset[i: i+batch_size])
            if batch_size == 1:
                res = [res]
            self.results += res
        
    def topn_accuracy(self, n: int) -> float:
        """Return the top-n accuracy of the experiment"""
        assert n > 0
        n_correct = 0
        for r, ground_truth in zip(self.results, self.ground_truths):
            if ground_truth in r.top_n_labels(n):
                n_correct += 1
        return n_correct / len(self.results)

    def confusion_matrix(self, filename: str):
        fig, ax = plt.subplots(figsize=(10, 5))
        ConfusionMatrixDisplay.from_predictions(self.ground_truths, self.predictions, ax=ax)
        #ax.xaxis.set_ticklabels(np.arange(1, n_classes + 1))
        #ax.yaxis.set_ticklabels(np.arange(1, n_classes + 1))
        if not filename.endswith(".png"):
            filename += ".png"
        plt.savefig(filename)

    def save(self, name: str):
        """Save the experiment results in a pickle file"""
        with open(name, "wb") as f:
            pickle.dump([self.results, self.ground_truths, self.clf.labels], f)

    def misclassification_summary(self, filename: str, threshold: float=0.7):
        with open(filename, "w", encoding="utf8") as file:
            file.write(f"# Wrongly classified lines with confidence >= {threshold}\n")
            for res, label in zip(self.results, self.ground_truths):
                if res.label != label and res.confidence >= threshold:
                    file.write(f"### {res.input_data}\n")
                    file.write(f"- Prediction {res.label} (SDG {res.sdg})\n")
                    file.write(f"- Ground truth {label} (SDG {label + 1})\n")
                    file.write(f"- Confidence {res.confidence*100:.3f}\n")

    def summary(self, directory: str):
        if not directory.startswith("summary/"):
            directory = os.path.join("summary", directory)
            os.makedirs(directory, exist_ok=True)
        
        self.confusion_matrix(os.path.join(directory,"confusion_matrix.png"))
        with open(os.path.join(directory, "summary.md"), "w", encoding="utf8") as f:
            f.write(f"# Experience summary for {self.clf.__class__.__name__}\n")
            f.write(f"## Labels \n")
            for i, label in enumerate(self.clf.labels):
                f.write(f"{i}. {label}\n")    
            f.write(f"## Confusion matrix\n")
            f.write(f"![confusion matrix](confusion_matrix.png)\n")
            f.write(f"## Metrics\n")
            f.write(f"- Accuracy {self.topn_accuracy(1) * 100:.3f}%\n")
            f.write(f"- Precision {precision_score(self.ground_truths, self.predictions, average='weighted') * 100:.3f}%\n")
            f.write(f"- Recall {recall_score(self.ground_truths, self.predictions, average='macro') * 100:.3f}%\n")
            f.write(f"- F1 {f1_score(self.ground_truths, self.predictions) * 100:.3f}\n")
        self.save(f"{directory}/results.pkl")


    @property
    def predictions(self) -> List[int]:
        return [r.label for r in self.results]

    @staticmethod
    def load(file_name: str) -> "Experiment":
        with open(file_name, "rb") as f:
            results, ground_truths, labels = pickle.load(f)
        def clf(_):
            pass
        clf.labels = labels
        exp = Experiment(clf)
        exp.results = results
        exp.ground_truths = ground_truths
        return exp

    def __len__(self):
        return len(self.results)