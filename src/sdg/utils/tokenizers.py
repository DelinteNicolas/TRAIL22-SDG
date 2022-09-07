import re
import string
import spacy
from nltk.stem import PorterStemmer

porter = PorterStemmer()
nlp = spacy.load('en_core_web_sm',disable=['parser', 'ner'])

def lemmatize(s: str) -> str:
    s = s.lower()
    s = re.sub('[%s0-9]' % re.escape(string.punctuation), '', s)
    s = ' '.join([token.lemma_ for token in nlp(s) if (token.is_stop==False)])
    return s

def lemmatize_stem(s: str) -> str:
    s = lemmatize(s)
    s = ' '.join([porter.stem(token) for token in s.split() if not token.isnumeric() ])
    return s
