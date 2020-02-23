from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from autoscrape import db, login_manager, app

#Specifically named function. Tells flask_login what data is stored in the login session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)        

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


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
	recommendation = db.Column(db.String, unique=False, nullable=True)
	company = db.Column(db.String, unique=False, nullable=True)
	analyst = db.Column(db.String, unique=False, nullable=True)
	latest_review = db.Column(db.String, unique=False, nullable=True)
	review_price = db.Column(db.Numeric, unique=False, nullable=True)
	current_price = db.Column(db.Numeric, unique=False, nullable=True)
	buy_below = db.Column(db.Numeric, unique=False, nullable=True)
	sell_above = db.Column(db.Numeric, unique=False, nullable=True)
	buy_margin = db.Column(db.Numeric, unique=False, nullable=True)
	sell_margin = db.Column(db.Numeric, unique=False, nullable=True)
	max_portfolio = db.Column(db.String, unique=False, nullable=True)

	def __repr__(self):
		return f"IntelligentInvestor('id: {self.id}, timestamp: {self.timestamp}," \
			   f" company_name: {self.company_name}, analyst_name: {self.analyst_name}," \
			   f" latest_review: {self.latest_review}, review_price: {self.review_price}," \
			   f" current_price: {self.current_price}, buy_below: {self.buy_below}," \
			   f" sell_above: {self.sell_above}, max_portfolio: {self.max_portfolio})"