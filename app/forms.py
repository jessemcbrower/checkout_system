from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class DeviceInfo(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('Mac', 'Mac'), ('Dell', 'Dell'), ('iPad', 'iPad'), ('MiFi', 'MiFi')], validators=[DataRequired()])
    tag = StringField('Asset Tag', validators=[DataRequired()])
    submit = SubmitField('Add Device')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm = PasswordField('confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')
    login = SubmitField('Login')
