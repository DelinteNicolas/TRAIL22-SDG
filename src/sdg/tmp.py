from dataclasses import dataclass
from typing import Any, Dict, List
import transformers as tfs
import pandas as pd
import pickle
from datasets import load_dataset
from constants import SDGS


@dataclass
class Result:
    MAX_SENTENCE_LEN = 50
    sentence: str
    confidence_scores: List[float]
    labels: List[int]

    # def __repr__(self) -> str:
    #     s = self.sentence
    #     if len(s) > Result.MAX_SENTENCE_LEN:
    #         s = self.sentence[:Result.MAX_SENTENCE_LEN - 3] + "..."
    #     return f"{s:{Result.MAX_SENTENCE_LEN}s}\t SDG-{self.sdg_num:2d}\t[{self.confidence_scores[0]:.4f}]"

    @staticmethod
    def from_dict(result: Dict[str, Any]) -> "Result":
        return Result(
            sentence=result["sequence"],
            confidence_scores=result["scores"],
            labels=[SDGS.index(label) + 1 for label in result["labels"]]
        )


@dataclass
class Experiment:
    results: List[Result]
    ground_truth: List[int]

    def __init__(self) -> None:
        self.results = []
        self.ground_truth = []

    def add_results(self, results: List[Result], ground_truth: List[int]):
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


def pad(tokens_lists: List[List[int]], pad_value: int):
    max_len = max(len(tokens) for tokens in tokens_lists)
    res_tokens, res_attention = [], []
    for tokens in tokens_lists:
        l = len(tokens)
        pad_len = max_len - l
        pad = [pad_value] * pad_len
        res_attention.append([1] * l + [0] * pad_len)
        res_tokens.append(tokens + pad)
    return res_tokens, res_attention

# TODO: confusion matrix

def run_experiment(name: str):
    batch_size = 128
    df = pd.read_csv("data/Test_data.csv")
    classifier = tfs.pipeline("zero-shot-classification", model="DelinteNicolas/SDG_classifier_v0.0.1", device=0, padding=True, truncation=True)
    exp = Experiment()
    for i in range(0, len(df), batch_size):
        print(f"\r{100*i/len(df):.2f}%...")
        inputs = list(df["text"][i:i+batch_size])
        ground_truth = list(df["SDG"][i:i+batch_size])
        results = classifier(
            inputs,
            candidate_labels=SDGS
        )
        exp.add_results([Result.from_dict(d) for d in results], ground_truth)
    
    with open(f"{name}.pkl", "wb") as f:
        pickle.dump(exp, f)
    return exp
    