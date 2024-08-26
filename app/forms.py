from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class DeviceInfo(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type = SelectField('type', choices=[('Mac', 'Mac'), ('Dell', 'Dell'), ('iPad', 'iPad'), ('MiFi', 'MiFi')], validators=[DataRequired()])
    user = StringField('user', validators=[DataRequired()])
    tag = StringField('tag', validators=[DataRequired()])

class LoginForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm = PasswordField('confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')
    login = SubmitField('Login')
