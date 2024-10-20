import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app

class TestVistaRegistro(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        return super().setUp()
    

    def test_registro_usuario_invalid0(self):

        ## Mock usuario con username invalido.
        nuevo_usuario = {
            'username': None,
            'email': self.data_factory.email(),
            'password1': '',
            'password2': '',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Faltan campos obligatorios"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Faltan campos obligatorios',
        )

    def test_registro_email_invalido(self):

        ## Mock usuario con email invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': None,
            'password1': '',
            'password2': '',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Faltan campos obligatorios"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Faltan campos obligatorios',
        )

    def test_registro_password1_invalido(self):

        ## Mock usuario con password1 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': None,
            'password2': '',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Faltan campos obligatorios"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Faltan campos obligatorios',
        )

    def test_registro_password2_invalido(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '',
            'password2': None,
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Faltan campos obligatorios"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Faltan campos obligatorios',
        )

    def test_registro_password2_invalido(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '',
            'password2': None,
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Faltan campos obligatorios"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Faltan campos obligatorios',
        )

    def test_registro_passwords_diferentes(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '12345679',
            'password2': '12345678',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "Las contraseñas no coinciden"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Las contraseñas no coinciden',
        )

    def test_registro_password_corto(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '1234567',
            'password2': '1234567',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "La contraseña debe tener al menos 8 caracteres"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'La contraseña debe tener al menos 8 caracteres',
        )

    def test_registro_password_sin_mayuscula(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '12345678',
            'password2': '12345678',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "La contraseña debe tener al menos una letra mayúscula"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'La contraseña debe tener al menos una letra mayúscula',
        )

    def test_registro_password_sin_minuscula(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '12345678A',
            'password2': '12345678A',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "La contraseña debe tener al menos una letra minúscula"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'La contraseña debe tener al menos una letra minúscula',
        )

    def test_registro_password_sin_caracter_especial(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '12345678Ab',
            'password2': '12345678Ab',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "La contraseña debe tener al menos un carácter especial (@#$%^&+=)"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'La contraseña debe tener al menos un carácter especial (@#$%^&+=)',
        )

    def test_registro_existoso(self):

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': self.data_factory.email(),
            'password1': '12345678Ab#',
            'password2': '12345678Ab#',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            201,
        )

        ## Se espera que retorne mensaje "Cuenta creada con éxito"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Cuenta creada con éxito',
        )

    def test_registro_username_existente(self):

        username = self.data_factory.user_name(),

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': username[0],
            'email': self.data_factory.email(),
            'password1': '12345678Ab#',
            'password2': '12345678Ab#',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

       

        ## Mock usuario con password2 invalido.
        nuevo_usuario_username = {
            'username': username[0],
            'email': self.data_factory.email(),
            'password1': '12345678Ab#',
            'password2': '12345678Ab#',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario_username = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario_username),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario_username = json.loads(
            solicitud_registro_usuario_username.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            201,
        )

        ## Se espera que retorne mensaje "Cuenta creada con éxito"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Cuenta creada con éxito',
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario_username.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "El nombre de usuario ya está registrado"
        self.assertEqual(
            respuesta_registro_usuario_username['mensaje'],
            'El nombre de usuario ya está registrado',
        )

    def test_registro_correo_existente(self):

        email = self.data_factory.email(),

        ## Mock usuario con password2 invalido.
        nuevo_usuario = {
            'username': self.data_factory.user_name(),
            'email': email[0],
            'password1': '12345678Ab#',
            'password2': '12345678Ab#',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario = json.loads(
            solicitud_registro_usuario.get_data()
        )

       

        ## Mock usuario con password2 invalido.
        nuevo_usuario_email = {
            'username': self.data_factory.user_name(),
            'email': email[0],
            'password1': '12345678Ab#',
            'password2': '12345678Ab#',
        }

        ## Mock peticion post para registrar usuario
        solicitud_registro_usuario_email = self.client.post(
            "/api/auth/signup",
            data=json.dumps(nuevo_usuario_email),
            headers={'Content-Type': 'application/json'}
        )

        ## Respuesta de la petición
        respuesta_registro_usuario_email = json.loads(
            solicitud_registro_usuario_email.get_data()
        )

         ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario.status_code, 
            201,
        )

        ## Se espera que retorne mensaje "Cuenta creada con éxito"
        self.assertEqual(
            respuesta_registro_usuario['mensaje'],
            'Cuenta creada con éxito',
        )

        ## Se espera que el servicio retorne código 400
        self.assertEqual(
            solicitud_registro_usuario_email.status_code, 
            400,
        )

        ## Se espera que retorne mensaje "El nombre de usuario ya está registrado"
        self.assertEqual(
            respuesta_registro_usuario_email['mensaje'],
            'El correo electrónico ya está registrado',
        )

