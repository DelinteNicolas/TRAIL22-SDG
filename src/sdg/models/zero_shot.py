from typing import Callable, Tuple, List
from sdg.constants import SDG_DICT
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


def zero_shot_classifier(model_name: str=None, multi_label=False, device=-1) -> Callable[[str], List[Tuple[float, str]]]:
    if model_name is None:
        model_name = "facebook/bart-large-mnli"
    tk = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    classifier = pipeline("zero-shot-classification", model=model, tokenizer=tk, multi_label=multi_label, device=device)
    labels = [SDG_DICT[i] for i in range(len(SDG_DICT))]
    inverse_labels = {value: key for key, value in SDG_DICT.items()}

    def classify(s: str):
        res = classifier(s, labels)
        scores_labels = [None] * len(SDG_DICT)
        for label, score in zip(res["labels"], res["scores"]):
            label_index = inverse_labels[label]
            scores_labels[label_index] = score, label
        return scores_labels
    
    return classify
    
