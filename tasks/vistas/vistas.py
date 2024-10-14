from flask import request, current_app
from modelos import db, User, Task
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
#from app import app
from werkzeug.utils import secure_filename
    
class VistaTasks(Resource):
    
    def post(self): 
       
       current_user = request.form.get('current_user')
       
       new_task = Task(
           user=current_user,
           status='uploaded',
       )
       
       db.session.add(new_task)
       db.session.commit()
       
       file = request.files['file']
       print(request.files)
       if file:

            # Crear el directorio para guardar el archivo, si no existe
            upload_directory = os.path.join('videos', str(new_task.id))
            os.makedirs(upload_directory, exist_ok=True)  # Crea el directorio si no existe
            
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            new_file_name = f"original_{new_task.id}{file_extension}"
            
            file.save(os.path.join('videos/' + str(new_task.id), new_file_name))
            
            video_url = f"http://127.0.0.1:5001/videos/{str(new_task.id)}/{new_file_name}"
            
            new_task.url_video_original = video_url
            
       db.session.commit()
       
       return {
            'message': 'Tarea creada exitosamente',
            'task': {
                'id': new_task.id,
                'status': new_task.status,
                'timeStamp': new_task.timeStamp.isoformat(),
                'url_video_original': new_task.url_video_original,
                'url_video_editado': new_task.url_video_editado,
            }
        }, 200
    