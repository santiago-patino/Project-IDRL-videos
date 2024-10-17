import sys
import os
ruta_modelos = os.path.join(os.path.dirname(__file__), '../../modelos')
sys.path.append(ruta_modelos)

from celery import Celery
from modelos import db, Task
import app
import requests
from flask import current_app
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import imageio

celery_app = Celery('task', broker='redis://redis:6379/0')

@celery_app.task(name="process.video")
def editar_video(task_id):
    print(f'task id: {task_id} queue recibida!!!!!')
    
    task = Task.query.get(task_id)
    
    if task:
        filename = task.nombre_video
        original_file_path = os.path.join(f'{current_app.config["UPLOAD_FOLDER"]}/{str(task_id)}', filename)
        
        directory = os.path.dirname(original_file_path)
        if os.path.exists(directory):
            image_path = "../images/logo.png"
            video_clip = VideoFileClip(original_file_path)
            
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
            edited_file_path = os.path.join(f'{current_app.config["UPLOAD_FOLDER"]}/{str(task_id)}', new_file_name)
                
            final_video.write_videofile(edited_file_path, fps=cropped_video.fps, codec='libx264')
            
            task.status = "processed"
            new_video_url = f"http://127.0.0.1:5001/api/video/{str(task.id)}"
            task.url_video = new_video_url
            
            db.session.commit()
    
        else:
            print(f"Directorio no existe: {task_id}")
        
        
        
            
        
        
        
        
        
        
    
    
    
    
    
    