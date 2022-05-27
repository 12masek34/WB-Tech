import json
from rest_framework import status
from django.test import TestCase, Client

client = Client()


class CreateNewUserTest(TestCase):
    """ Test module for inserting a new user """

    def setUp(self):
        self.valid_payload = {
            'username': 'Test1',
            'password1': 'password',
            'password2': 'password'
        }
        self.invalid_username_payload = {
            'username': '',
            'password1': 'password',
            'password2': 'password'
        }
        self.invalid_password_payload = {
            'username': '',
            'password1': 'drowssap',
            'password2': 'password'
        }

    def test_create_valid_user(self):
        response = client.post(
            'http://127.0.0.1:8000/api/v1/registration/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], self.valid_payload['username'])

    def test_create_invalid_username(self):
        response = client.post(
            'http://127.0.0.1:8000/api/v1/registration/',
            data=json.dumps(self.invalid_username_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_password(self):
        response = client.post(
            'http://127.0.0.1:8000/api/v1/registration/',
            data=json.dumps(self.invalid_password_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
