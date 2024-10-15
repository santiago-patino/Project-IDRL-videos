from flask import Flask, send_from_directory
from flask_restful import Api
from vistas import VistaTasks
from modelos import db
from os import environ
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_database'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(app.root_path, 'videos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_context = app.app_context()
app_context.push()

db.init_app(app)
    
api = Api(app)
api.add_resource(VistaTasks, '/api/tasks')

@app.route('/videos/<int:task_id>/<path:filename>', methods=['GET'])
def uploaded_file(task_id, filename):
    print()
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(task_id)), filename)



        
    
        
       