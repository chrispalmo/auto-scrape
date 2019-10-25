from datetime import datetime
from autoscrape import db


class TestDBClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_scraped = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String, unique=False, nullable=True)


class TestDBClass2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=False, nullable=False)
    filter_query1 = db.Column(db.String, unique=False, nullable=False)
    date_scraped = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String, unique=False, nullable=True)

class TestDBClass3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=False)
    filter_query1 = db.Column(db.String, unique=False)
    date_scraped = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
    result = db.Column(db.String, unique=False)

    def __repr__(self):
        return f"TestScrape('{self.id}','{self.result}')"