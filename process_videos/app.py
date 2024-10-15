from flask import Flask
from celery import Celery

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

celery = Celery(__name__, broker='redis://localhost:6379/0')




        
    
        
       