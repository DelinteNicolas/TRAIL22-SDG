from typing import Any, Callable, Tuple
import sdg
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score#, auc, roc_curve
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB



def eval_classifier(Y_true, Y_pred, pred, clf):
    n_classes = max(Y_true)
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
    ax.xaxis.set_ticklabels(range(1, n_classes+1))
    ax.yaxis.set_ticklabels(range(1, n_classes+1))
    _ = ax.set_title(
        f"Confusion Matrix for {clf.__class__.__name__}"
    )

def tf_idf(tokenizer: Callable[[str], str]) -> Tuple[MultinomialNB, TfidfVectorizer]:
    """Returns the NaiveBayes classifier and the vectorizer"""
    train, _ = sdg.dataset.load_sdg_dataframe()
    train_corpus = train["text"].apply(tokenizer)
    vectorizer = TfidfVectorizer(
        smooth_idf=True,
        use_idf=True, 
        stop_words="english", 
        analyzer='word',
        ngram_range=(1, 1), 
        max_df=0.1, 
        min_df=4/1664
    )

    X_train_tfidf = vectorizer.fit_transform(train_corpus)
    clf = MultinomialNB()
    clf.fit(X_train_tfidf, train["label"])
    return clf, vectorizer
