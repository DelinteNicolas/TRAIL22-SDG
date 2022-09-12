#! /usr/bin/env python3
import sdg


if __name__ == "__main__":
    clf = sdg.models.BertClassifier("DelinteNicolas/SDG_classifier_v0.0.1")
    sdg.pdf_classification.annotate_pdf(clf, "data/mouse.pdf")
    exit()
    