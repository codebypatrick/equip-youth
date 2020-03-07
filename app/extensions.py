# 3rd party imports
from flask_sqlalchemy import SQLAlchemy
#from flask_msearch import Search
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL, AllExcept, SCRIPTS, AUDIO, EXECUTABLES

db = SQLAlchemy()
#search = Search()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
images = UploadSet('images', IMAGES)
documents = UploadSet('documents', ALL) #filter out allowed docs
uploads = UploadSet('uploads', AllExcept(SCRIPTS + EXECUTABLES + AUDIO))
