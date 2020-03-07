from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import IMAGES
# local imports
from ...extensions import uploads
from ...models import ROLES, User

roles = []
for k, v in ROLES.items():
    roles.append((v,k))

class UserForm(Form):
    role = SelectField('Role', choices=roles, coerce=int)

class CommonForm(Form): 
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    image =FileField('Image', validators=[FileAllowed(IMAGES, 'Images only!')])
    published = BooleanField('Published')

class TagForm(Form):
    title = StringField('Tag', validators=[DataRequired()])

class VideoForm(Form):
    youtube_id = StringField('Youtube ID', validators=[DataRequired()])

class MediaForm(Form): 
    name = StringField('Caption', validators=[DataRequired()])
    #body = TextAreaField('Content', validators=[DataRequired()])
    image =FileField('Image', validators=[FileAllowed(IMAGES, 'Images only!')])
    #published = BooleanField('Published')

class SettingForm(Form):
    name = StringField('Key', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])


class WidgetForm(Form):
    name = StringField('Name', validators=[DataRequired()])

class WidgetItemForm(Form):
    heading = StringField('Heading')
    body = TextAreaField('Content')
    tagline = StringField('Tagline')
    image =FileField('Image', validators=[FileAllowed(IMAGES, 'Images only!')]) 
    action = StringField('Action')
    action_url = StringField('Action url')

class ImageForm(Form):
    image =FileField('Image', validators=[FileAllowed(IMAGES, 'Images only!')])
