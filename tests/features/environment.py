from sdg.models.bert import BertClassifier
from sdg.models.random_forest import RandomForestClassifier
from sdg.models.tf_idf import NaiveBayesClassifier
from sdg.models.zero_shot import ZeroShotClassifier
import sdg


def before_all(context):
    classifier_name = load_classifier_name(context)
    if classifier_name == 'bert':
        version = load_version(context)
        context.classifier = BertClassifier(filename=f"DelinteNicolas/SDG_classifier_v{version}")
    elif classifier_name == 'random-forest':
        context.classifier = RandomForestClassifier()
    elif classifier_name == 'naive-bayes':
        context.classifier = NaiveBayesClassifier()
    elif classifier_name == 'zero-shot':
        context.classifier = ZeroShotClassifier(list(sdg.SDG_DICT.values()))
    else:
        raise ValueError(f"Unknown classifier {classifier_name}")

def load_version(context):
    try:
        version: str = context.config.userdata['version']
    except KeyError:
        version = '0.0.4'
    return version

def load_classifier_name(context):
    try:
        cls: str = context.config.userdata['cls']
    except KeyError:
        cls = 'bert'
    return cls