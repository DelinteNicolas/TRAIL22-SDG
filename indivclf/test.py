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
    df = pd.read_csv("test_{}.csv".format(i))
    dfs.append(df)

    mod = AutoModelForSequenceClassification.from_pretrained("./saved_model_{}".format(i))
    classifier = pipeline("text-classification", model=mod, tokenizer=tokenizer)
    classifiers.append(classifier)

    y_true = []
    y_preds = []
    for _, r in df.iterrows():
        y_hat = classifier(r['text'])
        y = r['SDG']
        if y_hat[0]['label'] == "LABEL_0":
            y_hat = 0
        else:
            y_hat = 1
        y_true.append(y)
        y_preds.append(y_hat)

    cf_matrix = confusion_matrix(y_true, y_preds)
    import seaborn as sns

    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

    ax.set_title('Confusion Matrix {}\n\n'.format(i));
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ');

    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(['False','True'])
    ax.yaxis.set_ticklabels(['False','True'])

    ## Display the visualization of the Confusion Matrix.
    plt.savefig("{}.png".format(i))
    plt.clf()
