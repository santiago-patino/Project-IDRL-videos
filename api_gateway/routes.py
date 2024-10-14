from flask import Blueprint, request, jsonify
from autenticador import registrar_usuario, login, validate_token

# Crea un Blueprint para las rutas
routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def register_route():
    data = request.get_json()
    response, status_code = registrar_usuario(data)
    return jsonify(response), status_code

@routes.route('/login', methods=['POST'])
def login_route():
    user_data = request.get_json()
    response, status_code = login(user_data)
    return jsonify(response), status_code

@routes.route('/upload', methods=['POST'])
def upload_video():
    auth_header = request.headers.get('Authorization')
    if validate_token(auth_header):
        # Simula el envío de información
        incidentes = [
            {
                "id": 1,
                "tipo": "Queja",
                "descripcion": "Mala experiencia con el soporte técnico.",
                "estado": "Resuelto"
            },
            {
                "id": 2,
                "tipo": "Consulta",
                "descripcion": "Información sobre la garantía del producto.",
                "estado": "Cerrado"
            }
        ]
        return jsonify(incidentes), 200
    else:
        response, status_code = validate_token(auth_header)
        return jsonify(response), status_code