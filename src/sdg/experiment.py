from dataclasses import dataclass
from typing import Callable, List
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.metrics import ConfusionMatrixDisplay, precision_score, recall_score


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
    def sdg(self) -> int:
        """The SDG corresponding to the label"""
        sdg = self.label
        if self.n_classes == 17:
            sdg += 1
        return sdg

    @property
    def n_classes(self) -> int:
        """The number of classes"""
        return len(self.class_predictions)

    def top_n_labels(self, n: int) -> List[int]:
        """Retrieve the top n labels (unordered)"""
        return np.argpartition(self.class_predictions, -n)[-n:]

    def __repr__(self):
        return f"SDG {self.sdg} ({self.class_predictions[self.label] * 100:.2f}%)"
            

@dataclass
class Experiment:
    results: List[Classification]
    ground_truths: List[int]
    clf: Callable[[str], List[float]]

    def __init__(self, classifier: Callable[[str], List[float]]) -> None:
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

    def precision(self) -> float:
        return 0.

    def recall(self) -> float:
        return 0.

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
            pickle.dump(self.results, f)

    def summary(self, directory: str):
        if not directory.startswith("summary/"):
            directory = os.path.join("summary", directory)
            os.makedirs(directory, exist_ok=True)
        
        self.confusion_matrix(os.path.join(directory,"confusion_matrix.png"))
        with open(os.path.join(directory, "summary.md"), "w", encoding="utf8") as f:
            f.write(f"# Experience summary for {self.clf.__class__}\n")
            f.write(f"## Confusion matrix\n")
            f.write(f"![confusion matrix](confusion_matrix.png)\n")
            f.write(f"## Metrics\n")
            f.write(f"- Accuracy {self.topn_accuracy(1) * 100:.3f}%\n")
            f.write(f"- Precision {precision_score(self.ground_truths, self.predictions, average='weighted') * 100:.3f}%\n")
            f.write(f"- Recall {recall_score(self.ground_truths, self.predictions, average='macro') * 100:.3f}%\n")
        self.save(f"{directory}/results.pkl")


    @property
    def predictions(self) -> List[int]:
        return [r.label for r in self.results]

    @staticmethod
    def load(name: str) -> "Experiment":
        with open(name, "rb") as f:
            results = pickle.load(f)
        exp = Experiment(lambda *_: print("Mock classifier!"))
        exp.results = results
        return exp

    def __len__(self):
        return len(self.results)