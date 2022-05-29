import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class CreateNewPostTest(APITestCase):
    """"
    Test module for inserting a new post API
    """

    def setUp(self):
        User.objects.create_user(username='test', password='test')
        self.client = APIClient()

        self.login = {
            'username': 'test',
            'password': 'test',
        }

        self.token = self.client.post(
            'http://127.0.0.1:8000/api/v1/token/',
            data=json.dumps(self.login),
            content_type='application/json'
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.json()['access'])

        self.valid_post = {
            'title': 'title',
            'text': 'text'
        }

        self.invalid_post1 = {
            'text': 'text'
        }

        self.invalid_post2 = {
            'title': 'title'
        }

        self.invalid_post3 = {}

    def test_create_valid_post(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/post/',
            data=json.dumps(self.valid_post),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], self.valid_post['title'])
        self.assertEqual(response.json()['text'], self.valid_post['text'])
        self.assertIsInstance(response.json()['user'], int)

    def test_create_invalid_post1(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/post/',
            data=json.dumps(self.invalid_post1),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'title': ['This field is required.']})

    def test_create_invalid_post2(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/post/',
            data=json.dumps(self.invalid_post2),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'text': ['This field is required.']})

    def test_create_invalid_post3(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/post/',
            data=json.dumps(self.invalid_post3),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'title': ['This field is required.'],
                                           'text': ['This field is required.']})

    def test_create_post_not_auth(self):
        self.client.logout()
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/post/',
            data=json.dumps(self.invalid_post1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
