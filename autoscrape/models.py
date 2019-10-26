from datetime import datetime
from autoscrape import db


class TestDBClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scrape_query1 = db.Column(db.String, unique=False)
    scrape_url = db.Column(db.String, unique=False)
    date_scraped = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
    result = db.Column(db.String, unique=False)

    def __repr__(self):
        return f"TestScrape('{self.id}','{self.result}', {self.scrape_query1}, {self.scrape_url}, {self.date_scraped})"