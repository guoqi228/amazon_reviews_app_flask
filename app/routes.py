# need to import app varibales
from app import app
from flask import render_template, redirect, url_for, flash, request, Response, send_from_directory, make_response
from app.forms import SubmitProductIdForm, RidgePredictionForm, AdaPredictionForm
from app.scrape import scrape_reviews, get_product_info
from app.export import export_csv
from app.plots import plot_review_length_hist, plot_review_stars, plot_monthly_sales
from werkzeug.urls import url_parse
from app.sentiment import customer_sentiment
from app.wordcloud import make_word_cloud, group_df
from app.prediction import ridge_predict_plot, boost_decision_plot
from app.get_csv import get_csv_file
import pandas as pd
import time
import os

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = SubmitProductIdForm()
    if form.validate_on_submit():
        reviews_df = scrape_reviews(form.productId.data)
        if reviews_df.shape[0] == 0:
            flash('WARNING: Something went wrong, please check your ASIN number!')
            time.sleep(3)
            return redirect(url_for('index'))
        product_info = get_product_info(form.productId.data)
        product_name = product_info[0]
        if len(product_name) > 80:
            product_name = product_name[0:80] + ' ...'
        product_reviews = product_info[1]
        product_rating = product_info[2]
        export_csv(reviews_df, form.productId.data)
        reviews_df_string = reviews_df.to_string()
        filename = form.productId.data + '.csv'
        path = './static/csv/' + form.productId.data + '.csv'
        hist_plot = plot_review_length_hist(reviews_df)
        star_plot = plot_review_stars(reviews_df)
        sales_plot = plot_monthly_sales(reviews_df)
        ad_rating = reviews_df['review_rating'][reviews_df['review_length'] > 200].mean()
        ad_rating = round(ad_rating, 2)
        cs = customer_sentiment(reviews_df)
        cs1 = str(round(cs[0]))
        cs2 = str(round(cs[1]))
        cs3 = str(round(cs[2]))
        cs4 = str(round(cs[3]))
        wordcloud_df = group_df(reviews_df)
        plotnames = make_word_cloud(wordcloud_df, 3, 3, form.productId.data)
        plot1 = plotnames[0]
        plot2 = plotnames[1]
        if reviews_df.shape[0] > 50:
            reviews_df_html = reviews_df.drop(['range', 'year', 'month','rating_text'], axis=1).iloc[:50].to_html()
            return render_template('overview.html', reviews_df_html= reviews_df_html, reviews_df_string=reviews_df_string, path=path, filename=filename, product_name=product_name, product_reviews=product_reviews, product_rating=product_rating, hist_plot=hist_plot, ad_rating=ad_rating, star_plot=star_plot, cs1=cs1, cs2=cs2, cs3=cs3, cs4=cs4, plot1=plot1, plot2=plot2, sales_plot=sales_plot)
        else:
            reviews_df_html = reviews_df.drop(['range', 'year', 'month','rating_text'], axis=1).to_html()
            return render_template('overview.html', reviews_df_html= reviews_df_html, reviews_df_string=reviews_df_string, path=path, filename=filename, product_name=product_name, product_reviews=product_reviews, product_rating=product_rating, hist_plot=hist_plot, ad_rating=ad_rating, star_plot=star_plot, cs1=cs1, cs2=cs2, cs3=cs3, cs4=cs4, plot1=plot1, plot2=plot2, sales_plot=sales_plot)
    return render_template('index.html', form = form)

# @app.route("/download/<data>")
# def download_csv(data):
#    csv = data
#    return Response(
#        csv,
#        mimetype="text/csv",
#        headers={"Content-disposition":
#                 "attachment; filename=reviews.csv"})

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/prediction/<data>', methods = ['GET', 'POST'])
def prediction(data):
    ridgeform = RidgePredictionForm()
    adaform = AdaPredictionForm()
    if ridgeform.validate_on_submit():
        degree = ridgeform.degree.data
        alpha = ridgeform.alpha.data
        reviews_df = get_csv_file(data)
        reviews_df['review_posted_date'] = pd.to_datetime(reviews_df['review_posted_date'],format='%Y-%m-%d')
        ridgeplot = ridge_predict_plot(reviews_df, degree, alpha)
        return render_template('ridge.html', ridgeplot=ridgeplot)
    if adaform.validate_on_submit():
        depth = adaform.depth.data
        reviews_df = get_csv_file(data)
        reviews_df['review_posted_date'] = pd.to_datetime(reviews_df['review_posted_date'],format='%Y-%m-%d')
        adaplot = boost_decision_plot(reviews_df, depth)
        return render_template('ada.html', adaplot=adaplot)
    return render_template('prediction.html', ridgeform = ridgeform, adaform=adaform)
