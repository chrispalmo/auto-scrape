from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

class LoginForm(FlaskForm):

	password = PasswordField('Password',
		validators=[
			DataRequired()
		]
	)
	username = StringField('Username',
		validators=[
			DataRequired()
		]
	)
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


