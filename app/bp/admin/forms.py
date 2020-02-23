# third party imports
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

# local imports
from ...extensions import images, documents
from ...models import User, ROLES

roles = []
for k, v in ROLES.items():
    roles.append((v,k))
 
class UserForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    full_name = StringField('Full Name')
    role = SelectField('Role', choices=roles, coerce=int)

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address already registered!')
 
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already registered!')

class UserEditForm(Form):
    full_name = StringField('Full Name')
    role = SelectField('Role', choices=roles, coerce=int)

class PageForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    lead = StringField('Lead')
    body = TextAreaField('Content', validators=[DataRequired()])
    published = BooleanField('Published')

class CourseForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    lead = StringField('Lead')
    body = TextAreaField('Content', validators=[DataRequired()])

class ImageUploadForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    media = FileField('Media', validators=[FileRequired(),FileAllowed(images, 'Images only!')])

class DocumentUploadForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    media = FileField('Media', validators=[FileAllowed(documents, 'File type not allowed!')])

class SettingForm(Form):
    name = StringField('Key', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    min_value = StringField('Min Value')
    max_value = StringField('Max Value')

class WidgetForm(Form):
    name = StringField('Name', validators=[DataRequired()])

class WidgetItemForm(Form):
    heading = StringField('Heading')
    body = TextAreaField('Content')
    tagline = StringField('Tagline')
    image =FileField('Image', validators=[FileAllowed(images, 'Images only!')]) 
    action = StringField('Action')
    action_url = StringField('Action url')

