from celery import Celery
from modelos import db, Task
import app
import requests
from flask import current_app
from werkzeug.utils import secure_filename
import os
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import imageio
#from PIL import Image

celery_app = Celery('task', broker='redis://localhost:6379/0')

@celery_app.task(name="process.video")
def editar_video(task_id):
    print(f'task id: {task_id} queue recibida!!!!!')
    
    task = Task.query.get(task_id)
    
    if task:
        video_url = task.url_video_original
        
        filename = video_url.split("/")[-1]
        original_file_path = os.path.join(f'{current_app.config["UPLOAD_FOLDER"]}/' + str(task_id), filename)
        
        directory = os.path.dirname(original_file_path)
        if os.path.exists(directory):
            image_path = "../images/logo.png"
            video_clip = VideoFileClip(original_file_path)
            image_logo = ImageClip(image_path).set_duration(3).resize(video_clip.size)
            final_video = concatenate_videoclips([image_logo, video_clip, image_logo])
                
            new_file_name = filename.replace('original', 'edited')
            edited_file_path = os.path.join(f'{current_app.config["UPLOAD_FOLDER"]}/' + str(task_id), new_file_name)
                
            final_video.write_videofile(edited_file_path, fps=video_clip.fps, codec='libx264')
            
            task.status = "processed"
            new_video_url = f"http://127.0.0.1:5001/videos/{str(task.id)}/{new_file_name}"
            task.url_video_editado = new_video_url
            
            db.session.commit()
    
        else:
            print(f"Directorio no existe: {task_id}")
        
        
        
            
        
        
        
        
        
        
    
    
    
    
    
    