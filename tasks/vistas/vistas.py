from flask import request, current_app, jsonify
from modelos import db, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
from werkzeug.utils import secure_filename

task_schema = TaskSchema()
    
class VistaTasks(Resource):
    
    def get(self):
        
        current_user = request.form.get('current_user')
        
        # Obtener parámetros de consulta
        max_results = request.args.get('max', type=int)  # Convertir a entero o None
        order = request.args.get('order', type=int)  # Convertir a entero o None
        
        query = Task.query.filter_by(user=current_user)
        
        #tasks = Task.query.filter_by(user=current_user).all()
        
        # Aplicar ordenamiento
        if order == 1:
            query = query.order_by(Task.id.desc())  # Descendente
        else:
            query = query.order_by(Task.id.asc())  # Ascendente
            
        # Aplicar límite si se especifica
        if max_results:
            query = query.limit(max_results)
            
        tasks = query.all()
        
        tasks_json = [
            {
                "id": task.id,
                "user": task.user,
                "timeStamp": task.timeStamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(task.timeStamp, datetime) else None,
                "status": task.status,
                "url_video_original": task.url_video_original,
                "url_video_editado": task.url_video_editado,
            }
            for task in tasks
        ]
        
        return tasks_json
    
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
    
class VistaTask(Resource):
    
    def get(self, id_task):
        task = Task.query.get(id_task)
        
        if task is None:
            return {"message": "Task no encontrada"}, 404
        
        return task_schema.dump(task), 200