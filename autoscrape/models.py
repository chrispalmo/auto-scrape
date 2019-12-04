from datetime import datetime
from autoscrape import db

class Session(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_started = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	date_stopped = db.Column(db.DateTime, unique=False)
	description = db.Column(db.String, nullable=False)
	scraper = db.Column(db.String, nullable=False)
	status = db.Column(db.String, nullable=False, default="Active")
	logs = db.relationship('LogEntry', backref='session', lazy=True)
	data = db.relationship('DataEntry', backref='session', lazy=True)

	def __repr__(self):
		return f"Session('id: {self.id}, status: {self.status}, date_started: {self.date_started}, date_stopped: {self.date_stopped}, description: {self.description}, scraper: {self.scraper})"


class LogEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	message = db.Column(db.String, unique=False, nullable=False)
	session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


class DataEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	scraper = db.Column(db.String, unique=False, nullable=False)
	timestamp = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	url = db.Column(db.String, unique=False, nullable=False)
	data_label = db.Column(db.String, unique=False, nullable=False)
	data = db.Column(db.String, unique=False, nullable=True)
	session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


class TestDBClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	scrape_query1 = db.Column(db.String, unique=False)
	scrape_url = db.Column(db.String, unique=False)
	date_scraped = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	result = db.Column(db.String, unique=False)

	def __repr__(self):
		return f"TestScrape('{self.id}','{self.result}', {self.scrape_query1}, {self.scrape_url}, {self.date_scraped})"