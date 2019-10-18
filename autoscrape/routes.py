from flask import render_template, url_for, flash
from autoscrape.forms import TestScrapeForm
from autoscrape import app


@app.route("/", methods=['POST', 'GET'])
def home():
    form = TestScrapeForm()
    return render_template('index.html', form=form)