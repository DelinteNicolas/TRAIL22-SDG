#! /usr/bin/env python3
import sdg
from transformers import pipeline


if __name__ == "__main__":
    trainx, trainy, testx, testy = sdg.dataset.load_sdg()
    model, tk = sdg.models.load_finetuned_bert()
    classifier = pipeline("text-classification", model=model, tokenizer=tk)

    res = classifier(testx[0])
    print(testx[0], res)
