import json
from unittest import TestCase
from unittest.mock import patch
from faker import Faker
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import app 

import random

class TestVistaTasks(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        numero_aleatorio = random.randint(10000, 99999)
        self.data_factory.seed_instance(numero_aleatorio)
        self.client = app.test_client()
        self.token = self._register_and_login()

    def _register_and_login(self):
        self.username = self.data_factory.user_name()
        print(self.username)
        self.password = self.data_factory.password(length=10, special_chars=True,digits=True)

        usuario = {
            'username': self.username,
            'email': self.data_factory.email(),
            'password1': self.password,
            'password2': self.password,
        }

        self.client.post(
            "/api/auth/signup",
            data=json.dumps(usuario),
            headers={'Content-Type': 'application/json'}
        )

        credenciales_usuario = {
            'username': self.username,
            'password': self.password,
        }

         ## Mock peticion post para registrar usuario
        solicitud_login =   solicitud_login = self.client.post(
            "/api/auth/login",
            data=json.dumps(credenciales_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_login_usuario = json.loads(
            solicitud_login.get_data()
        )

        print(respuesta_login_usuario)

        return respuesta_login_usuario['token']

    def test_peticion_sin_token(self):
        headers = {
            'Content-Type': 'application/json',
            }

        response = self.client.get('/api/tasks', headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_token_invalido(self):
        token_manipulado = self.token.replace('e', 'h')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token_manipulado}'
            }

        response = self.client.get('/api/tasks', headers=headers)

        self.assertEqual(response.status_code, 422)

    @patch('requests.get')
    def test_usuario_sin_tasks(self, mock_get):
        mock_get.return_value.json.return_value = {"message": "No hay tasks asociadas al usuario"}
        mock_get.return_value.status_code = 404


        headers = {
            'Authorization': f'Bearer {self.token}'
            }

        response = self.client.get('/api/tasks', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(mock_get.called)
        called_args = [call[0][0] for call in mock_get.call_args_list]
        self.assertIn('http://tasks:5001/api/tasks' ,called_args)

    @patch('requests.get')
    def test_usuario_con_tasks(self, mock_get):
        mock_get.return_value.json.return_value = [{
            "id": 2,
            "timeStamp": "2024-10-19T12:45:00-05:00",
            "user_id": 102,
            "status": "en progreso",
            "nombre_video": "Video de Ejemplo 2",
            "url_video": "http://localhost/5000/videos/video2",
            "calificacion": 4
         }]
        mock_get.return_value.status_code = 200


        headers = {
            'Authorization': f'Bearer {self.token}'
            }

        response = self.client.get('/api/tasks', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_get.called)
        called_args = [call[0][0] for call in mock_get.call_args_list]
        self.assertIn('http://tasks:5001/api/tasks' ,called_args)

    
    # @patch('requests.post')
    # def test_escribir_task_sin_video(self, mock_post):
    #     headers = {
    #         'Authorization': f'Bearer {self.token}'
    #         }

    #     response = self.client.get('/api/tasks', headers=headers)

    #     self.assertEqual(response.status_code, 200)

