from flask import render_template, url_for, flash
from autoscrape import app


@app.route("/")
def home():
    return render_template('index.html')