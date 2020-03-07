# 3rd Party imports
from flask import Flask
from flask_uploads import patch_request_class #limit fileupload
#import flask_whooshalchemy as wa
# local import
from config import config
from .extensions import db, migrate, login_manager, images, documents, uploads, configure_uploads, mail

def create_app(config_name=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    #register_search(app)

    from .filters import register_filters

    register_filters(app)
    initialize_extentions(app)

    register_blueprints(app)

    return app


def initialize_extentions(app):
    db.init_app(app)
    mail.init_app(app)    
    login_manager.session_protection = 'strong'
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    configure_uploads(app, (images, documents, uploads))
    #limit file upload size
    patch_request_class(app, 32 * 1024 * 1024) #32 Mb

    from .models import User
    migrate.init_app(app, db)


def register_blueprints(app):
    from .bp.main import main
    from .bp.admin import admin
    from .bp.auth import auth
    from .bp.dashboard import dashboard

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

