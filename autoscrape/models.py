from datetime import datetime
from autoscrape import db

class Session(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.String, nullable=False, default="Active")
	date_started = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	date_stopped = db.Column(db.DateTime, unique=False)
	description = db.Column(db.String, nullable=False)
	scraper = db.Column(db.String, nullable=False)
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
	timestamp = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	scrape_url = db.Column(db.String, unique=False, nullable=False)
	scrape_function = db.Column(db.String, unique=False, nullable=False)
	scrape_query = db.Column(db.String, unique=False, nullable=False)
	element_1 = db.Column(db.String, unique=False, nullable=True)
	element_2 = db.Column(db.String, unique=False, nullable=True)
	element_3 = db.Column(db.String, unique=False, nullable=True)
	element_4 = db.Column(db.String, unique=False, nullable=True)
	element_5 = db.Column(db.String, unique=False, nullable=True)
	session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


class TestDBClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	scrape_query1 = db.Column(db.String, unique=False)
	scrape_url = db.Column(db.String, unique=False)
	date_scraped = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	result = db.Column(db.String, unique=False)

	def __repr__(self):
		return f"TestScrape('{self.id}','{self.result}', {self.scrape_query1}, {self.scrape_url}, {self.date_scraped})"