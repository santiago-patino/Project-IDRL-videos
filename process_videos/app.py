import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../modelos')
sys.path.append(ruta_modelos)

from flask import Flask
from modelos import db
from os import environ
from dotenv import load_dotenv
import threading

from tareas import iniciar_suscripcion

load_dotenv()

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@flask_db:5432/flask_database"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()
db.init_app(app)
iniciar_suscripcion(app_context)

# def iniciar_suscriptor():
#     app_context = app.app_context()
#     app_context.push()
#     db.init_app(app)
    
#     iniciar_suscripcion(app_context)
    
    #thread = threading.Thread(target=iniciar_suscripcion, args=(app_context,))
    #thread.start()

#db.init_app(app)

#iniciar_suscriptor()








        
    
        
       