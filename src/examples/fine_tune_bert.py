#! /usr/bin/env python3
import sdg
from transformers import pipeline

if __name__ == "__main__":
    model, tk = sdg.fine_tune_bert("saved_models", n_epochs=1)
    _, _, testx, testy = sdg.dataset.load_sdg_dataframe()
    classifier = pipeline("text-classification", model=model, tokenizer=tk, device=0)
    inputs = testx[0]
    res = classifier(inputs)
    print(inputs, res)