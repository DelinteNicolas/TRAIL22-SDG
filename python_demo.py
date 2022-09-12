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

    colors = {"SDG1: No Poverty": "#eb1c2d",
              "SDG10: Reduced Inequality": "#ff45aa",
              "SDG11: Sustainable Cities and Communities": "#f99d26",
              "SDG12: Responsible Consumption and Production": "#cf8d2a",
              "SDG13: Climate Action": "#66a559",
              "SDG14: Life Below Water": "#4dc4ff",
              "SDG15: Life on Land": "#48ff5a",
              "SDG16: Peace and Justice Strong Institutions": "#4ab7ff",
              "SDG17: Partnerships to achieve the Goal": "#448aff",
              "SDG2: Zero Hunger": "#D3A029",
              "SDG3: Good Health and Well-being": "#43ce6b",
              "SDG4: Quality Education": "#c31f33",
              "SDG5: Gender Equality": "#ef402b",
              "SDG6: Clean Water and Sanitation": "#00aed9",
              "SDG7: Affordable and Clean Energy": "#fdb713",
              "SDG8: Decent Work and Economic Growth": "#ff3b70",
              "SDG9: Industry, Innovation and Infrastructure": "#f36d25"}

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
        if sdg[0]['score'] > .9 and len(txt) > 10 and sdg[0]['label']!="Not a SDG":
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

    model_name_or_path = "DelinteNicolas/SDG_classifier_v0.0.2"

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
