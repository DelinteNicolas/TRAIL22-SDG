from typing import List
import sdg
from spacy import displacy
import re
import os
import subprocess
from tqdm import tqdm


COLOURS = [
    "#eb1c2d", "#ff45aa", "#f99d26", "#cf8d2a", "#66a559", 
    "#4dc4ff", "#48ff5a", "#4ab7ff", "#448aff", "#D3A029", 
    "#43ce6b", "#c31f33", "#ef402b", "#00aed9", "#fdb713",
    "#ff3b70", "#f36d25", "#A36d25", "#A30d05"
]

def _get_sentences(pdf_location: str) -> List[str]:
    # TODO: gerer les appels concurrents !
    # TODO: gerer les echecs de conversion
    _ = subprocess.call([
        "pdftotext",
        pdf_location,
        "tmp.txt"
    ])
    with open("tmp.txt", "r", encoding="utf8") as f:
        text = f.read()
        text = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)', '.', text)
    os.remove("tmp.txt")
    return re.split(r'[;.\?!]', text)


def annotate_pdf(classifier: sdg.models.Classifier, filename: str):
    sentences = _get_sentences(filename)
    html = predict(classifier, sentences)
    with open("res.html", "w") as out:
        out.write(html)


def predict(classifier: sdg.models.Classifier, sentences: List[str]):
    label2colour = {f"{i}": c for i, c in enumerate(COLOURS)}
    all_text = ".".join(sentences)
    doc = {
        "text": all_text,
        "ents": [],
        "colors": label2colour,
        "title": None
    }
    html2 = """
    <html>
    <body>
    <ol>
    """
    for txt in tqdm(sentences):
        sdg = classifier(txt)
        list_item = "<li>"
        if sdg.confidence > .5 and len(txt) > 10:
            list_item += f'<b style="color: red"> SDG {sdg.sdg}: </b>'
            doc["ents"].append({"start": all_text.index(txt),
                                "end": all_text.index(txt)+len(txt)+1,
                                "label": f"{sdg.sdg}"})
        list_item += f"{txt}</li>\n"
        html2 += list_item
    html2 += """
    </ol>
    </body>
    </html>
    """
    # return html2

    html = displacy.render(doc, style="ent", page=True,
                           manual=True, minify=True, options={"colors": label2colour})
    html = (
        "<div style='overflow:auto'>"
        + html
        + "</div>"
    )

    html = html.replace('line-height: 1', 'line-height: 2.5')
    html = html.replace('</br>', '')

    return html
