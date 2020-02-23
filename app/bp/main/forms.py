from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField

class ProfileForm(Form):
    bio = StringField('About Me')


