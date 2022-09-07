import sdg
import re
import string
import spacy
import pandas as pd
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from textwrap import wrap

import matplotlib.pyplot as plt

def _clean_df(df: pd.DataFrame):
    porter = PorterStemmer()
    df['cleaned']=df['text'].apply(lambda x: x.lower())

    # remove punctuations
    '''df['cleaned']=df['cleaned'].apply(lambda x: x.replace('sdg ','sdg_').replace('climate change','climate_change')
    .replace('1','one').replace('2','two').replace('3','three').replace('4','four').replace('5','five').replace('6','six')
    .replace('7','seven').replace('8','eight').replace('9','nine').replace('10','ten').replace('11','eleven').replace('12','twelve')
    .replace('13','thirteen').replace('14','fourteen').replace('15','fifteen').replace('16','sixteen').replace('17','seventeen')
                                        )'''

    df['cleaned']=df['cleaned'].apply(lambda x: re.sub('[%s0-9]' % re.escape(string.punctuation), '', x))

    # Loading model
    nlp = spacy.load('en_core_web_sm',disable=['parser', 'ner'])

    # Lemmatization with stopwords removal
    df['lemmatized']=df['cleaned'].apply(lambda x: ' '.join([token.lemma_ for token in list(nlp(x)) if (token.is_stop==False)]))

    # Stem and remove numbers
    df['stemmed']=df['lemmatized'].apply(lambda x: ' '.join([porter.stem(token) for token in x.split() if not token.isnumeric() ]))
    return df


# Function for generating word clouds
def generate_wordcloud(data: pd.DataFrame, sdg_num: int, save_dir: str):
    title = sdg.SDGS[sdg_num]
    wc = WordCloud(width=400, height=330, max_words=150, colormap="Dark2").generate_from_frequencies(data)
    plt.figure(figsize=(5,4))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.savefig(f"{save_dir}/{title}.png")
    # plt.show()

def wordclouds(save_dir: str):
    # Load the dataset
    ds = sdg.load_sdg_dataset()
    df = pd.DataFrame.from_dict(ds["train"])
    df = _clean_df(df)
    df_grouped = df[['label','lemmatized']].groupby(by='label').agg(lambda x:' '.join(x))
    # Creating Document Term Matrix
    cv=CountVectorizer(analyzer='word')
    data=cv.fit_transform(df_grouped['lemmatized'])
    print(cv.get_feature_names())
    df_dtm = pd.DataFrame(data.toarray(), columns=cv.get_feature_names())
    df_dtm.index=df_grouped.index

    # Transposing document term matrix
    df_dtm=df_dtm.transpose()
    print(df_dtm)

    # Plotting word cloud for each SDG
    for product in df_dtm.columns:
        generate_wordcloud(df_dtm[product].sort_values(ascending=False), product, save_dir)
