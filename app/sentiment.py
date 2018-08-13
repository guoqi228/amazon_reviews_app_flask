from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer
import nltk
import pandas as pd
import numpy as np


def pa_mapper(text):
    blob = TextBlob(text, analyzer=PatternAnalyzer())
    if blob.sentiment[0] < 0:
        return 0
    elif blob.sentiment[0] > 0:
        return 1

def customer_sentiment(df):
    reviews = df['review_text']
    ratings = df['review_rating']
    total = len(reviews)
    pos = round((ratings[ratings>3].count() / total), 2) * 100
    neg = round((ratings[ratings<3].count() / total), 2) * 100
    pa = reviews.apply(pa_mapper)
    pa_pos = round((pa[pa==1].count() / total), 2) * 100
    pa_neg = round((pa[pa==0].count() / total), 2) * 100
    return [pos, neg, pa_pos, pa_neg]
