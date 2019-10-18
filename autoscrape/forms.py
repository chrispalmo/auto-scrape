from flask_wtf import FlaskForm
from wtforms import SubmitField


class TestScrapeForm(FlaskForm):
    submit = SubmitField('Start Test Scrape')