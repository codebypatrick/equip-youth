# third party imports
from flask import render_template, request, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_required
import os
import uuid

# local imports
from . import dashboard
from .forms import UserForm, CommonForm, SettingForm, WidgetForm, WidgetItemForm, TagForm, VideoForm, MediaForm
from ...models import User, Page, Course, Setting, Widget, WidgetItem, Post, Tag, Video, Media
from ...extensions import db, uploads

def unique_name():
    return str(uuid.uuid4().hex)[:15]
 
@dashboard.route('/')
def index():
    models = {}
    return render_template('dashboard/index.html', models=models)

@dashboard.route('/users')
def user_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False) 
 
    return render_template('dashboard/user/list.html', users=users)

#@dashboard.route('/users/insert', defaults={'uuid':None}, methods=['GET', 'POST'])
@dashboard.route('/users/edit/<uuid>', methods=['GET', 'POST'])
def user_update(uuid):
    user = User.query.filter_by(uuid=uuid).first() if uuid else None
    form = UserForm(obj = user)
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash('User updated', 'success')
        return redirect(url_for('.user_list'))

    return render_template('dashboard/user/form.html', form=form)

@dashboard.route('/pages', methods=['GET', 'POST'])
def page_list():
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_string = request.form['search']
        pages = Page.query.filter(Page.title.ilike(f"%{search_string}%")).paginate(1, per_page=app.config['PER_PAGE'], error_out=False) 

    else:

        pages = Page.query.order_by(Page.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False) 
    return render_template('dashboard/page/list.html', pages=pages)

@dashboard.route('/pages/search')
def page_search():    
    return render_template('dashboard/page/list.html', pages=results)

@dashboard.route('/pages/insert', defaults={'uuid': None}, methods=['GET', 'POST'])
@dashboard.route('/pages/edit/<uuid>', methods=['GET', 'POST'])
def page_action(uuid):
    page = Page.query.filter_by(uuid=uuid).first() if uuid else None

    form = CommonForm(obj = page)
    tagForm = TagForm()
    if form.validate_on_submit():
        filename = None
        #image uploaded
        if request.files['image']:
            img = request.files['image']
            filename = uploads.save(img, name=unique_name() + '.')

        if uuid is None:
            page_to_add = Page(title=form.title.data, 
                    body=form.body.data, 
                    published=form.published.data,
                    image=filename)
            db.session.add(page_to_add)
            flash('Page Added', 'success')
        else:
            # remove prev image
            if filename and  page.image:
                img_path = uploads.path(page.image)
                os.remove(img_path)
            
            page.image = filename
            page.name = form.title.data
            page.body = form.body.data
            page.published = form.published.data
            flash('Page updated', 'success')
        db.session.commit()
        return redirect(url_for('.page_list'))

    return render_template('dashboard/common_form.html',
            form=form, 
            model='Page',
            data=page,
            tagForm=tagForm)

@dashboard.route('/pages/delete/<uuid>', methods=['GET', 'POST'])
def page_delete(uuid):
    page = Page.query.filter_by(uuid=uuid).first_or_404()
    img_path = None
    if page.image:
        img_path = uploads.path(page.image)
        
    db.session.delete(page)
    db.session.commit()
    # remove img
    if img_path:
        os.remove(img_path)
    flash('Page deleted', 'success')
    return redirect(url_for('.page_list'))

