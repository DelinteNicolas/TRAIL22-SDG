from multiprocessing.sharedctypes import Value
from sdg.models.bert import BertClassifier
from sdg.models.random_forest import RandomForestClassifier
from sdg.models.tf_idf import NaiveBayesClassifier
from sdg.models.zero_shot import ZeroShotClassifier


def before_all(context):
    try:
        cls: str = context.config.userdata['cls']
    except KeyError:
        cls = 'bert0.2'
    if cls == 'bert0.1':
        context.classifier = BertClassifier(filename="DelinteNicolas/SDG_classifier_v0.1.0")
    elif cls == 'bert0.2':
        context.classifier = BertClassifier(filename="DelinteNicolas/SDG_classifier_v0.0.2")
    elif cls == 'random-forest':
        context.classifier = RandomForestClassifier()
    elif cls == 'tf-idf':
        context.classifier = NaiveBayesClassifier()
    elif cls == 'zero-shot':
        context.classifier = ZeroShotClassifier()
    else:
        raise ValueError(f"Unknown classifier {cls}")
    context.config.outfiles = [cls]