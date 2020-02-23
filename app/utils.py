# 3rd party imports
import uuid
import os
from flask import current_app, url_for

# local
from .extensions import images, documents

#def unique_id():
#    return hex(uuid.uuid4().time)[2:-1]
#
def upload_image(_file):
    random_name = str(uuid.uuid4().hex)[:8]
    filename = images.save(_file, name=f"{random_name}.")
    url = url_for('static', filename=f"img/{filename}", _external=True)
    path = os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], filename)  
    return filename, url, path

def upload_document(_file):
    random_name = str(uuid.uuid4().hex)[:8]
    filename = documents.save(_file, name=f"{random_name}.")
    url = url_for('static', filename=f"docs/{filename}", _external=True)
    path = os.path.join(current_app.config['UPLOADED_DOCUMENTS_DEST'], filename)  
    return filename, url, path 


