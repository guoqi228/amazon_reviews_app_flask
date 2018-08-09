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
        if len(form.productId.data) != 10:
            flash('Invalid ASIN number!')
            time.sleep(2)
            flash(' Redirecting...')
            return redirect(url_for('index'))
        reviews_df = scrape_reviews(form.productId.data)
        reviews_df_html = reviews_df.to_html()
        return render_template('showoverview.html', reviews_df_html= reviews_df_html)
    return render_template('index.html', form = form)

@app.route('/modal', methods = ['GET', 'POST'])
def modal():
    return render_template('modal.html')
