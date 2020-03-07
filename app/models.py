# 3rd party imports
#from flask import current_app as app
from flask_login import UserMixin
#import flask.ext.whooshalchemy as wa
from werkzeug.security import generate_password_hash, check_password_hash
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from slugify import slugify
from markdown import markdown
import bleach
import uuid
import datetime

# local imports
from .extensions import db, login_manager, uploads


allowed_tags = ['a', 'b', 'blockqoute', 'i','br', 'ul', 'li', 'ol', 'h1', 'h2','h3', 'p', 'strong', 'em']

ROLES = {
        'user': 1,
        'editor':2,
        'manager':3,
        'admin': 4,
        'developer':5
        }

def generate_uuid():
    return str(uuid.uuid4().hex)[:8]

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, default=generate_uuid)
    created = db.Column(db.DateTime, default = db.func.current_timestamp())
    modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())

class User(Base, UserMixin):

    __tablename__ = 'users'

    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    full_name = db.Column(db.String)
    about_me = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String)
    confirmed=db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime)
    image = db.Column(db.String)
    role = db.Column(db.Integer, default= ROLES['user'])
    pages = db.relationship('Page', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    courses = db.relationship('Course', backref='author', lazy='dynamic')
        

    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(self.password)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

   
    def is_admin(self):
        return self.role == ROLES['admin']


    def is_allowed(self, access_level):
        return self.role >= ROLES[access_level]
    
    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.first_name)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Page(Base):

    __tablename__ = 'pages'
    #__searchable__ = ['title', 'body']

    title = db.Column(db.String)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    slug = db.Column(db.String)
    image = db.Column(db.String)
    published = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #media = db.relationship('Media', backref='page', lazy='dynamic')

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'), tags=allowed_tags, strip=True))

    @property
    def imgsrc(self):
        return uploads.url(self.image)
    
    def __repr__(self):
        return '<Page {}: {}>'.format(self.id, self.title[:20])

db.event.listen(Page.title,'set', Page.slugify)
db.event.listen(Page.body, 'set', Page.on_changed_body)

tags = db.Table('post_tags', 
        db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
        )

class Tag(Base):
    __tablename__ = 'tags'
    
    title = db.Column(db.String)
    slug = db.Column(db.String)

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)
    
    def __repr__(self):
        return '<Tag: {}>'.format(self.title)

db.event.listen(Tag.title,'set', Tag.slugify)

class Post(Base):

    __tablename__ = 'posts'

    title = db.Column(db.String)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    slug = db.Column(db.String)
    image = db.Column(db.String)
    published = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', 
            secondary=tags,
            backref=db.backref('tags', lazy='dynamic'))
    #media = db.relationship('Media', backref='page', lazy='dynamic')

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'), tags=allowed_tags, strip=True))

    @property
    def imgsrc(self):
        return uploads.url(self.image)
    
    def __repr__(self):
        return '<Post {}: {}>'.format(self.id, self.title[:20])

db.event.listen(Post.title,'set', Post.slugify)
db.event.listen(Post.body, 'set', Post.on_changed_body)

class Course(Base):

    __tablename__ = 'courses'

    title = db.Column(db.String)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    image = db.Column(db.String)
    body_html = db.Column(db.Text)
    published = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #media = db.relationship('Media', backref='course', lazy='dynamic')

   
    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)
    
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'), tags=allowed_tags, strip=True))
    

    @property
    def imgsrc(self):
        return uploads.url(self.image)

db.event.listen(Course.title,'set', Course.slugify)
db.event.listen(Course.body, 'set', Course.on_changed_body)

class Video(Base):

    __tablename__ = 'videos'

    youtube_id = db.Column(db.String)

    def __repr__(self):
        return '<Video {}>'.format(self.id)

class Media(Base):

    __tablename__ = 'media'
    
    name = db.Column(db.String)
    filename = db.Column(db.String)
    url = db.Column(db.String)
    path = db.Column(db.String)
    media_type = db.Column(db.String)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
 

    @property
    def imgsrc(self):
        return uploads.url(self.filename)
 
class Setting(Base):

    __tablename__ = 'settings'

    name = db.Column(db.String)
    value = db.Column(db.Text)
    description = db.Column(db.String)

class Widget(Base):
    __tablename__ = 'widgets'

    name = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('WidgetItem', backref='widget', lazy='dynamic')

class WidgetItem(Base):

    __tablename__ = 'widget_items'

    heading = db.Column(db.String)
    body= db.Column(db.String)
    tagline = db.Column(db.String) 
    image = db.Column(db.String)
    action = db.Column(db.String)
    action_url = db.Column(db.String)
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))

    @property
    def imgsrc(self):
        return uploads.url(self.image)

    




