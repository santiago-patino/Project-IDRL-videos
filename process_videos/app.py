from flask import Flask
from modelos import db
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(app.root_path, '../videos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_context = app.app_context()
app_context.push()

db.init_app(app)






        
    
        
       