@dashboard.route('/courses')
def course_list():
    page = request.args.get('page', 1, type=int)                                                                
    courses = Course.query.order_by(Course.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
    return render_template('dashboard/course/list.html', courses=courses)

@dashboard.route('/courses/insert', defaults={'uuid': None}, methods=['GET', 'POST'])
@dashboard.route('/courses/edit/<uuid>', methods=['GET', 'POST'])
def course_action(uuid):
    course = Course.query.filter_by(uuid=uuid).first() if uuid else None
    form = CommonForm(obj = course)
    tagForm = TagForm()
    if form.validate_on_submit():
        filename=None
        #image uploaded
        if request.files['image']:
            img = request.files['image']
            filename = uploads.save(img, name=unique_name() + '.')

        if uuid is None:
            course = Course(title=form.title.data,
                    body=form.body.data,
                    published=form.published.data,
                    image=filename)
            db.session.add(course)
            flash('Course Added', 'success')
        else:
            if filename and course.image:
                img_path = uploads.path(course.image)
                os.remove(img_path)
                
            if filename:
                course.image=filename
            course.title = form.title.data
            course.body= form.body.data
            course.published = form.published.data
                        
        db.session.commit()
        return redirect(url_for('.course_list'))
    return render_template('dashboard/common_form.html', form=form, model="Course", data=course, tagForm=tagForm)

@dashboard.route('/courses/delete/<uuid>', methods=['GET', 'POST'])
def course_delete(uuid):
    course = Course.query.filter_by(uuid=uuid).first()
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted', 'success')
    return redirect(url_for('.course_list'))

@dashboard.route('/posts')
def post_list():
    page = request.args.get('page', 1, type=int)                                                                
    posts = Post.query.order_by(Post.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
 
    return render_template('dashboard/post/list.html', posts=posts)


@dashboard.route('/posts/insert', defaults={'uuid': None}, methods=['GET', 'POST'])
@dashboard.route('/posts/edit/<uuid>', methods=['GET', 'POST'])
def post_action(uuid):
    post = Post.query.filter_by(uuid=uuid).first() if uuid else None
    
    form = CommonForm(obj = post)
    tagForm = TagForm()
    if form.validate_on_submit():
        filename = None
        
        #image uploaded
        if request.files['image']:
            img = request.files['image']
            filename = uploads.save(img, name=unique_name() + '.')

        if uuid is None:
            post_to_add = Post(title=form.title.data, 
                    body=form.body.data, 
                    published=form.published.data,
                    image=filename)
           
            db.session.add(post_to_add)
            flash('Post Added', 'success')
        else:
            # remove prev image
            if filename and  post.image:
                img_path = uploads.path(post.image)
                os.remove(img_path)
            
            post.image = filename
            post.title = form.title.data
            post.body = form.body.data
            post.published = form.published.data
            flash('Post updated', 'success')
        db.session.commit()
        return redirect(url_for('.post_list'))
    return render_template('dashboard/common_form.html', form=form, model='Post', data=post, tagForm=tagForm)

@dashboard.route('/posts/<uuid>')
def post_show(uuid):
    post = Post.query.filter_by(uuid=uuid).first()
    tagForm = TagForm()

    return render_template('dashboard/post/show.html', post=post)

@dashboard.route('/posts/tag/<uuid>', methods=['GET', 'POST'])
def post_tag(uuid):
    post = Post.query.filter_by(uuid=uuid).first()
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(title=form.title.data)
        post.tags.append(tag)
        db.session.add(tag)
        db.session.commit()
        flash('Tag created', 'success')
        
    return redirect(url_for('.post_action', uuid=uuid))

@dashboard.route('/posts/delete/<uuid>', methods=['GET', 'POST'])
def post_delete(uuid):
    post = Post.query.filter_by(uuid=uuid).first_or_404()
    if post.image:
        img_path = uploads.path(post.image)
        
    db.session.delete(post)
    db.session.commit()
    # remove img
    if img_path:
        os.remove(img_path)
    flash('Post deleted', 'success')
    return redirect(url_for('.page_list'))

@dashboard.route('/gallery')
def media_list():
    page = request.args.get('page', 1, type=int)                                                                
    media = Media.query.order_by(Media.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
  
    return render_template('dashboard/media/list.html', media=media)

@dashboard.route('/gallery/insert', defaults={'uuid':None}, methods=['GET', 'POST'])
@dashboard.route('/gallery/edit/<uuid>', methods=['GET', 'POST'])
def media_action(uuid):
    media = Media.query.filter_by(uuid=uuid).first()
    form = MediaForm(obj=media)
    if form.validate_on_submit():
        filename = None
        
        #image uploaded
        if request.files['image']:
            img = request.files['image']
            filename = uploads.save(img, name=unique_name() + '.')

        if uuid is None:
            media = Media(name=form.name.data, filename=filename)
            db.session.add(media)
            flash('Media Added', 'success')
        else:
            # remove prev image
            if filename and  media.filename:
                img_path = uploads.path(media.filename)
                os.remove(img_path)
            
            if filename:
                media.filename = filename
            media.name= form.name.data
            flash('Media updated', 'success')
        db.session.commit()
        return redirect(url_for('.media_list'))
    return render_template('dashboard/media/form.html', form=form)

@dashboard.route('/gallery/delete/<uuid>', methods=['GET', 'POST'])
def media_delete(uuid):
    media = Media.query.filter_by(uuid=uuid).first()
    if post.image:
        img_path = uploads.path(media.filename)
    db.session.delete(media)
    db.session.commit()
    if img_path:
        os.remove(img_path)
    return redirect(url_for('.media_list'))


@dashboard.route('/videos')
def video_list():
    page = request.args.get('page', 1, type=int)                                                                
    videos = Video.query.order_by(Video.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
  
    return render_template('dashboard/video/list.html', videos=videos)

@dashboard.route('/videos/insert', defaults={'uuid':None}, methods=['GET', 'POST'])
@dashboard.route('/videos/edit/<uuid>', methods=['GET', 'POST'])
def video_action(uuid):
    video = Video.query.filter_by(uuid=uuid).first()
    form = VideoForm(obj=video)
    if form.validate_on_submit():
        if uuid is None:
            video = Video(youtube_id=form.youtube_id.data)
            db.session.add(video)
            flash('Video Added', 'success')
        else:
            video.youtube_id = form.youtube_id.data
            flash('Video updated', 'success')
        db.session.commit()
        return redirect(url_for('.video_list'))
    return render_template('dashboard/video/form.html', form=form)

@dashboard.route('/videos/delete/<uuid>', methods=['GET', 'POST'])
def video_delete(uuid):
    video = Video.query.filter_by(uuid=uuid).first()
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('.video_list'))


@dashboard.route('/settings')
def setting_list():
    page = request.args.get('page', 1, type=int)                                                                
    settings = Setting.query.order_by(Setting.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
  
    return render_template('dashboard/setting/list.html', settings=settings)

@dashboard.route('/settings/insert', defaults={'uuid':None}, methods=['GET', 'POST'])
@dashboard.route('/settings/edit/<uuid>', methods=['GET', 'POST'])
def setting_action(uuid):
    setting = Setting.query.filter_by(uuid=uuid).first()
    form = SettingForm(obj=setting)
    if form.validate_on_submit():
        if uuid is None:
            setting = Setting(name=form.name.data, value=form.value.data)
            db.session.add(setting)
            flash('Setting Added', 'success')
        else:
            setting.name = form.name.data
            setting.value = form.value.data
            flash('Setting updated', 'success')
        db.session.commit()
        return redirect(url_for('.setting_list'))
    return render_template('dashboard/setting/form.html', form=form)

@dashboard.route('/settings/delete/<uuid>', methods=['GET', 'POST'])
def setting_delete(uuid):
    setting = Setting.query.filter_by(uuid=uuid).first()
    db.session.delete(setting)
    db.session.commit()
    return redirect(url_for('.setting_list'))

@dashboard.route('/widgets')
def widget_list():
    page = request.args.get('page', 1, type=int)                                                                
    widgets = Widget.query.order_by(Widget.modified.desc()).paginate(page, per_page=app.config['PER_PAGE'], error_out=False)
    return render_template('dashboard/widget/list.html', widgets=widgets)

@dashboard.route('/widgets/insert', defaults={'uuid': None}, methods=['GET', 'POST'])
@dashboard.route('/widgets/edit/<uuid>', methods=['GET', 'POST'])
def widget_action(uuid):
    widget = Widget.query.filter_by(uuid=uuid).first() if uuid else None
    form = WidgetForm(obj = widget)
    if form.validate_on_submit():
        if uuid is None:
            widget = Widget(name=form.name.data)
            db.session.add(widget)
            flash('Widget added', 'success')
        else:
            widget.name = form.name.data
            flash('Widget Updated', 'succcess')
        db.session.commit()
        return redirect(url_for('.widget_list'))
    
    return render_template('dashboard/widget/form.html', form=form, widget=widget)

@dashboard.route('/widgets/items/insert/<uuid>', methods=['GET', 'POST'])
def widget_item(uuid):
    widget = Widget.query.filter_by(uuid=uuid).first()
    
    form = WidgetItemForm()
    if form.validate_on_submit():
        filename = None
        #image uploaded
        if request.files['image']:
            img = request.files['image']
            filename = uploads.save(img, name=unique_name() + '.')


        widgetItem = WidgetItem(heading=form.heading.data,
                body=form.body.data,
                tagline=form.tagline.data,
                image = filename,
                action=form.action.data,
                action_url=form.action_url.data,
                widget_id=widget.id)
        db.session.add(widgetItem)
        db.session.commit()
        flash('Item Added', 'success')
        return redirect(url_for('.widget_action', uuid=uuid))
    return render_template('dashboard/widget/item.html', form=form)

@dashboard.route('/widgets/delete/<uuid>', methods=['GET', 'POST'])
def widget_delete(uuid):
    widget = Widget.query.filter_by(uuid=uuid).first()
    db.session.delete(widget)
    db.session.commit()
    flash('Widget Deleted', 'success')
    return redirect(url_for('.widget_list'))

@dashboard.route('/widget-items/<uuid>', methods=['GET', 'POST'])
def widget_item_edit(uuid):
    widget_item = WidgetItem.query.filter_by(uuid=uuid).first()
    widget = Widget.query.get(widget_item.widget_id)
    form = WidgetItemForm(obj = widget_item)
    if form.validate_on_submit():
        filename = None
        #image uploaded
        if request.files['image']:
            img = request.files['image']
            filename = uploads.save(img, name=unique_name() + '.')

        # remove prev image
        if filename and  widget_item.image:
                img_path = uploads.path(post.image)
                os.remove(img_path)
        if filename:
            widget_item.image = filename
        
 
        widget_item.heading = form.heading.data
        widget_item.body = form.body.data
        widget_item.tagline = form.tagline.data
        widget_item.action= form.action.data
        widget_item.action_url = form.action_url.data
        db.session.commit()
        flash('Item updated', 'success')
        return redirect(url_for('.widget_action', uuid=widget.uuid))
    return render_template('dashboard/widget/item.html', form=form)

@dashboard.route('/widget-item/delete/<uuid>', methods=['GET', 'POST'])
def widget_item_delete(uuid):
    widget_item = WidgetItem.query.filter_by(uuid=uuid).first()
    widget = Widget.query.get(widget_item.widget_id)
    db.session.delete(widget_item)
    db.session.commit()
    flash('Item Deleted', 'success')
    return redirect(url_for('.widget_action', uuid=widget.uuid))


