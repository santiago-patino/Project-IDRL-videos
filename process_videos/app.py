from flask import Flask
from modelos import db
from os import environ
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@flask_db:5432/flask_database"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)






        
    
        
       