from typing import Tuple
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, PreTrainedTokenizer


def load_finetuned_bert(filename=None) -> Tuple[torch.nn.Module, PreTrainedTokenizer]:
    tk = AutoTokenizer.from_pretrained("bert-base-cased")
    if filename is None:
        filename = "DelinteNicolas/SDG_classifier_v0.0.1"
    model = AutoModelForSequenceClassification.from_pretrained(filename)
    return model, tk
