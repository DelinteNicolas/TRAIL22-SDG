#! /usr/bin/env python3
import sdg

if __name__ == "__main__":
    classifiers = [
        #("Random forest", sdg.models.RandomForestClassifier(sdg.SDGS)),
        #("Naive bayes (TF/IDF)", sdg.models.NaiveBayesClassifier(sdg.SDGS)),
        ("Finetuned Bert", sdg.models.BertClassifier(sdg.SDGS, device=0)),
        #("Zero shot", sdg.models.ZeroShotClassifier(sdg.SDGS, device=0)),
    ]
    for name, clf in classifiers:
        print(name, clf.classify("However, with growing pressures on ecosystems, forests also need to adjust to changing conditions"))

    # classifiers = [
    #     ("Random forest", sdg.models.random_forest_classifier()),
    #     ("Naive bayes (TF/IDF)", sdg.models.tf_idf_classifier())
    #     ("Finetuned Bert", sdg.models.load_finetuned_bert()),
    #     ("Zero shot", sdg.models.zero_shot_classifier(device=0)),
    # ]
    # _, _, test_x, test_y = sdg.dataset.load_sdg()
    # for name, clf in classifiers:
    #     exp = sdg.Experiment(clf)
    #     exp.run(test_x, test_y)
    #     exp.summary(name, 18)
