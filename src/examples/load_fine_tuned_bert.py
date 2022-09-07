#! /usr/bin/env python3
import sdg
from transformers import pipeline

if __name__ == "__main__":
    model, tokenizer = sdg.load_finetuned_bert()
    ds = sdg.load_sdg_dataset(tokenizer)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0)
    inputs = ds["train"][0]["text"]
    res = classifier(inputs)
    print(inputs, res)
