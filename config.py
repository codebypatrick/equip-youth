import os

# Define application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10
    
    UPLOADED_IMAGES_DEST =  BASE_DIR + '/app/static/img/'
    UPLOADED_DOCUMENTS_DEST = BASE_DIR + '/app/static/docs'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    #MAIL_USERNAME = os.environ['APP_MAIL_USERNAME'] 
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']


    #MAIL_DEFAULT_SENDER = os.environ['APP_MAIL_SENDER'] 


    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SECRET_KEY = 's3cr3t'
    SECURITY_SALT = 's3cr3t-salt'
   

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,

        'default': DevelopmentConfig
        }
