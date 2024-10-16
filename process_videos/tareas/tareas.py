from celery import Celery
from flask import current_app
import redis

app = Celery('task', broker='redis://localhost:6379/0')

@app.task(name="process.video")
def editar_video(task_id):
    print('task queue recibida!!!!!')
    print(task_id)
    