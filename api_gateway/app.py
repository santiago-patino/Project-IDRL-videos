import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../modelos')
sys.path.append(ruta_modelos)

from flask import Flask
from flask_restful import Api
from vistas import VistaRegistro, VistaLogin, VistaTasks, VistaTask, VistaVideos
from flask_jwt_extended import JWTManager
from datetime import timedelta

from modelos import db
from os import environ

import json

with open('../config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@35.238.142.44:5432/flask_database'
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY']='frase-secreta'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['PROPAGATE_EXCEPTIONS'] = True


app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaRegistro, '/api/auth/signup')
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaVideos, '/api/videos')

jwt = JWTManager(app)
    
    

        
    
        
       