import re
import string
from typing import List
import spacy
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

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


def get_vectorizer() -> TfidfVectorizer:
    vectorizer = TfidfVectorizer(
        smooth_idf=True,
        use_idf=True, 
        stop_words="english", 
        analyzer='word',
        ngram_range=(1, 1), 
        max_df=0.1, 
        min_df=4/1664
    )
    return vectorizer
