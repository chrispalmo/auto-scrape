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


class IntelligentInvestor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, unique=False, default=datetime.utcnow)
	company_name = db.Column(db.String, unique=False, nullable=True)
	analyst_name = db.Column(db.String, unique=False, nullable=True)
	latest_review = db.Column(db.String, unique=False, nullable=True)
	review_price = db.Column(db.Numeric, unique=False, nullable=True)
	current_price = db.Column(db.Numeric, unique=False, nullable=True)
	buy_below = db.Column(db.Numeric, unique=False, nullable=True)
	sell_above = db.Column(db.Numeric, unique=False, nullable=True)
	additional_discount = db.Column(db.Numeric, unique=False, nullable=True)
	sell_margin = db.Column(db.Numeric, unique=False, nullable=True)
	max_portfolio = db.Column(db.String, unique=False, nullable=True)

	def __repr__(self):
		return f"IntelligentInvestor('id: {self.id}, timestamp: {self.timestamp}," \
			   f" company_name: {self.company_name}, analyst_name: {self.analyst_name}," \
			   f" latest_review: {self.latest_review}, review_price: {self.review_price}," \
			   f" current_price: {self.current_price}, buy_below: {self.buy_below}," \
			   f" sell_above: {self.sell_above}, max_portfolio: {self.max_portfolio})"