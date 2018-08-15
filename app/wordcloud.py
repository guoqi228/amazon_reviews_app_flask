import matplotlib
matplotlib.use('agg')
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import safe_get_stop_words
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import os

def group_df(reviews_df):
    reviews_df['rating_text'] = None
    reviews_df['rating_text'].loc[reviews_df['review_rating'] < 3] = '1 or 2 stars'
    reviews_df['rating_text'].loc[reviews_df['review_rating'] > 3] = '4 or 5 stars'
    reviews_by_rating = reviews_df.groupby('rating_text')['review_text'].apply(list)
    reviews_by_rating = reviews_by_rating.reset_index(drop=False)
    return reviews_by_rating

def make_word_cloud(df, ngram_min, ngram_max, name):
    my_path = os.path.abspath(os.path.dirname(__file__)) + '/static/wordcloud/'
    stop_words = safe_get_stop_words('en')
    filenames=[]
    for ind, row in df.iterrows():
        data = row['review_text']
        num_words = 200
        ngram_range = (ngram_min, ngram_max)
        count_vectorizer = CountVectorizer(lowercase=True,stop_words=stop_words,ngram_range=ngram_range)
        counts = count_vectorizer.fit_transform(data)
        counts = counts.toarray().sum(axis=0)
        count_weighting = dict(zip(count_vectorizer.get_feature_names(), counts))
        count_weighting_df = pd.DataFrame.from_dict(count_weighting, orient='index')
        count_weighting_df = count_weighting_df.reset_index(drop=False)
        count_weighting_df.columns = ['word', 'count']

        count_weighting_df = count_weighting_df.sort_values(['count'], ascending=False)
        count_weighting_df = count_weighting_df.set_index('word')

        word_cloud_freq = count_weighting_df['count'].head(num_words).to_dict()
        wordcloud = WordCloud(collocations=False).generate_from_frequencies(word_cloud_freq)
        plotname = '{}_{}.png'.format(name,ind+1)
        filenames.append(plotname)
        url = my_path + plotname
        fig = plt.figure(figsize=(10,10))
        plt.imshow(wordcloud, cmap=plt.cm.bone, interpolation='bilinear')
        plt.axis("off")
        fig.savefig(url,transparent = True, bbox_inches = 'tight', pad_inches = 0)
    return filenames
