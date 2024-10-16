from flask import request, current_app, jsonify
from modelos import db, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import shutil
from celery import Celery

celery_app = Celery('task', broker='redis://localhost:6379/0')

@celery_app.task(name="process.video")
def editar_video(task_id):
    pass

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
            upload_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], str(new_task.id))
            os.makedirs(upload_directory, exist_ok=True)  # Crea el directorio si no existe
            
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            new_file_name = f"original_{new_task.id}{file_extension}"
            
            file.save(os.path.join(f'{current_app.config["UPLOAD_FOLDER"]}/' + str(new_task.id), new_file_name))
            
            #Enviar cola
            args = (new_task.id,)
            editar_video.apply_async(args, persistent=True)
            
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
    
    def delete(self, id_task):
        task = Task.query.get(id_task)
        
        if task is None:
            return {"message": "Task no encontrada"}, 404
        
        directory_task_files = os.path.join('videos', str(task.id))
        
        if os.path.exists(directory_task_files):
            # Eliminar la carpeta y su contenido
            shutil.rmtree(directory_task_files)
            
            db.session.delete(task)
            db.session.commit()
            db.session.commit()
        else:
            return {"mensaje": "Task eliminada"}, 200
        
        return {"mensaje": "Task eliminada"}, 200
    
class VistaVideos(Resource):
    
    def get(self):
        
        editar_video.apply_async((38,), persistent=True)
        
        max_results = request.args.get('max', type=int) 
        order = request.args.get('order', type=int)
        
        query = Task.query
        
        if order == 1:
            query = query.order_by(Task.id.desc())  # Descendente
        else:
            query = query.order_by(Task.id.asc())  # Ascendente
            
        if max_results:
            query = query.limit(max_results)
            
        tasks = query.all()
        
        videos_json = [
            {
                "timeStamp": task.timeStamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(task.timeStamp, datetime) else None,
                "url_video_uploaded": task.url_video_original,
                "url_video_processed": task.url_video_editado,
            }
            for task in tasks
        ]
        
        return videos_json, 200