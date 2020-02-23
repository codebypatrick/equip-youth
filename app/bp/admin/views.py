# third party imports
from flask import render_template, request, redirect, url_for, flash, current_app, session, jsonify
from flask_login import login_required, current_user
import os
import uuid
import json

# local imports
from . import admin
from .forms import UserForm, UserEditForm, PageForm, CourseForm, ImageUploadForm, DocumentUploadForm, SettingForm, WidgetForm, WidgetItemForm
from ...models import db, User, Page, Course, Media, Setting, Widget, WidgetItem
#from ...extensions import uploaded_images
from ...utils import upload_image, upload_document

PER_PAGE = 10

@admin.route('/')
@login_required
def index():
    user_count = User.query.count()
    page_count = Page.query.count()
    course_count = Course.query.count()
    return render_template('admin/index.html', 
                            user_count=user_count,
                            page_count = page_count,
                            course_count = course_count)

@admin.route('/users', methods=['GET', 'POST'])
@login_required
def user_list():
    if request.method == 'POST':
        items = request.form.getlist('user_id')
        print(items)
        if items:
            deleted_items = User.__table__.delete().where(User.uuid.in_(items))
            db.session.execute(deleted_items)
            db.session.commit()
            flash('{} user(s) deleted!'.format(len(items)), 'success')

    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.modified.desc()).paginate(page, per_page=PER_PAGE, error_out=False) 
    return render_template('admin/user/list.html', users=users)

