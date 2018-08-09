# need to import app varibales
from app import app
from flask import render_template, redirect, url_for, flash, request
from app.forms import SubmitProductIdForm
from app.scrape import scrape_reviews
from werkzeug.urls import url_parse
import time

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = SubmitProductIdForm()
    if form.validate_on_submit():
        reviews_df = scrape_reviews(form.productId.data)
        if reviews_df.shape[0] == 0:
            flash('* Something went wrong, please check your ASIN number!')
            time.sleep(3)
            return redirect(url_for('index'))
        reviews_df_html = reviews_df.to_html()
        return render_template('showoverview.html', reviews_df_html= reviews_df_html)
    return render_template('index.html', form = form)
