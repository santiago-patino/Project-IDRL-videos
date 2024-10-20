import json
from unittest import TestCase
from unittest.mock import patch, call
from app import app, VistaTasks
from faker import Faker
import random

class TestVistaTasks(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        numero_aleatorio = random.randint(10000, 99999)
        self.data_factory.seed_instance(numero_aleatorio)
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    # @patch('requests.get')  
    # def test_usuario_sin_tasks(self, mock_get):
    #     # Preparar el comportamiento del mock
    #     mock_get.return_value.json.return_value = {"message": "No hay tasks asociadas al usuario"}
    #     mock_get.return_value.status_code = 404
        
    #     # Hacer la llamada a la API
    #     headers = {'Content-Type': 'application/json'}
    #     response = self.client.get('/api/tasks', headers=headers)

    #     # Verificar los resultados
    #     self.assertEqual(response.status_code, 404)
    #     self.assertTrue(mock_get.called)
    #     called_args = [call[0][0] for call in mock_get.call_args_list]
    #     self.assertIn('http://tasks:5001/api/tasks', called_args)

