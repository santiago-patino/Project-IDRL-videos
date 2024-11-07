import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../modelos')
sys.path.append(ruta_modelos)

from flask import Flask
#from modelos import db
from os import environ
from dotenv import load_dotenv

from modelos import db, Task
import app
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import imageio
from google.cloud import storage, pubsub_v1

import threading

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask App Context
app_context = app.app_context()
app_context.push()

bucket_name = os.environ.get('BUCKET_NAME')

def editar_video(task_id):
    #task_id = message.data.decode("utf-8")
    
    print(f'task id: {task_id} queue recibida!!!!!')
    
    with current_app.app_context():
    
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

def listen_to_pubsub():
    subscriber = pubsub_v1.SubscriberClient()
    project_id = os.environ.get('GOOGLE_PROJECT')
    sub_id = os.environ.get('SUB_ID')
    subscription_path = f'projects/{project_id}/subscriptions/{sub_id}'

    def callback(message):
        try:
            with app.app_context():
                editar_video(message.data.decode("utf-8"))
            message.ack()
        except Exception as e:
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

@app.before_first_request
def start_pubsub_listener_thread():
    thread = threading.Thread(target=listen_to_pubsub)
    thread.daemon = True
    thread.start()
    print("Pub/Sub listener started in background.")

if __name__ == "__main__":
    app.run(debug=True)
    








        
    
        
       