@admin.route('/users/new', methods=['GET', 'POST'])
@login_required
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user =  User(email=form.email.data, 
                username=form.username.data,
                password='123', 
                full_name=form.full_name.data,
                role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('user Added', 'success')
        return redirect(url_for('.user_list'))

    return render_template('admin/user/form.html', form=form, action='New')


@admin.route('/users/<uuid>', methods=['GET', 'POST'])
@login_required
def user_update(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    form = UserEditForm()
    if form.validate_on_submit():
        user.full_name = form.full_name.data
        db.session.commit()
        flash('{} updated'.format(user.username), 'success')
        return redirect(url_for('.user_list'))

    return render_template('admin/user/update.html', form=form, user=user)

@admin.route('/pages', methods=['GET', 'POST'])
@login_required
def page_list():
    if request.method == 'POST':
        items = request.form.getlist('page_id')
        print(items)
        if items:
            deleted_items = Page.__table__.delete().where(Page.uuid.in_(items))
            db.session.execute(deleted_items)
            db.session.commit()
            flash('{} user(s) deleted!'.format(len(items)), 'success')

    page = request.args.get('page', 1, type=int)
    pages = Page.query.order_by(Page.modified.desc()).paginate(page, per_page=PER_PAGE, error_out=False) 
    return render_template('admin/page/list.html', pages=pages)


@admin.route('/pages/new', methods=['GET', 'POST'])
@login_required
def page_create():
    form = PageForm()
    if form.validate_on_submit():
        page = Page(name=form.name.data,lead=form.lead.data, body=form.body.data, published=form.published.data,  author=current_user)
        db.session.add(page)
        db.session.commit()
        flash('Page created', 'success')
        return redirect(url_for('.page_list'))

    return render_template('admin/page/form.html', form=form, action='New')

@admin.route('/pages/<uuid>/edit', methods=['GET', 'POST'])
@login_required
def page_update(uuid):
    form = PageForm()
    page = Page.query.filter_by(uuid=uuid).first()
    if form.validate_on_submit():
        page.name = form.name.data
        page.body = form.body.data
        page.lead = form.lead.data
        page.published = form.published.data
        page.author = current_user
        db.session.commit()
        flash('Page updated', 'success')
        return redirect(url_for('.page_list'))

    return render_template('admin/page/form.html', form=form, page=page, action='Edit')

@admin.route('/pages/<uuid>/media/image', methods=['GET', 'POST'])
def page_image_create(uuid):
    form = ImageUploadForm()
    page = Page.query.filter_by(uuid=uuid).first()
    if form.validate_on_submit():  
        filename, url, path = upload_image(request.files['media'])
        
        media = Media(name=form.name.data, media_type='image', filename=filename, url=url, path=path, page=page)
       
        db.session.add(media)
        db.session.commit()
        flash('Media added', 'success')

    return render_template('admin/page/media.html', form=form, page=page)

@admin.route('/pages/<uuid>/media/docs', methods=['GET', 'POST'])
def page_docs_create(uuid):
    form = DocumentUploadForm()
    page = Page.query.filter_by(uuid=uuid).first()
    if form.validate_on_submit():  
        filename, url, path = upload_document(request.files['media'])
               
        media = Media(name=form.name.data, media_type='document', filename=filename, url=url,path=path, page=page)
       
        db.session.add(media)
        db.session.commit()
        flash('Media added', 'success')

    return render_template('admin/page/media.html', form=form, page=page)

@admin.route('/courses', methods=['GET', 'POST'])
@login_required
def course_list():
    if request.method == 'POST':
        items = request.form.getlist('course_id')
        if items:
            deleted_items = Course.__table__.delete().where(Course.uuid.in_(items))
            db.session.execute(deleted_items)
            db.session.commit()
            flash('{} course(s) deleted!'.format(len(items)), 'success')

    page = request.args.get('page', 1, type=int)
    courses = Course.query.order_by(Course.modified.desc()).paginate(page, per_page=PER_PAGE, error_out=False) 
    return render_template('admin/course/list.html', courses=courses)


@admin.route('/courses/new', methods=['GET', 'POST'])
@login_required
def course_create():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data,lead=form.lead.data, body=form.body.data, description=form.description.data, creator=current_user)
        db.session.add(course)
        db.session.commit()
        flash('Course created', 'success')
        return redirect(url_for('.course_list'))

    return render_template('admin/course/form.html', form=form, action='New')

@admin.route('/courses/<uuid>/edit', methods=['GET', 'POST'])
@login_required
def course_update(uuid):
    form = CourseForm()
    course = Course.query.filter_by(uuid=uuid).first()
    if form.validate_on_submit():
        course.name = form.name.data
        course.body = form.body.data
        course.lead = form.lead.data
        course.description = form.description.data
        course.creator = current_user
        db.session.commit()
        flash('Course updated', 'success')
        return redirect(url_for('.course_list'))

    return render_template('admin/course/form.html', form=form, course=course, action='Edit')

@admin.route('/courses/<uuid>/media/image', methods=['GET', 'POST'])
def course_image_create(uuid):
    form = ImageUploadForm()
    course = Course.query.filter_by(uuid=uuid).first()
    if form.validate_on_submit():  
        filename, url, path = upload_image(request.files['media'])
        
        media = Media(name=form.name.data, media_type='image', filename=filename, url=url, path=path, course=course)
       
        db.session.add(media)
        db.session.commit()
        flash('Media added', 'success')

    return render_template('admin/course/media.html', form=form, course=course)

@admin.route('/courses/<uuid>/media/docs', methods=['GET', 'POST'])
def course_docs_create(uuid):
    form = DocumentUploadForm()
    course = Course.query.filter_by(uuid=uuid).first()
    if form.validate_on_submit():  
        filename, url, path = upload_document(request.files['media'])
               
        media = Media(name=form.name.data, media_type='document', filename=filename, url=url,path=path, course=course)
       
        db.session.add(media)
        db.session.commit()
        flash('Media added', 'success')

    return render_template('admin/course/media.html', form=form, course=course)


@admin.route('/media', methods=['GET', 'POST'])
@login_required
def media_list():
    page = request.args.get('page', 1, type=int)
    media = Media.query.order_by(Media.modified.desc()).paginate(page, per_page=PER_PAGE, error_out=False) 
    return render_template('admin/media/list.html', media=media)


@admin.route('/media/delete', methods=['POST'])
@login_required
def media_delete():
    items = request.form.getlist('media_id')
    _deleted = []
    for m in items:
        media = Media.query.filter_by(uuid=m).first()
        db.session.delete(media)
        # add to list to delete from server
        if media.path:
            _deleted.append(media.path)

        
    # delete from server
    for d in _deleted:
        os.remove(d)

    db.session.commit()

    return redirect(request.form['back'])

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def setting_list():
    if request.method == 'POST':
        items = request.form.getlist('setting_id')
        print(items)
        if items:
            deleted_items = Setting.__table__.delete().where(Setting.uuid.in_(items))
            db.session.execute(deleted_items)
            db.session.commit()
            flash('{} setting(s) deleted!'.format(len(items)), 'success')

    page = request.args.get('page', 1, type=int)
    settings = Setting.query.order_by(Setting.modified.desc()).paginate(page, per_page=PER_PAGE, error_out=False) 
    return render_template('admin/setting/list.html', settings=settings)

@admin.route('/settings/main')
@login_required
def setting_main():
    return render_template('admin/setting/main.html')

@admin.route('/settings/new', methods=['GET', 'POST'])
@login_required
def setting_create():
    form = SettingForm()
    session['back'] = url_for('.setting_create')
    if form.validate_on_submit():
        setting =  Setting(name=form.name.data, 
                value=form.value.data,
                min_value=form.min_value.data, 
                max_value=form.max_value.data
                )
        db.session.add(setting)
        db.session.commit()
        flash('Setting', 'success')
        return redirect(url_for('.setting_list'))
    if 'back' in session:
        session.pop('back')

    if 'json_obj' in session:
        session.pop('json_obj')

    if 'json_list' in session:
        session.pop('json_list')
    
    return render_template('admin/setting/form.html', form=form, action='New')

@admin.route('/settings/<uuid>', methods=['GET', 'POST'])
@login_required
def setting_update(uuid):
    setting = Setting.query.filter_by(uuid=uuid).first()
    form = SettingForm()
    if form.validate_on_submit():
        setting.value = form.value.data
        setting.name = form.name.data
        setting.min_value= form.min_value.data
        setting.max_value.data
        db.session.commit()
        flash('{} updated'.format(setting.name), 'success')
        return redirect(url_for('.setting_list'))

    return render_template('admin/setting/form.html', form=form, setting=setting, action='Edit')


@admin.route('/setting/navigation', methods=['GET', 'POST'])
@login_required
def setting_navigation():
   
    setting = Setting.query.filter_by(name='navigation').first()
    if request.method == 'POST':
        if request.form['navigation']:
            setting.value= request.form['navigation']
            flash('Navigation settings upddated', 'success')
            db.session.commit()

    return render_template('admin/setting/navigation.html', setting=setting)

@admin.route('/settings/hero', methods=['GET', 'POST'])
@login_required
def setting_hero():
    # get setting
    setting = Setting.query.filter_by(name='widget_hero').first()
    if request.method == 'POST':
        if request.form['hero']:
            setting.value= request.form['hero']
            flash('Hero settings upddated', 'success')
            db.session.commit()

    return render_template('admin/setting/hero.html', setting=setting)

@admin.route('/settings/intro', methods=['GET', 'POST'])
@login_required
def setting_intro():
    # get setting
    setting = Setting.query.filter_by(name='widget_intro').first()
    if request.method == 'POST':
        if request.form['intro']:
            setting.value= request.form['intro']
            flash('Intro settings upddated', 'success')
            db.session.commit()

 
    return render_template('admin/setting/intro.html', setting=setting)

@admin.route('/setting/feature', methods=['GET', 'POST'])
@login_required
def setting_feature():
    # get setting
    setting = Setting.query.filter_by(name='widget_features').first()
    if request.method == 'POST':
        if request.form['features']:
            setting.value= request.form['features']
            flash('Features settings upddated', 'success')
            db.session.commit()

 
    return render_template('admin/setting/feature.html', setting=setting)

@admin.route('/setting/feature/delete', methods=['GET', 'POST'])
@login_required
def setting_feature_delete():
    setting = Setting.query.filter_by(name='features').first()
    print(setting.value)
    db_nav = json.loads(setting.value)

    items = request.form.getlist('setting_id')
    print(db_nav)
    
    for i in items:
        
        for d in db_nav:
            print(d)
            if db_nav[d]['heading']:
                del db_nav[d]
                break

    setting.value = json.dumps(db_nav)
    db.session.commit() 
    return redirect(url_for('.setting_feature'))
    # create dict
    return render_template('admin/setting/navigation.html', db_nav=db_nav)

@admin.route('/setting/marketing', methods=['GET', 'POST'])
@login_required
def setting_marketing():
    # get setting
    setting = Setting.query.filter_by(name='marketing').first()
    if setting is None:
         _features = []
    else:
        _features = json.loads(setting.value)

    if request.method == 'POST':
        if request.files['image']:
            filename, url, path = upload_image(request.files['image'])

        heading = request.form['heading']
        body = request.form['body']
        link = request.form['link']
        data = {'heading': heading, 'body':body,'link': link, 'image': url, 'path': path}
        _features.append(data)
        if setting:
            setting.value = json.dumps(_features)
        else:
            setting = Setting(name='marketing', value=json.dumps(_features))
            db.session.add(setting)
        db.session.commit()

    # create dict
    return render_template('admin/setting/feature.html', features=_features)

@admin.route('/setting/feature/delete', methods=['GET', 'POST'])
@login_required
def setting_marketing_delete():
    setting = Setting.query.filter_by(name='marketing').first()
    if setting is None:
         db_nav = []
    else:
        db_nav = json.loads(setting.value)

    items = request.form.getlist('setting_id')
    
    for i in items:
        for d in range(len(db_nav)):
            if db_nav[d]['label']:
                del db_nav[d]
                break

    setting.value = json.dumps(db_nav)
    db.session.commit() 
    return redirect(url_for('.setting_marketing'))
    # create dict
    return render_template('admin/setting/feature.html', db_nav=db_nav)

@admin.route('/settings/json', methods=['GET', 'POST'])
def setting_json():
    schema = {} #schema
    fields= ''
    form = {}
    data = ''
    _list = []
    back= ''
    if request.args.get('from') == 'New':
        back = url_for('.setting_create')

    if request.args.get('from') == 'Edit' and request.args.get('id'):
        back = url_for('.setting_update', uuid=request.args.get('id'))
        
    #redirect_url = ''

    if 'json_obj' in session:
        schema = json.loads(session['json_obj'])

    if 'json_list' in session:
        # create list of session vars
        data = json.loads(session['json_list'])
    #if 'back' in session:
        #redirect_url = session['back']
     

    # create form from schema
    if schema:
        
        for k in schema:
            if k == 'attachment':
                fields += f'''\
                        <div class='mb-4'>\
                        <input  type="file" name="{k}">\
                        </div>'''
            else:
                fields += f'''\
                <div class="mb-4">\
                <input type="text" name="{k}" placeholder="{k}" class="field"/>\
                </div>'''         

    if request.method == 'POST':
        # create schema
        key = request.form['key']
         
        if key:
            schema[key]= ''
            session['json_obj'] = json.dumps(schema)
            return redirect(request.url)
        
        if request.files:
            for k,v in request.files.items():
                _file = request.files[k]
                if _file.filename:
                    filename, url, path = upload_document(request.files[k])
                    form[k] = {}
                    form[k]['url'] = url
                    form[k]['path'] = path
        
        if request.form:
            for k,v in request.form.items():
                if v:
                    form[k] = request.form[k]
        
        #check if form not empty
        if len(form.keys()) > 0:
            if not 'json_list' in session:
                # list empty create dict
                session['json_list'] = json.dumps(form)

            else:
                old = []
                # check if dict and add to list
                if type(data) is dict:
                    old.append(data)
                else:
                    old = data

                _list.append(form)
                session['json_list'] = json.dumps(old + _list)    
                data = json.dumps(session['json_list'])
            
        
        return redirect(request.url)
               
    return render_template('admin/setting/json.html', schema=schema, fields=fields, data=data, back=back)

@admin.route('/settings/json/clear')
def setting_json_clear():

    if 'json_obj' in session:
        session.pop('json_obj')

    if 'json_list' in session:
        session.pop('json_list')
    
    return redirect(url_for('.setting_json'))

@admin.route('/settings/builder')
def setting_builder():
    return render_template('admin/setting/builder.html')
   
@admin.route('/delete/file', methods=['POST'])
def delete_file():
    #
    if request.method == 'POST':
        if request.form['path']:
            os.remove(request.form['path'])
            
    return jsonify({'message': 'file deleted'})

@admin.route('/upload', methods=['GET', 'POST'])
def upload():
    #
    if request.method == 'POST':
        if request.files['file']:
            filename, url, path = upload_document(request.files['file'])
    return jsonify({'url': url, 'path': path})

@admin.route('/widgets', methods=['GET', 'POST'])
def widget_list():
    if request.method == 'POST':
        items = request.form.getlist('widget_id')
        if items:
            deleted_items = Widget.__table__.delete().where(Widget.uuid.in_(items))
            db.session.execute(deleted_items)
            db.session.commit()
            flash('{} widget(s) deleted!'.format(len(items)), 'success')

    page = request.args.get('page', 1, type=int)
    widgets = Widget.query.order_by(Widget.modified.desc()).paginate(page, per_page=PER_PAGE, error_out=False) 
    return render_template('admin/widget/list.html', widgets=widgets)

@admin.route('/widgets/new', methods=['GET', 'POST'])
def widget_create():
    form = WidgetForm()
    if form.validate_on_submit():
        widget = Widget(name=form.name.data)
        db.session.add(widget)
        db.session.commit()
        flash('Widget created', 'success')
        return redirect(url_for('.widget_list'))
    return render_template('/admin/widget/form.html', form=form)

@admin.route('/widget/<uuid>', methods=['GET', 'POST'])
def widget_update(uuid):
    widget = Widget.query.filter_by(uuid=uuid).first()
    form = WidgetForm()
    if form.validate_on_submit():
        widget.name = form.name.data
        db.session.commit()
        flash('Widget updated', 'success')
        return redirect(url_for('.widget_list'))
    
    return render_template('/admin/widget/form.html', form=form, widget=widget)

@admin.route('/widget/<uuid>/items', methods=['GET', 'POST'])
def widget_items(uuid):
    widget = Widget.query.filter_by(uuid=uuid).first()
    if request.method == 'POST':
        items = request.form.getlist('widget_item_id')
        if items:
            for i in items:
                #get item
                widget_item = WidgetItem.query.filter_by(uuid=i).first()
                #remove any images
                if widget_item.image_path:
                    os.remove(widget_item.image_path)

            deleted_items = WidgetItem.__table__.delete().where(WidgetItem.uuid.in_(items))
            db.session.execute(deleted_items)
            db.session.commit()
            flash('{} widget(s) deleted!'.format(len(items)), 'success')
            return redirect(request.url)

    return render_template('/admin/widget/item/list.html', widget=widget)

@admin.route('/widget-item/<uuid>/create', methods=['GET', 'POST'])
def widget_item_create(uuid):
    widget = Widget.query.filter_by(uuid=uuid).first()
    form = WidgetItemForm()
    if form.validate_on_submit():
        widget_item = WidgetItem(heading=form.heading.data, 
                body= form.body.data,
                tagline=form.tagline.data,
                action=form.action.data,
                action_url=form.action_url.data,
                widget_id=widget.id)
        
        if request.files['image']:
            filename, url, path = upload_image(request.files['image'])
            widget_item.image_url = url
            widget_item.image_path = path

        db.session.add(widget_item)
        db.session.commit()
        flash('Item added', 'success')
        return redirect(url_for('.widget_items', uuid=widget.uuid))

    return render_template('/admin/widget/item/form.html', form=form, item='')

@admin.route('/widget-item/<uuid>/edit', methods=['GET', 'POST'])
def widget_item_update(uuid):
    widget_item = WidgetItem.query.filter_by(uuid=uuid).first()
    form = WidgetItemForm()
    if form.validate_on_submit():
        widget_item.heading = form.heading.data
        widget_item.body = form.body.data
        widget_item.tagline = form.tagline.data
        widget_item.action = form.action.data
        widget_item.action_url = form.action_url.data

        if request.files['image']:
            #old_image = widget_item.image_path
            filename, url, path = upload_image(request.files['image'])
            widget_item.image_url = url
            widget_item.image_path = path
            #os.remove(old_image)

        flash('Item updated', 'success')
        return redirect(url_for('.widget_items', uuid=uuid))
    return render_template('/admin/widget/item/form.html', form=form, item=widget_item)
