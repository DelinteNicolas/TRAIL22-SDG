from transformers import pipeline
from transformers import AutoTokenizer
from datasets import load_dataset
import pandas as pd

from transformers import AutoModelForSequenceClassification
import numpy as np
from datasets import load_metric
from transformers import TrainingArguments, Trainer

import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

SENTENCE = "I don't think I can afford the gas bill this month."

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
dfs = []
classifiers = []
for i in range(1,18):
    mod = AutoModelForSequenceClassification.from_pretrained("./saved_model_{}".format(i))
    classifier = pipeline("text-classification", model=mod, tokenizer=tokenizer)
    classifiers.append(classifier)


max_score = -1000000
max_ind = None
for i in range(17):
    pred = classifiers[i](SENTENCE)
    y_hat = pred[0]['label']
    score = pred[0]['score']
    if y_hat == "LABEL_0":
        score = -1 * score
    if score > max_score:
        max_score = score
        max_ind = i + 1
print("Sentence: {}".format(SENTENCE))
print("Prediction: {} ({})".format(max_ind, max_score))
