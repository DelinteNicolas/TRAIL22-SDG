#! /usr/bin/env python3
import sdg


if __name__ == "__main__":
    sdg.pdf_classification.annotate_pdf(sdg.models.BertClassifier(), "data/mouse.pdf")
    exit()
    