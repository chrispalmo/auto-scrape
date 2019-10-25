from datetime import datetime
from autoscrape import db


class TestDBClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_scraped = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return f"TestScrape('{self.id}','{self.result}')"