from dataclasses import dataclass
from typing import Callable, List
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.metrics import ConfusionMatrixDisplay

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
        """The confidence of the prediction"""
        return self.class_predictions[self.label]

    def top_n_labels(self, n: int) -> List[int]:
        """Retrieve the top n labels (unordered)"""
        return np.argpartition(self.class_predictions, -n)[-n:]

    def __repr__(self):
        l = self.label
        return f"{l} ({self.class_predictions[l] * 100:.2f}%)"
            

@dataclass
class Experiment:
    results: List[Classification]
    clf: Callable[[str], List[float]]

    def __init__(self, classifier: Callable[[str], List[float]]) -> None:
        self.results = []
        self.clf = classifier

    def run(self, dataset: List[str], labels: List[int], batch_size: int=1):
        """Run the classification on the given dataset"""
        assert len(dataset) == len(labels)
        for i in tqdm(range(0, len(dataset), batch_size)):
            sentences, ground_truths = dataset[i: i+batch_size], labels[i: i+batch_size]
            probabilities = self.clf(sentences)
            for sentence, proba, ground_truth in zip(sentences, probabilities, ground_truths):
                self.results.append(Classification(sentence, proba, ground_truth))
        
    def topn_accuracy(self, n: int) -> float:
        """Return the top-n accuracy of the experiment"""
        assert n > 0
        n_correct = 0
        for r in self.results:
            if r.ground_truth in r.top_n_labels(n):
                n_correct += 1
        return n_correct / len(self.results)

    def precision(self) -> float:
        pass

    def recall(self) -> float:
        pass

    def confusion_matrix(self, n_classes: int, filename: str):
        fig, ax = plt.subplots(figsize=(10, 5))
        ConfusionMatrixDisplay.from_predictions(self.ground_truths, self.predictions, ax=ax)
        #ax.xaxis.set_ticklabels(np.arange(1, n_classes + 1))
        #ax.yaxis.set_ticklabels(np.arange(1, n_classes + 1))
        
        _ = ax.set_title(
            f"Confusion Matrix for Naive Bayes"
        )
        if not filename.endswith(".png"):
            filename += ".png"
        plt.savefig(filename)

    def save(self, name: str):
        """Save the experiment results in a pickle file"""
        with open(name, "wb") as f:
            pickle.dump(self.results, f)

    def summary(self, directory: str, n_classes: int):
        if not directory.endswith(".md"):
            directory += ".md"
        if not directory.startswith("summary/"):
            directory = os.path.join("summary", directory)
            os.makedirs(directory)
        
        self.confusion_matrix(n_classes, f"{directory}/confusion_matrix.png")
        file = f"{directory}/summary"
        with open(file, "w", encoding="utf8") as f:
            f.write(f"# Experience summary for {self.clf.__name__}\n")
            f.write(f"## Confusion matrix\n")
            f.write(f"![confusion matrix]({directory})\n")
            f.write(f"## Metrics\n")
            f.write(f"- Accuracy {self.topn_accuracy(1) * 100}%")
            f.write(f"- Precision {self.precision() * 100}%")
            f.write(f"- Recall {self.recall() * 100}%")
        self.save(f"{directory}/results.pkl")


    @property
    def ground_truths(self) -> List[int]:
        return [r.ground_truth for r in self.results]

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