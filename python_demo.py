# -*- coding: utf-8 -*-

import re
import sys
import json
from tqdm import tqdm
from spacy import displacy
from PyPDF2 import PdfReader
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification


def predict(text):

    colors = {"SDG1: No Poverty": "#e16f78",
              "SDG10: Reduced Inequality": "#e26cac",
              "SDG11: Sustainable Cities and Communities": "#e5b270",
              "SDG12: Responsible Consumption and Production": "#e3b36b",
              "SDG13: Climate Action": "#86df73",
              "SDG14: Life Below Water": "#6fbce2",
              "SDG15: Life on Land": "#70e47b",
              "SDG16: Peace and Justice Strong Institutions": "#68aedc",
              "SDG17: Partnerships to achieve the Goal": "#7099de",
              "SDG2: Zero Hunger": "#e6c67b",
              "SDG3: Good Health and Well-being": "#72dd91",
              "SDG4: Quality Education": "#e1707d",
              "SDG5: Gender Equality": "#e17669",
              "SDG6: Clean Water and Sanitation": "#78cce1",
              "SDG7: Affordable and Clean Energy": "#e2bf6e",
              "SDG8: Decent Work and Economic Growth": "#e07391",
              "SDG9: Industry, Innovation and Infrastructure": "#e49971"}

    doc = {
        "text": text,
        "ents": [],
        "colors": colors,
        "title": None
    }

    text2 = re.sub(
        r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)', '.', text)

    txtList = text2.split('.')

    for txt in tqdm(txtList):
        sdg = classifier(txt)
        if sdg[0]['score'] > .9 and len(txt) > 15 and sdg[0]['label'] != "Not a SDG":
            doc["ents"].append({"start": text.index(txt),
                                "end": text.index(txt)+len(txt)+1,
                                "label": sdg[0]['label']})

    html = displacy.render(doc, style="ent", page=True,
                           manual=True, minify=True, options={"colors": colors})
    html = (
        "<div style='overflow:auto'>"
        + html
        + "</div>"
    )

    html = html.replace('line-height: 1', 'line-height: 2.5')
    html = html.replace('</br>', '')

    return html


if __name__ == '__main__':

    model_name_or_path = "DelinteNicolas/SDG_classifier_v0.0.4"

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    classifier = pipeline("text-classification", model=model,
                          tokenizer=tokenizer)

    filename = sys.argv[1]
    if filename.endswith(".pdf"):
        file = filename[:-4]
        reader = PdfReader(filename)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    elif filename.endswith(".json"):
        file = filename[:-5]
        text = json.load(filename)
    elif filename.endswith(".txt"):
        file = filename[:-4]
        with open(filename) as f:
            text = f.read()
    else:
        print("Unsupported file type")

    html = predict(text)

    out = open(file+".html", "w")
    out.write(html)
    out.close()
