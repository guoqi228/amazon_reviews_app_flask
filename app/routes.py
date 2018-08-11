# need to import app varibales
from app import app
from flask import render_template, redirect, url_for, flash, request, Response, send_from_directory
from app.forms import SubmitProductIdForm
from app.scrape import scrape_reviews
from app.export import export_csv
from werkzeug.urls import url_parse
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
        export_csv(reviews_df, form.productId.data)
        reviews_df_string = reviews_df.to_string()
        filename = form.productId.data + '.csv'
        path = './static/csv/' + form.productId.data + '.csv'
        if reviews_df.shape[0] > 50:
            reviews_df_html = reviews_df.iloc[:50].to_html()
            return render_template('overview.html', reviews_df_html= reviews_df_html, reviews_df_string=reviews_df_string, path=path, filename=filename)
        else:
            reviews_df_html = reviews_df.to_html()
            return render_template('overview.html', reviews_df_html= reviews_df_html, reviews_df_string=reviews_df_string, path=path, filename=filename)
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
