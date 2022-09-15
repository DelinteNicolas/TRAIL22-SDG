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
        random_state = load_random_state(context)
        context.classifier = RandomForestClassifier(random_state=random_state)
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
        return context.config.userdata['model']
    except KeyError:
        return 'bert'

def load_random_state(context):
    try:
        return int(context.config.userdata['random_state'])
    except KeyError:
        return None