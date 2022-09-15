from typing import Dict, List, Tuple
import sdg
from spacy import displacy
import re
import os
from time import time_ns
import shutil
import subprocess
from bs4 import BeautifulSoup
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
        text = text.replace("\n", " ")
        text = re.sub(
            r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)', '.', text)
    os.remove("tmp.txt")
    return re.split(r'[;.\?!]', text)


def save_image_names(soup: BeautifulSoup) -> Tuple[BeautifulSoup, Dict[str, str]]:
    translations = {}
    for file in os.listdir("tmp"):
        if file.endswith("jpg") or file.endswith("png"):
            src = os.path.join("tmp", file)
            dst = os.path.join("html", "public", "tmp_images", file)
            shutil.move(src, dst)
    for img in soup.select("img"):
        timestamp = f"{time_ns()}"
        img_location = img['src'].replace("tmp/", "tmp_images/")
        translations[timestamp] = img_location
        img["src"] = timestamp
    return soup, translations


def replace_image_paths(soup: BeautifulSoup) -> BeautifulSoup:
    # Move images to another temp folder
    for file in os.listdir("tmp"):
        if file.endswith("jpg") or file.endswith("png"):
            src = os.path.join("tmp", file)
            dst = os.path.join("html", "public", "tmp_images", file)
            shutil.move(src, dst)
    for img in soup.select("img"):
        path = img["src"]
        new_path = path.replace("tmp/", "tmp_images/")
        img["src"] = new_path
    return soup


def save_urls(soup: BeautifulSoup) -> Tuple[BeautifulSoup, Dict[str, str]]:
    replacements = {}
    body = str(soup.body)
    body = body.replace("&amp;", "&")
    matches = re.finditer(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)', body)
    indices = [m.span() for m in matches]
    i = 0
    for start, stop in reversed(indices):
        timestamp = f"{time_ns()}"
        s = body[start:stop]
        print(i, s)
        i += 1
        replacements[timestamp] = body[start:stop]
        # if "www.reptilesinc.com.au/shopshow.toy" in replacements[timestamp]:
        #     print("www.reptilesinc.com.au/shopshow.toy")
        #     s = body[start:stop]
        #     print(s)
        body = body[:start] + timestamp + body[stop:]
    soup = BeautifulSoup(body)
    return soup, replacements


def sanitize(html_content: str) -> Tuple[str, Dict[str, str]]:
    """
    Sanitize the html by replacing urls and file names by unique IDs
    Returns
     - The sanitized html
     - A dictionary mapping from IDs to whatever has been replaced
    """
    soup = BeautifulSoup(html_content)
    soup, translations = save_image_names(soup)
    soup, url_translations = save_urls(soup)
    translations.update(url_translations)
    return str(soup.body), translations


def split_sentences(html_body: str) -> List[str]:
    """
    Split the html body down to sentences while preserving splitting terms (.;?!).
    """
    indices = [m.span() for m in re.finditer(r'[;.\?!]', html_body)]
    sentences = []
    start = 0
    for _, stop in indices:
        sentences.append(html_body[start:stop])
        start = stop
    return sentences


def build_preview_html(sentences: List[str], ids: Dict[str, str]) -> str:
    """
    - Concatenates the sentences into an html document
    - Adds a <sentence id="..."></sentence> tag to every sentence
    - Restores the IDs to their original value
    
    """
    id_sentences = []
    for i, s in enumerate(sentences):
        if i == 179:
            print(i)
        s = s.strip()
        start = 0
        # Avoid messing with html tags by starting the <sentence> tag
        while s[start] == "<" and start < len(s):
            start += s[start:].index(">") + 1
        s = s[:start] + f'<sentence id="id-{i}">' + s[start:] + "</sentence>"
        id_sentences.append(s)
    #sentences = [f'<sentence id="{i}">{s}</sentence>' for i, s in enumerate(sentences)]
    body = "".join(id_sentences)
    return restore_html(body, ids)


def get_plain_sentences(html_sentence: List[str]) -> List[str]:
    """Extracts plain text from the html sentences"""
    plain_sentences = []
    for s in html_sentence:
        soup = BeautifulSoup(s)
        plain_text = soup.text
        plain_text = plain_text.replace("\n", "").strip()
        plain_text = re.sub(r"\s+", " ", plain_text)
        plain_sentences.append(plain_text)
    return plain_sentences


def restore_html(body: str, matches: Dict[str, str]) -> str:
    """Restore the html with all the unique IDs replaced by their original value"""
    for key, value in matches.items():
        body = body.replace(key, value)
    return body


def get_html(pdf_location: str) -> Tuple[str, List[str]]:
    """
    Extracts the PDF text to html and splits it into sentences.
    Returns:
        - The html body where sentences are included in a <sentence id="..."> </sentence> tag
        - The plain text sentences
    """
    _ = subprocess.call([
        "pdftohtml",
        pdf_location,
        "tmp/tmp.html"
    ])

    with open("tmp/tmps.html", "r") as f:
        content = f.read()
    content, matches = sdg.pdf_classification.sanitize(content)
    sentences = sdg.pdf_classification.split_sentences(content)
    plain_sentences = sdg.pdf_classification.get_plain_sentences(sentences)
    output_html = sdg.pdf_classification.build_preview_html(sentences, matches)
    return output_html, plain_sentences

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
