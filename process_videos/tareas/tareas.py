import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../../modelos')
sys.path.append(ruta_modelos)

#from celery import Celery
from modelos import db, Task
import requests
from flask import current_app
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import imageio
from google.cloud import storage, pubsub_v1

#celery_app = Celery('task', broker='redis://localhost:6379/0')
bucket_name = os.environ.get('BUCKET_NAME')
subscriber = pubsub_v1.SubscriberClient()
project_id = os.environ.get('GOOGLE_PROJECT')
sub_id = os.environ.get('SUB_ID')
subscription_path = f'projects/{project_id}/subscriptions/{sub_id}'

def callback(message, app_context):
    # Usa el contexto de la aplicación Flask explícitamente
    with app_context:
        print("Mensaje recibido:", message.data.decode('utf-8'))
        editar_video(int(message.data.decode('utf-8')))
        # Procesa el mensaje como sea necesario
        message.ack()    

# @celery_app.task(name="process.video")
def editar_video(task_id):
    
    print(f'task id: {task_id} queue recibida!!!!!')
    
    task = Task.query.get(task_id)
    if task:
            filename = task.nombre_video
            original_file_path = os.path.join(str(task_id), filename)
            #original_file_path = os.path.join(f'{str(task_id)}', filename)
            #print(original_file_path)
            
            temp_path = os.path.join(f'/tmp/{str(task_id)}')
            os.makedirs(temp_path, exist_ok=True)
            path_video_download = f'{temp_path}/{filename}'
            
            download_video(original_file_path, path_video_download)
            directory = os.path.dirname(path_video_download)
            
            if os.path.exists(directory):
                image_path = "../images/logo.png"
                video_clip = VideoFileClip(path_video_download)
                
                video_aspect_ratio = 16 / 9
                video_width, video_height = video_clip.size
                new_width = video_width
                new_height = int(new_width / video_aspect_ratio)
                
                if new_height > video_height:
                    new_height = video_height
                    new_width = int(new_height * video_aspect_ratio)
                    
                cropped_video = video_clip.crop(width=new_width, height=new_height, x_center=video_width/2, y_center=video_height/2)
                
                max_duration = 20
                if cropped_video.duration > max_duration:
                    cropped_video = cropped_video.subclip(0, max_duration)
                
                image_logo = ImageClip(image_path).set_duration(3).resize(cropped_video.size)
                final_video = concatenate_videoclips([image_logo, cropped_video, image_logo])
                    
                new_file_name = f"edited_{filename}"
                edited_file_path = os.path.join(temp_path, new_file_name)
                
                final_video.write_videofile(edited_file_path, fps=cropped_video.fps, codec='libx264')
                upload_video(edited_file_path, f'{str(task.id)}/{new_file_name}');
                
                task.status = "processed"
                
                db.session.commit()
            else:
                print(f"Directorio no existe: {task_id}")
    else:
            print(f"Tarea con id {task_id} no encontrada")
    message.ack()
    
    
            
def download_video(source_blob_name, destination_file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f'videos/{source_blob_name}')

    blob.download_to_filename(destination_file_path)
    print(f'Video {source_blob_name} descargado a {destination_file_path}.')
    return True
            
def upload_video(source_file_path, destination_blob_name):

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f'videos/{destination_blob_name}')

    blob.upload_from_filename(source_file_path)
    print(f'Video {source_file_path} subido a {destination_blob_name} en el bucket {bucket_name}.')
    
    if os.path.exists(source_file_path):
        os.remove(source_file_path)
        print(f'Video {source_file_path} fue eliminado de la ruta temporal.')
    
def iniciar_suscripcion(app_context):
    
    def wrapped_callback(message):
        callback(message, app_context)
        
    # Inicia el suscriptor
    subscriber.subscribe(subscription_path, callback=wrapped_callback)
    print("Suscriptor de Pub/Sub está escuchando mensajes...")
        
#listen_to_pubsub()
    
    
    
    
    