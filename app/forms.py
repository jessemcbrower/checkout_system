from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class DeviceInfo(Form):
	name = StringField('name', validators=[DataRequired()])
	type = SelectField('type', choices=[('Mac', 'Mac'), ('Dell', 'Dell'), ('iPad', 'iPad'), ('MiFi', 'MiFi')], validators=[DataRequired()])
	user = StringField('user', validators=[DataRequired()])
	tag = StringField('tag', validators=[DataRequired()])

class LoginForm(Form):
	firstname = StringField('firstname', validators=[DataRequired()])
	lastname = StringField('lastname', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	confirm = PasswordField('confirm', validators=[DataRequired()])
	submit = SubmitField('Submit')
	login = SubmitField('Login')