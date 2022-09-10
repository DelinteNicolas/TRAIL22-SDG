from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, overload
from sdg.experiment import Classification


@dataclass
class Classifier(ABC):
    labels: List[str]


    @overload
    def __call__(self, x: str) -> Classification:
        pass

    @overload
    def __call__(self, x: List[str]) -> List[Classification]:
        pass

    def __call__(self, x):
        return self.classify(x)

    @overload
    def classify(self, x: str) -> Classification:
        pass

    @overload
    def classify(self, x: List[str]) -> List[Classification]:
        pass

    @abstractmethod
    def classify(self, x):
        """
        Classify the input(s) and return the corresponding label(s).
        """
