from transformers import pipeline
from sdg.models.bert import load_finetuned_bert

def before_all(context):
    model, tk = load_finetuned_bert()  
    context.classifier = pipeline("text-classification", model=model, tokenizer=tk)