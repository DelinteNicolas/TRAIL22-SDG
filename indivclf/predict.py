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

df = pd.read_csv("./../data/Test_data.csv".format(i))
y_true = []
y_preds = []
for _, r in df.iterrows():
    max_score = -1000000
    max_ind = 0
    for i in range(17):
        pred = classifiers[i](r['text'])
        y_hat = pred[0]['label']
        score = pred[0]['score']
        if y_hat == "LABEL_0":
            score = -1 * score
        if score > max_score:
            max_score = score
            max_ind = i + 1
    y_true.append(r['SDG'])
    y_preds.append(max_ind)


cf_matrix = confusion_matrix(y_true, y_preds)
import seaborn as sns

ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

ax.set_title('Confusion Matrix\n\n'.format(i));
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values ');

## Ticket labels - List must be in alphabetical order
ax.xaxis.set_ticklabels(range(1,18))
ax.yaxis.set_ticklabels(range(1,18))

## Display the visualization of the Confusion Matrix.
plt.savefig("Confmatri.png".format(i))
plt.clf()
