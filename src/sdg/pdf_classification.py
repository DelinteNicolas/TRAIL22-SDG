from typing import List
import sdg
from PyPDF2 import PdfReader
from spacy import displacy
import re
from tqdm import tqdm
from spacy import displacy
from PyPDF2 import PdfReader


COLOURS = [
    "#eb1c2d", "#ff45aa", "#f99d26", "#cf8d2a", "#66a559", 
    "#4dc4ff", "#48ff5a", "#4ab7ff", "#448aff", "#D3A029", 
    "#43ce6b", "#c31f33", "#ef402b", "#00aed9", "#fdb713",
    "#ff3b70", "#f36d25", "#A36d25", "#A30d05"
]

def _get_sentences(pdf_location: str) -> List[str]:
    reader = PdfReader(pdf_location)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    text = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)', '.', text)
    return re.split(r'[;.\?!]', text)


def annotate_pdf(classifier: sdg.models.Classifier, filename: str):
    sentences = _get_sentences(filename)
    html = predict(classifier, sentences)

    with open("res.html", "w") as out:
        out.write(html)


def predict(classifier: sdg.models.Classifier, sentences: List[str]):
    label2colour = {l: c for l, c in zip(classifier.labels, COLOURS)}
    doc = {
        "text": "".join(sentences),
        "ents": [],
        "colors": label2colour,
        "title": None
    }

    for txt in tqdm(sentences):
        sdg = classifier(txt)
        if sdg.confidence > .5 and len(txt) > 10:
            doc["ents"].append({"start": sentences.index(txt),
                                "end": sentences.index(txt)+len(txt)+1,
                                "label": classifier.labels[sdg.label]})

    html = displacy.render(doc, style="ent", page=True,
                           manual=True, minify=True, options={"colors": label2colour})
    html = "<div style='overflow:auto'>"  + html + "</div>"
    html = html.replace('line-height: 1', 'line-height: 2.5')
    html = html.replace('</br>', '')

    return html
