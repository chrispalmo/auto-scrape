from datetime import datetime
from autoscrape import db

class Session(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status_active = db.Column(db.Boolean, unique=False, default=True)
	status_completed = db.Column(db.Boolean, unique=False, default=False)
	status_errors = db.Column(db.Boolean, unique=False, default=False) 
	date = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	description = db.Column(db.String, nullable=False)
	scraper = db.Column(db.String, nullable=False)
	logs = db.relationship('LogEntry', backref='session', lazy=True)

	def __repr__(self):
		return f"Session('id: {self.id}, description: {self.description}, date: {self.date}"

class LogEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	message = db.Column(db.String, unique=False, nullable=False)
	session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

class TestDBClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scrape_query1 = db.Column(db.String, unique=False)
    scrape_url = db.Column(db.String, unique=False)
    date_scraped = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
    result = db.Column(db.String, unique=False)

    def __repr__(self):
        return f"TestScrape('{self.id}','{self.result}', {self.scrape_query1}, {self.scrape_url}, {self.date_scraped})"