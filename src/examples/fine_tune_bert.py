#! /usr/bin/env python3
from utils import load_sdg_dataset
from training import fine_tune_bert
from transformers import pipeline

if __name__ == "__main__":
    #################################################
    # Run this example from the 'code directory'    #
    # e.g: python3 examples/fine_tune_bert.py #
    #################################################
    model, tk = fine_tune_bert("saved_models", n_epochs=10)
    ds = load_sdg_dataset(tk)
    classifier = pipeline("text-classification", model=model, tokenizer=tk, device=0)
    inputs = ds["train"][0]["text"]
    res = classifier(inputs)
    print(inputs, res)
