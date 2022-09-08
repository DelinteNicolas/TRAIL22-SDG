#! /usr/bin/env python3
import sdg
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score#, auc, roc_curve
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def eval_classifier(n_classes, Y_true,Y_pred, pred ):
    acc = accuracy_score(Y_true, Y_pred)
    print('accuracy :',100*acc.round(3))

    precision = precision_score(Y_true, Y_pred, average='weighted')#micro, macro, weighted
    print('precision:',100*precision.round(3))

    recall = recall_score(Y_true, Y_pred, average='macro')#micro, macro, weighted
    print('recall   :',100*recall.round(3))

    roc_auc = roc_auc_score(Y_true, pred, multi_class='ovo') #'raise', 'ovr', 'ovo'
    print('roc_auc  :',100*roc_auc.round(3))

    fig, ax = plt.subplots(figsize=(10, 5))
    ConfusionMatrixDisplay.from_predictions(Y_true, Y_pred, ax=ax)
    ax.xaxis.set_ticklabels(np.arange(1, n_classes + 1))
    ax.yaxis.set_ticklabels(np.arange(1, n_classes + 1))
    _ = ax.set_title(
        f"Confusion Matrix for Naive Bayes"
    )
    plt.savefig("confusion_matrix.png")


if __name__ == "__main__":
    tk = sdg.tokenizers.lemmatize_stem
    model, vectorizer = sdg.models.tf_idf_classifier(tk)
    _, _, test_x, test_y = sdg.dataset.load_sdg()
    test_x = vectorizer.transform([tk(x) for x in test_x])
    test_y = np.array(test_y) - 1 # Because SDG labels start at 1
    predicted_probs = model.predict_proba(test_x)
    predicted_labels = np.argmax(predicted_probs, axis=-1)
    eval_classifier(17, test_y, predicted_labels, predicted_probs)
    