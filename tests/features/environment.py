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
        version = load_version(context, default='prior')
        context.classifier = NaiveBayesClassifier(version == 'prior')
    elif classifier_name == 'zero-shot':
        context.classifier = ZeroShotClassifier(list(sdg.SDG_DICT.values()))
    else:
        raise ValueError(f"Unknown classifier {classifier_name}")

def load_version(context, default='0.0.4'):
    try:
        return context.config.userdata['version']
    except KeyError:
        return default

def load_classifier_name(context):
    try:
        cls: str = context.config.userdata['model']
    except KeyError:
        cls = 'bert'
    return cls