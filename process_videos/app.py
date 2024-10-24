from flask import Flask
from modelos import db
from os import environ
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(app.root_path, environ.get('VIDEOS_FOLDER'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_context = app.app_context()
app_context.push()

db.init_app(app)






        
    
        
       