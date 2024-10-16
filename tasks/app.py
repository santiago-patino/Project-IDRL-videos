from flask import Flask, send_from_directory, jsonify
from flask_restful import Api
from vistas import VistaTasks, VistaTask, VistaVideos
from modelos import db
from os import environ
import os

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_database'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(app.root_path, '../videos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_context = app.app_context()
app_context.push()

db.init_app(app)
    
api = Api(app)
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaVideos, '/api/videos')

@app.route('/videos/<int:task_id>/<path:filename>', methods=['GET'])
def uploaded_file(task_id, filename):
    video_directory = os.path.join(app.config['UPLOAD_FOLDER'], str(task_id))
    file_path = os.path.join(video_directory, filename)
    
    if os.path.exists(file_path):
        return send_from_directory(video_directory, filename)
    else:
        # Si el archivo no se encuentra, enviar un mensaje de error
        return jsonify({"mensaje": f"El archivo '{filename}' no se encontró en la tarea '{task_id}'."}), 404



        
    
        
       