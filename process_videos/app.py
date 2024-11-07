from flask import Flask
#from modelos import db
from os import environ
import os

from dotenv import load_dotenv

from tareas import listen_to_pubsub

load_dotenv()

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    
    # Cargar configuración desde las variables de entorno o archivo .env
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa aquí cualquier extensión de Flask, si es necesario
    # db.init_app(app)

    return app

#app_context = app.app_context()
#app_context.push()

app = create_app()

with app.app_context():
    listen_to_pubsub()

#db.init_app(app)






        
    
        
       