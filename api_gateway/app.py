import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../modelos')
sys.path.append(ruta_modelos)

from flask import Flask
from flask_restful import Api
from vistas import VistaRegistro, VistaLogin, VistaTasks, VistaTask, VistaVideos, VistaWorkers, VistaVideo
from flask_jwt_extended import JWTManager
from datetime import timedelta

from modelos import db
from os import environ

from dotenv import load_dotenv

    
load_dotenv()

#print(os.environ.get('DB_URL'))

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@flask_db:5432/flask_database"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
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
api.add_resource(VistaWorkers, '/api/workers')
api.add_resource(VistaVideo, '/api/video/<int:id_task>')

jwt = JWTManager(app)
    
    

        
    
        
       