# third party imports
from flask import render_template, request, redirect, url_for, g
from flask_login import login_required
import json

# local imports
from . import main
from .forms import ProfileForm
from ...models import Setting, Page, Course, Widget, Video, Media, Post

@main.before_request
def load_settings_func():
    app_name = Setting.query.filter_by(name='app_name').first()
    if app_name:
        g.app_name = app_name.value

    location = Setting.query.filter_by(name='location').first()
    if location:
        g.location = location.value

    telephone = Setting.query.filter_by(name='telephone').first()
    if telephone:
        g.telephone = telephone.value

    facebook = Setting.query.filter_by(name='facebook').first()
    if facebook:
        g.facebook = facebook.value

    instagram = Setting.query.filter_by(name='instagram').first()
    if instagram:
        g.instagram = instagram.value


    youtube = Setting.query.filter_by(name='youtube').first()
    if youtube:
        g.youtube = youtube.value

    twitter = Setting.query.filter_by(name='twitter').first()
    if twitter:
        g.twitter = twitter.value

    navigation = Widget.query.filter_by(name='navigation').first()
    if navigation:
        g.navigation = navigation.items

    courses = Course.query.order_by(Course.modified.desc()).limit(6).all()
    if courses:
        g.courses = courses
    


@main.route('/')
def index():
    heroObj = ''
    #introObj = ''
    #featuresObj = ''
    #marketingObj = ''

    hero = Widget.query.filter_by(name='hero').first()
    if hero:
        heroObj = hero

    #intro = Setting.query.filter_by(name='widget_intro').first()
    #if intro and intro.value:
    #    introObj = json.loads(intro.value)

    #features = Setting.query.filter_by(name='widget_features').first()
    #if features and features.value:
    #    featuresObj = json.loads(features.value)

    #marketing = Setting.query.filter_by(name='widget_marketing').first()
    #if marketing and marketing.value:
    #    marketingObj = json.loads(marketing.value)

   # featuresObj = [
   #         {"heading": "Company X", "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ipsum eu nunc commodo posuere et sit amet ligula. ", "image": url_for('static', filename='gettyimages-1093954602-2048x2048.jpeg') },
    #        {"heading": "Company Y", "body": "some body text here Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ipsum eu nunc commodo posuere et sit amet ligula. ", "image": url_for('static', filename='hvac.jpeg') }]


    #marketingObj = [
     #       {"heading": "Affordable Eduction", "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ipsum eu nunc commodo posuere et sit amet ligula. ", "image": url_for('static', filename='blacktailor.jpeg') },
      #      {"heading": "Accredited Courses", "body": "some body text here Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ipsum eu nunc commodo posuere et sit amet ligula. ", "image": url_for('static', filename='motorv.jpg') },
       #     {"heading": "Industry Focused", "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ipsum eu nunc commodo posuere et sit amet ligula. ", "image": url_for('static', filename='img/89029531.jpeg') }]

    courses = Course.query.order_by(Course.modified.desc()).limit(6).all()
    videos = Video.query.order_by(Video.modified.desc()).limit(2).all()
    posts = Post.query.order_by(Post.modified.desc()).limit(2).all()
    return render_template('main/_index.html',
                            hero=heroObj, 
                            courses= courses,
                            videos=videos,
                            posts=posts)

@main.route('/<slug>')
def page(slug):
    page  = Page.query.filter_by(slug=slug).first()
    courses = Course.query.order_by(Course.modified.desc()).limit(3).all()
    return render_template('main/page.html', page=page, courses=courses)

@main.route('/blog')
def posts():
    posts = Post.query.all() #paginate
    return render_template('main/posts.html', posts=posts)

@main.route('/blog/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    courses = Course.query.order_by(Course.modified.desc()).limit(3).all()
    return render_template('main/post.html', post=post, courses=courses)

@main.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('main/courses.html', courses=courses)

@main.route('/courses/<slug>')
def course(slug):
    course = Course.query.filter_by(slug=slug).first()
    courses = Course.query.order_by(Course.modified.desc()).limit(3).all()
    return render_template('main/course.html', course=course, courses=courses)

@main.route('/gallery')
def gallery():
    page = request.args.get('page', 1, type=int)                                                                
    media = Media.query.order_by(Media.modified.desc()).paginate(page, per_page=20, error_out=False)
  
    return render_template('main/gallery.html', media=media)

 
@main.route('/profile')
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.bio = form.bio.data
    return render_template('main/profile.html')

@main.route('/one')
def temp_1():
    return render_template('one.html')

@main.route('/two')
def temp_2():
    return render_template('two.html')

@main.route('/three')
def temp_3():
    return render_template('three.html')

@main.route('/four')
def temp_4():
    return render_template('four.html')

@main.route('/five')
def temp_5():
    return render_template('five.html')

