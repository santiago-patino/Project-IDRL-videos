import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../modelos')
sys.path.append(ruta_modelos)

from flask import Flask, send_from_directory, jsonify
from flask_restful import Api
from vistas import VistaTasks, VistaTask, VistaVideos, VistaVideo
from modelos import db
from os import environ
import os

import json

with open('../config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@35.238.142.44:5432/flask_database'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(app.root_path, config['VIDEOS_FOLDER'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_context = app.app_context()
app_context.push()

db.init_app(app)
    
api = Api(app)
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaVideos, '/api/videos')
api.add_resource(VistaVideo, '/api/video/<int:id_task>')



        
    
        
       