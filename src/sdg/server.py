import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from time import time
import os
import sdg

app = Flask(__name__)
CORS(app)
cache = {}

@app.route("/document/upload", methods=["POST"])
@cross_origin()
def upload_file():
    file = request.files["document"]
    saved_filename = os.path.join("tmp", f"{time()}-{file.filename}")
    file.save(saved_filename)
    html, to_analyze = sdg.pdf_classification.get_html(saved_filename)
    cache[saved_filename] = to_analyze
    return {
        "filename": saved_filename,
        "html": html
    }


@app.route("/model", methods=["POST"])
def add_model(model_name):
    print(f"Adding {model_name} to the models")
    return "OK"

@app.route("/models")
@cross_origin()
def get_models():
    return json.dumps(sdg.models.MODEL_NAMES)


@app.route("/document/analyze", methods=["POST"])
@cross_origin()
def analyze():
    json_data = request.json
    sentences = cache[json_data["filename"]]
    classifier = sdg.models.get_model(json_data["model"])
    results = classifier(sentences)
    return json.dumps([r.to_json() for r in results])


def run(port=5000):
    app.run(port=port, debug=True)