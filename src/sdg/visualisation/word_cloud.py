import sdg
import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

import matplotlib.pyplot as plt


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
    df, _ = sdg.dataset.load_sdg_dataframe(tokenizer=sdg.tokenizers.lemmatize)
    df_grouped = df[['label','text']].groupby(by='label').agg(lambda x:' '.join(x))
    # Creating Document Term Matrix
    cv=CountVectorizer(analyzer='word')
    data=cv.fit_transform(df_grouped['text'])
    print(cv.get_feature_names())
    df_dtm = pd.DataFrame(data.toarray(), columns=cv.get_feature_names())
    df_dtm.index=df_grouped.index

    # Transposing document term matrix
    df_dtm=df_dtm.transpose()
    print(df_dtm)

    # Plotting word cloud for each SDG
    for product in df_dtm.columns:
        generate_wordcloud(df_dtm[product].sort_values(ascending=False), product, save_dir)
