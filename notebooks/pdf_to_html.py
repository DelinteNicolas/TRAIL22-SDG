from spacy import displacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from PyPDF2 import PdfReader

reader = PdfReader("drive/MyDrive/TRAIL22/pdfs/temp.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

model_name_or_path = "DelinteNicolas/SDG_classifier_v0.0.1"

model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path)

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)


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

    txtList = text.split('.')

    for txt in txtList:
        sdg = classifier(txt)
        if sdg[0]['score'] > .5:
            doc["ents"].append({"start": text.index(txt), "end": text.index(
                txt)+len(txt)+1, "label": sdg[0]['label']})

    html = displacy.render(doc, style="ent", page=True,
                           manual=True, minify=True, options={"colors": colors})
    html = (
        "<div style='overflow:auto'>"
        + html
        + "</div>"
    )

    return html

html=predict(text)

out = open("drive/MyDrive/TRAIL22/pdfs/temp.html","w")
out.write(html)
out.close()