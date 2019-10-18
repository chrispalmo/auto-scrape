from flask import render_template, url_for, flash
from autoscrape import app


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/test_scrape")
def test_scrape():
    return render_template('test_scrape.html')
