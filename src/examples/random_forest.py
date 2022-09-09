#! /usr/bin/env python3
import sdg
import numpy as np

if __name__ == "__main__":
    tk = sdg.tokenizers.lemmatize_stem
    clf = sdg.models.random_forest_classifier(tk)
    _, _, test_x, test_y = sdg.dataset.load_sdg()
    test_y = np.array(test_y) - 1 # Because SDG labels start at 1
    predicted_probs = clf(test_x)
    predicted_labels = np.argmax(predicted_probs, axis=-1)
    sdg.utils.eval_classifier(17, test_y, predicted_labels, predicted_probs)
    