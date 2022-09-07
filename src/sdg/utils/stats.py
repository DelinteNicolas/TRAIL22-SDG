import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score#, auc, roc_curve
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def eval_classifier(n_classes, labels, label_predictions, probabilities_predictions ):
    acc = accuracy_score(labels, label_predictions)
    print('accuracy :',100*acc.round(3))

    precision = precision_score(labels, label_predictions, average='weighted')#micro, macro, weighted
    print('precision:',100*precision.round(3))

    recall = recall_score(labels, label_predictions, average='macro')#micro, macro, weighted
    print('recall   :',100*recall.round(3))

    roc_auc = roc_auc_score(labels, probabilities_predictions, multi_class='ovo') #'raise', 'ovr', 'ovo'
    print('roc_auc  :',100*roc_auc.round(3))

    fig, ax = plt.subplots(figsize=(10, 5))
    ConfusionMatrixDisplay.from_predictions(labels, label_predictions, ax=ax)
    ax.xaxis.set_ticklabels(np.arange(1, n_classes + 1))
    ax.yaxis.set_ticklabels(np.arange(1, n_classes + 1))
    _ = ax.set_title(
        f"Confusion Matrix for Naive Bayes"
    )
    plt.savefig("confusion_matrix.png")