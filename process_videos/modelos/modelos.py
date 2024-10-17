from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
import pytz

db = SQLAlchemy()

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', back_populates='user_data', lazy=True)
    
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeStamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50))
    nombre_video = db.Column(db.String(255), nullable=True)
    url_video = db.Column(db.String(255), nullable=True)
    user_data = db.relationship('User', back_populates='tasks')
    videos = db.relationship('Video', back_populates='task_data', lazy=True)
    
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task_data = db.relationship('Task', back_populates='videos')
    calificacion = db.Column(db.Integer, nullable=True)
    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        
class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
        
class VideoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        include_relationships = True
        load_instance = True