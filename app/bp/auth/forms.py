# third party imports
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

# local imports
from ...models import User

class RegisterForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    #full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')


class LoginForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')

class EmailForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])


