from flask import after_this_request, request, current_app, jsonify, send_from_directory
from modelos import db, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import shutil
from celery import Celery
from moviepy.editor import VideoFileClip
import shutil
import pytz
import urllib.request
from google.cloud import storage, pubsub_v1

# Lista de tipos MIME válidos para videos
ALLOWED_VIDEO_MIME_TYPES = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv']

#celery_app = Celery('task', broker='redis://' + str(os.environ.get('REDIS_SERVER')) + ':6379/0')
bucket_name = os.environ.get('BUCKET_NAME')

project_id = os.environ.get('GOOGLE_PROJECT')
topic_id = os.environ.get('TOPIC_ID')
publisher = pubsub_v1.PublisherClient()
topic_path = f'projects/{project_id}/topics/{topic_id}'

# @celery_app.task(name="process.video")
# def editar_video(task_id):
#     pass

task_schema = TaskSchema()

class VistaTasks(Resource):
    
    def get(self):
        
        current_user = request.form.get('current_user')
        
        # Obtener parámetros de consulta
        max_results = request.args.get('max', type=int)  # Convertir a entero o None
        order = request.args.get('order', type=int)  # Convertir a entero o None
        
        query = Task.query.filter_by(user_id=current_user)
        
        # Aplicar ordenamiento
        if order == 1:
            query = query.order_by(Task.id.desc())  # Descendente
        else:
            query = query.order_by(Task.id.asc())  # Ascendente
            
        # Aplicar límite si se especifica
        if max_results:
            query = query.limit(max_results)
            
        tasks = query.all()
        
        if not tasks:
            return {"message": "No hay tasks asociadas al usuario"}, 404
        
        tasks_json = [
            {
                "id": task.id,
                "timeStamp": task.timeStamp.astimezone(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(task.timeStamp, datetime) else None,
                "upload_by": { "id": task.user_data.id, "username": task.user_data.username },
                "processed": task.status == "processed",
                "nombre_archivo": task.nombre_video,
                **({"url_video": task.url_video} if task.status == "processed" else {}),
            }
            for task in tasks
        ]
        
        return tasks_json
    
    def post(self): 
        
        current_user = request.form.get('current_user')
       
        file = request.files['file']
        
        if file.mimetype not in ALLOWED_VIDEO_MIME_TYPES:
            return {"error": "Archivo invalido. Porfavor envie un archivo de video (.mp4)"}, 400
        
        new_task = Task(
            user_id=current_user,
            status='uploaded',
        )
       
        db.session.add(new_task)
        db.session.commit()
        
        temp_dir = f'/tmp/{new_task.id}'
        temp_file_path = os.path.join(temp_dir, secure_filename(file.filename))
        os.makedirs(temp_dir, exist_ok=True)
        file.save(temp_file_path)
        
        try:
            with VideoFileClip(temp_file_path) as video:
                duration = video.duration  # Duración en segundos
                
            if duration < 20 or duration > 60:
                os.remove(temp_file_path)  # Elimina el archivo si no cumple con las condiciones
                return {'error': 'Video debe tener una duracion minima de 20 segundos y maxima de 60'}, 400
            
        except Exception as e:
             if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                return {'error': str(e)}, 400  
            
        filename = secure_filename(file.filename)
            
        upload_video(temp_file_path, f'{str(new_task.id)}/{filename}');
            
        new_task.nombre_video = filename
        db.session.commit()
        
        #Enviar cola
        publish_task(new_task.id)
        
        web_layer_url = os.environ.get('CLOUD_RUN_WEB')
        new_video_url = web_layer_url +"/api/video/"+str(new_task.id)
        new_task.url_video = new_video_url
        db.session.commit()
    
        return {
            'message': f'Tarea {new_task.id} creada exitosamente',
        }, 200
    
class VistaTask(Resource):
    
    def get(self, id_task):
        
        current_user = request.form.get('current_user')
        
        task = Task.query.filter_by(id=id_task).first()
        
        if not task:
            return {"message": "Task no encontrada"}, 404
        
        if str(task.user_id) != str(current_user):
            return {"message": "No tienes permisos para ver esta Task"}, 401
        
        task_json = {
            "id": task.id,
            "timeStamp": task.timeStamp.astimezone(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(task.timeStamp, datetime) else None,
            "upload_by": {
                "id": task.user_data.id,
                "username": task.user_data.username
            },
            "processed": task.status == "processed",
            "nombre_archivo": task.nombre_video,
            **({"url_video": task.url_video} if task.status == "processed" else {}),
        }
        
        return task_json
    
    def delete(self, id_task):
        
        current_user = request.form.get('current_user')
        
        task = Task.query.get(id_task)
        
        if task is None:
            return {"message": "Task no encontrada"}, 404
        
        if str(task.user_id) != str(current_user):
            return {"message": "No tienes permisos para eliminar esta Task"}, 401
        
        if task.status == "processed":
            db.session.delete(task)
            db.session.commit()
                
            try:
               delete_video(str(task.id))
               return {"mensaje": f"Task {task.id} eliminada"}, 200
            except Exception as e:
               print(e)
               return {"mensaje": f"No se encontró el video en el bucket para la tarea {task.id}."}, 404 
           
        else:
            return {"mensaje": f"Task {task.id} aun no ha sido procesada"}, 200
        
        
    
class VistaVideos(Resource):
    
    def get(self):
        
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
        
        if not tasks:
            return {"mensaje": "No hay videos almacenados"}, 404
        
        videos_json = [
            {
                "id": task.id,
                "upload_by": { "id": task.user_data.id, "username": task.user_data.username },
                "timeStamp": task.timeStamp.astimezone(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(task.timeStamp, datetime) else None,
                "status": task.status,
                "nombre_video": task.nombre_video,
                **({"url_video": task.url_video} if task.status == "processed" else {}),
                "calificacion": task.calificacion,
            }
            for task in tasks
        ]
        return videos_json, 200
    
class VistaVideo(Resource):
    
    def get(self, id_task):
        task = Task.query.get(id_task)
        
        if task is None:
            return {"message": "Video no encontrado"}, 404
        
        filename = f"edited_{task.nombre_video}"
        
        temp_path = f'/tmp/{str(task.id)}'
        os.makedirs(temp_path, exist_ok=True)
        path_video_download = f'{temp_path}/{filename}'
        
        download_video(f'{task.id}/{filename}', path_video_download)
        
        if os.path.exists(path_video_download):
            
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(path_video_download)
                    print(f"Archivo {filename} eliminado después de la descarga.")
                except Exception as e:
                    print(f"Error al eliminar el archivo {filename}: {e}")
                return response
            
            return send_from_directory(temp_path, filename)
        
        else:
            return jsonify({"mensaje": f"El archivo de video no se encontró o no ha sido procesado para la tarea '{id_task}'."}), 404
        
def obtener_ip_externa():
    try:
        # URL de los metadatos de GCP para la IP externa
        url = "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip"
        
        # Necesario agregar este encabezado para acceder a los metadatos
        headers = {"Metadata-Flavor": "Google"}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            ip_externa = response.read().decode('utf-8').strip()
            return ip_externa
    except Exception as e:
        return None

def upload_video(source_file_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f'videos/{destination_blob_name}')

    blob.upload_from_filename(source_file_path)
    print(f'Video {source_file_path} subido a {destination_blob_name} en el bucket {bucket_name}.')
    
    if os.path.exists(source_file_path):
        os.remove(source_file_path)
        print(f'Video {source_file_path} fue eliminado de la ruta temporal.')
    
def download_video(source_blob_name, destination_file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f'videos/{source_blob_name}')

    blob.download_to_filename(destination_file_path)
    print(f'Video {source_blob_name} descargado a {destination_file_path}.')
    
def delete_video(id_task):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    #blob = bucket.blob(f'videos/{id_task}/')
    blobs = bucket.list_blobs(prefix=f'videos/{id_task}/')
    
    num_deleted = 0
    
    for blob in blobs:
        blob.delete()
        print(f'Archivo {blob.name} eliminado del bucket {bucket_name}.')
        num_deleted += 1
    
    print(f'Se eliminaron {num_deleted} archivos del directorio "videos/{id_task}/" en el bucket {bucket_name}.')
    
def publish_task(task_id):
    # Publica el mensaje con el ID de la tarea
    data = str(task_id).encode("utf-8")
    future = publisher.publish(topic_path, data)
    
    try:
        message_id = future.result()  # Espera a que se complete la publicación
        print(f"Mensaje publicado exitosamente con ID: {message_id}")
    except Exception as e:
        print(f"Ocurrió un error al publicar el mensaje: {e}")