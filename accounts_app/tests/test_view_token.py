import json
from rest_framework import status
from django.test import TestCase, Client
from django.contrib.auth.models import User

client = Client()


class GetTokenTest(TestCase):
    """ Test module for get token API """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

        self.valid_payload = {
            'username': 'test',
            'password': 'test',
        }
        self.invalid_password_payload = {
            'username': 'test',
            'password': 'tset',
        }
        self.invalid_username_payload = {
            'username': 'fake',
            'password': 'tset',
        }

    def test_get_token(self):
        response = client.post(
            'http://127.0.0.1:8000/api/v1/token/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test_invalid_password_get_token(self):
        response = client.post(
            'http://127.0.0.1:8000/api/v1/token/',
            data=json.dumps(self.invalid_password_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_username_get_token(self):
        response = client.post(
            'http://127.0.0.1:8000/api/v1/token/',
            data=json.dumps(self.invalid_username_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
