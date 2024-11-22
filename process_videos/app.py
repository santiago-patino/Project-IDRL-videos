import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../modelos')
sys.path.append(ruta_modelos)

from flask import Flask, request, jsonify
from flask_restful import Api
from modelos import db
from os import environ
from dotenv import load_dotenv
import threading
import base64

#from tareas import editar_video

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()
db.init_app(app)
# thread = threading.Thread(target=iniciar_suscripcion, args=(app_context,))
# thread.start()

@app.route('/process-message', methods=['POST'])
def process_message():
    message = request.get_json()
    print("Mensaje recibido:", message)
    encoded_data = message['message']['data']
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    print(decoded_data)
    #editar_video(int(message))
    return jsonify({'status': 'Message processed'}), 200










        
    
        
       