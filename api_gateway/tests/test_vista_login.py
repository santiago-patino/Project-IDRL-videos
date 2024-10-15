import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app

class TestVistaLogin(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        self.username = self.data_factory.user_name()[0]
        self.password = self.data_factory.password(length=10, special_chars=True,digits=True)

         ## Mock usuario con username invalido.
        nuevo_usuario = {
            'username': self.username,
            'email': self.data_factory.email(),
            'password1': self.password,
            'password2': self.password,
        }


         ## Mock peticion post para registrar usuario
        self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        return super().setUp()
     
    def test_login_username_invalido(self):
        ## Mock credenciales de acceso.
        credenciales_usuario = {
            'username': None,
            'password': self.password,
        }

        ## Mock peticion post para registrar usuario
        solicitud_login = self.client.post(
            "/api/auth/login",
            data=json.dumps(credenciales_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_login_usuario = json.loads(
            solicitud_login.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_login.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Falta el campo username"
        self.assertEqual(
            respuesta_login_usuario['mensaje'],
            'Falta el campo username',
        )

    def test_login_password_invalido(self):
        ## Mock credenciales de acceso.
        credenciales_usuario = {
            'username': self.username,
            'password': None,
        }

        ## Mock peticion post para registrar usuario
        solicitud_login = self.client.post(
            "/api/auth/login",
            data=json.dumps(credenciales_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_login_usuario = json.loads(
            solicitud_login.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_login.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Faltan el campo password"
        self.assertEqual(
            respuesta_login_usuario['mensaje'],
            'Faltan el campo password',
        )

    def test_login_username_no_existe(self):
        ## Mock credenciales de acceso.
        credenciales_usuario = {
            'username': self.data_factory.user_name()[1],
            'password': self.password,
        }

        ## Mock peticion post para registrar usuario
        solicitud_login = self.client.post(
            "/api/auth/login",
            data=json.dumps(credenciales_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_login_usuario = json.loads(
            solicitud_login.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_login.status_code, 
            401,
        )

        ## Se espera que retorne mensaje "Usuario o contraseña incorrectos"
        self.assertEqual(
            respuesta_login_usuario['mensaje'],
            'Usuario o contraseña incorrectos',
        )
    
    def test_login_password_incorrecto(self):
        ## Mock credenciales de acceso.
        credenciales_usuario = {
            'username': self.username,
            'password': self.data_factory.password(length=10, special_chars=True,digits=True)[1],
        }

        ## Mock peticion post para registrar usuario
        solicitud_login = self.client.post(
            "/api/auth/login",
            data=json.dumps(credenciales_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_login_usuario = json.loads(
            solicitud_login.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_login.status_code, 
            401,
        )

        ## Se espera que retorne mensaje "Usuario o contraseña incorrectos"
        self.assertEqual(
            respuesta_login_usuario['mensaje'],
            'Usuario o contraseña incorrectos',
        )

    def test_login_exitoso(self):
        ## Mock credenciales de acceso.
        credenciales_usuario = {
            'username': self.username,
            'password': self.password,
        }

        ## Mock peticion post para registrar usuario
        solicitud_login = self.client.post(
            "/api/auth/login",
            data=json.dumps(credenciales_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_login_usuario = json.loads(
            solicitud_login.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_login.status_code, 
            200,
        )

        ## Se espera que retorne mensaje con el token de sesión
        self.assertIsNotNone(
            respuesta_login_usuario['token'],
        )



