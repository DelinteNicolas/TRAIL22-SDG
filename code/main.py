#! /usr/bin/env python3
from utils import load_sdg_dataset
from models import load_finetuned_bert
from transformers import pipeline

if __name__ == "__main__":
    model, tokenizer = load_finetuned_bert()
    ds = load_sdg_dataset(tokenizer)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    inputs = ds["train"][0]["text"]
    res = classifier(inputs)
    print(inputs, res)
