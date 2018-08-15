import numpy as np
import pandas as pd
import pygal
from pygal.style import DarkSolarizedStyle
from pygal import Config
import datetime

def plot_review_length_hist(reviews_df):
    try:
        bins = np.arange(0, 1001, 50)
        reviews_df['range'] = pd.cut(reviews_df['review_length'], bins, right = True)
        review_length_df = reviews_df[['range', 'review_length']].groupby('range').count().reset_index().rename(columns={'review_length': 'counts'})
        review_length_df['left'] = review_length_df['range'].apply(lambda x: x.left).astype(int)
        review_length_df['right'] = review_length_df['range'].apply(lambda x: x.right).astype(int)
        hist_bin = []
        for index, row in review_length_df.iterrows():
            new_tuple = (row['counts'], row['left'], row['right'])
            hist_bin.append(new_tuple)
        review_length_hist = pygal.Histogram(height=400, show_legend=False, title=u'Review Length Histogram', dynamic_print_values=True,  style=DarkSolarizedStyle(
                          value_font_family='googlefont:Raleway',
                          value_font_size=30,
                          value_colors=('white',)), x_title='Review length(in characters)', y_title='Counts')
        review_length_hist.add('Reviews',  hist_bin)
        review_length_hist = review_length_hist.render_data_uri()
        return review_length_hist
    except Exception as e:
        return str(e)

def plot_review_stars(reviews_df):
    try:
        reviews_200 = reviews_df[reviews_df['review_length'] > 200].groupby('review_rating').count().reset_index()
        reviews_200 = reviews_200[['review_rating','review_author']].rename(columns={'review_author': 'counts'}).sort_values(by=['review_rating'])
        review_star_bar = pygal.Bar(height=400, show_legend=False,dynamic_print_values=True,  style=DarkSolarizedStyle(
                          value_font_family='googlefont:Raleway',
                          value_font_size=30,
                          value_colors=('white',)), x_title='Review Star', y_title='Counts')
        review_star_bar.title = 'Review Stars for Review Length > 200'
        review_star_bar.x_labels = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']
        review_star_bar.add('# of Stars', reviews_200['counts'].tolist())
        review_star_bar = review_star_bar.render_data_uri()
        return review_star_bar
    except Exception as e:
        return str(e)

def plot_monthly_sales(reviews_df):
    try:
        reviews_df['year'] = reviews_df['review_posted_date'].apply(lambda reviews_df:reviews_df.year)
        reviews_df['month'] = reviews_df['review_posted_date'].apply(lambda reviews_df:reviews_df.month)
        monthly_reviews = reviews_df.groupby(['year', 'month']).count().reset_index()
        monthly_reviews['day'] = monthly_reviews['month'].apply(lambda monthly_reviews:1)
        monthly_reviews_counts = monthly_reviews[['year','month', 'day', 'review_posted_date']].rename(columns={'review_posted_date': 'counts'})
        monthly_reviews_counts['date'] = pd.to_datetime(monthly_reviews_counts[['year','month','day']])
        monthly_review_series = pygal.Line(height=350, x_label_rotation=20,show_minor_x_labels=False, show_legend=False,dynamic_print_values=True, style=DarkSolarizedStyle(
                          value_font_family='googlefont:Raleway',
                          value_font_size=30,
                          value_colors=('white',)))
        date_list = list(map(lambda d: d.strftime('%Y-%m-%d'), monthly_reviews_counts['date'].tolist()))
        monthly_review_series.x_labels = date_list
        monthly_review_series.x_labels_major = date_list[::3]
        monthly_review_series.title = 'Estimated Monthly Sales Based on Number of Reviews'
        monthly_review_series.add("Sales", monthly_reviews_counts['counts'].tolist())
        monthly_review_series = monthly_review_series.render_data_uri()
        return monthly_review_series
    except Exception as e:
        return str(e)
