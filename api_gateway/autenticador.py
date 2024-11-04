import jwt
import datetime
from modelos import User, db
import re

# Clave secreta para firmar el JWT
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'

# Función para validar la contraseña
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

def registrar_usuario(data):
    # Validar los campos
    if not data.get('username') or not data.get('email') or not data.get('password1') or not data.get('password2'):
        return {'mensaje': 'Faltan campos obligatorios'}, 400

    # Verificar si el username o email ya existe
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return {'mensaje': 'El usuario o correo ya está registrado'}, 400
    
    # Verificar que las contraseñas coincidan
    if data['password1'] != data['password2']:
        return {'mensaje': 'Las contraseñas no coinciden'}, 400
    
    es_valida, error_contrasena = validar_contrasena(data['password1'])
    if not es_valida:
        return {'mensaje': error_contrasena}, 400

    # Crear el nuevo usuario
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password1']
    )

    # Guardar el usuario en la base de datos
    db.session.add(new_user)
    db.session.commit()

    return {'mensaje': 'Usuario registrado con éxito'}, 201

def login(data):
    
    # Verificar si se pasaron los campos requeridos
    if not data.get('username') or not data.get('password'):
        return {'mensaje': 'Faltan campos obligatorios'}, 400
    
    # Buscar el usuario por nombre de usuario
    user = User.query.filter_by(username=data['username']).first()
    
    # Si el usuario no existe o la contraseña es incorrecta
    if not user or user.password != data['password']:
        return {'mensaje': 'Usuario o contraseña incorrectos'}, 401
    
    
    # Crear el token JWT con una expiración de 1 hora
    token = jwt.encode({
        'userId': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return {'token': token}, 200
    
def validate_token(token):
    
    if not token:
        return {'error': 'Token are required'}, 400
    try:
        # Si logra decifrarlo, el token es correcto
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.InvalidTokenError:
        # Si falla en decifrarlo, el token ha sido adulterado
        return {'mensaje': 'Token inválido o modificado'}, 401
    