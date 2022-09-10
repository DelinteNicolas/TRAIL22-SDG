from transformers import pipeline
from sdg.models.bert import BertClassifier

def before_all(context):
    context.classifier = BertClassifier() 