from flask import request
from modelos import db, User, UserSchema, Task
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from autenticador import registrar_usuario, login, validate_token
import re
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from os import environ
import requests

# Instancia del esquema
user_schema = UserSchema()
#tasks_url = 'http://tasks:5001/'
tasks_url = 'http://localhost:5001/'


def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not re.search("[A-Z]", contrasena):
        return False, "La contraseña debe tener al menos una letra mayúscula"
    if not re.search("[a-z]", contrasena):
        return False, "La contraseña debe tener al menos una letra minúscula"
    if not re.search("[0-9]", contrasena):
        return False, "La contraseña debe tener al menos un número"
    if not re.search("[@#$%^&+=-]", contrasena):
        return False, "La contraseña debe tener al menos un carácter especial (@#$%^&+=)"
    return True, None

class VistaRegistro(Resource):
    
    def post(self):
        data = request.json
        
        # Validar que no falten campos obligatorios
        if not data.get('username') or not data.get('email') or not data.get('password1') or not data.get('password2'):
            return {'mensaje': 'Faltan campos obligatorios'}, 400
        
        # Verificar si el nombre de usuario o el correo ya existen
        if User.query.filter_by(username=data['username']).first():
            return {'mensaje': 'El nombre de usuario ya está registrado'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'mensaje': 'El correo electrónico ya está registrado'}, 400
        
         # Verificar que las contraseñas coincidan
        if data['password1'] != data['password2']:
            return {'mensaje': 'Las contraseñas no coinciden'}, 400
        
        # Validar la contraseña usando la función validar_contrasena
        es_valida, error_contrasena = validar_contrasena(data['password1'])
        if not es_valida:
            return {'mensaje': error_contrasena}, 400
        
        # Crear el nuevo usuario
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password1']
        )
        
        try:
            # Guardar el nuevo usuario en la base de datos
            db.session.add(new_user)
            db.session.commit()

            # Devolver el nuevo usuario serializado
            return {'mensaje': 'Cuenta creada con éxito'}, 201
        except Exception as e:
            db.session.rollback()
            return {"mensaje": "Error al crear la cuenta", "detalles": str(e)}, 500
        
class VistaLogin(Resource):
    
    def post(self):
        
        data = request.json
        
        # Verificar si se pasaron los campos requeridos
        if not data.get('username') and not data.get('email'):
            return {'mensaje': 'Se requiere el campo username o email'}, 400
        
        if not data.get('password'):
            return {'mensaje': 'Faltan el campo password'}, 400
        
        # Buscar el usuario por nombre de usuario
        user = None
        if data.get('username'):
            user = User.query.filter_by(username=data['username']).first()
        elif data.get('email'):
            user = User.query.filter_by(email=data['email']).first()
        
        # Si el usuario no existe o la contraseña es incorrecta
        if not user or user.password != data['password']:
            return {'mensaje': 'Usuario o contraseña incorrectos'}, 401
        
        token = create_access_token(identity = user.id)
        
        return {'token': token}, 200
    
class VistaTasks(Resource):
    
    @jwt_required()
    def get(self):
        
        current_user = get_jwt_identity()
        
        params = request.args.to_dict()
        
        data = {
            'current_user': current_user
        }
        
        response = requests.get(f'{tasks_url}api/tasks', params=params, data=data)
        
        return response.json(), response.status_code
    
    @jwt_required()
    def post(self):
        
        # Verifica si se ha enviado un archivo
        if 'file' not in request.files:
            return {'message': 'Debe enviar un archivo de video'}, 400
        
        file = request.files['file']
        
        # Guarda el archivo en la carpeta 'uploads'
        #file.save(os.path.join('../uploads', file.filename))
        
        current_user = get_jwt_identity()
        data = {
            'current_user': current_user
        }
        
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(f'{tasks_url}api/tasks', files=files, data=data)
        
        return response.json(), response.status_code
        
class VistaTask(Resource):
    
    @jwt_required()
    def get(self, id_task):
        
        current_user = get_jwt_identity()
        
        data = {
            'current_user': current_user
        }
        
        response = requests.get(f'{tasks_url}api/tasks/{id_task}', data=data)
        
        return response.json(), response.status_code
    
    @jwt_required()
    def delete(self, id_task):
        
        current_user = get_jwt_identity()
        
        data = {
            'current_user': current_user
        }
        
        response = requests.delete(f'{tasks_url}api/tasks/{id_task}', data=data)
        
        return response.json(), response.status_code
    
class VistaVideos(Resource):
    
    def get(self):
        
        params = request.args.to_dict()
        
        response = requests.get(f'{tasks_url}/api/videos', params=params)
        
        return response.json(), response.status_code
        
    
       
    