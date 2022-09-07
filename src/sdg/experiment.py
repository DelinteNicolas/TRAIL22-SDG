from dataclasses import dataclass
from typing import List
import pickle
from tqdm import tqdm
import pandas as pd

@dataclass
class Classification:
    input_data: str
    """The classifier input"""
    class_prediction: List[float]
    """The probability for every class"""
    class_names: List[str]
    """The name of every class"""
    ground_truth: int
    """The actual label of the data"""
    

@dataclass
class Experiment:
    results: List[Classification]
    ground_truth: List[int]

    def __init__(self) -> None:
        self.results = []
        self.ground_truth = []

    def add_results(self, results: List[Classification], ground_truth: List[int]):
        assert len(results) == len(ground_truth)
        self.results += results
        self.ground_truth += ground_truth

    def topn_accuracy(self, n: int) -> float:
        assert n > 0
        n_correct = 0
        for r, ground_truth in zip(self.results, self.ground_truth):
            if ground_truth in r.labels[:n]:
                n_correct += 1
        return n_correct / len(self.results)

    def confusion_matrix(self):
        pass

    def save(self, name: str):
        with open(name, "wb") as f:
            pickle.dump(self, f)