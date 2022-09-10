#! /usr/bin/env python3
import sdg

if __name__ == "__main__":
    classifiers = [
        #("Random forest", sdg.models.RandomForestClassifier()),
        #("Naive bayes (TF_IDF)", sdg.models.NaiveBayesClassifier()),
        ("Finetuned Bert", sdg.models.BertClassifier(device=0)),
        #("Zero shot", sdg.models.ZeroShotClassifier(sdg.SDGS, device=0)),
        #("Zero shot with 'None class'", sdg.models.ZeroShotClassifier(list(sdg.SDG_DICT.values()), device=0)),
    ]
    
    _, _, test_x, test_y = sdg.dataset.load_sdg()
    for name, clf in classifiers:
        # Type hinting
        clf: sdg.models.Classifier= clf
        exp = sdg.Experiment(clf)
        exp.run(test_x, test_y, batch_size=32)
        exp.summary(name)
