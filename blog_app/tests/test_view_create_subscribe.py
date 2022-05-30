import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from blog_app.models import Post


class CreateSubscribeTest(APITestCase):
    """"
    Test module for create a new subscribe API
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
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

        users = [User(username='Test%s' % i, password='password%s' % i) for i in range(10)]


        User.objects.bulk_create(users)

        self.subscribe1 = {
            'user_to': users[0].id
        }

        self.subscribe2 = {
            'user_to': users[1].id
        }
        self.subscribe3 = {}

    def test_create_subscribe(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/subscribe/',
            data=json.dumps(self.subscribe1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_to', response.json())
        self.assertIn('user', response.json())
        self.assertEqual(response.json()['user_to'], self.subscribe1['user_to'])
        self.assertEqual(response.json()['user'], self.user.id)

        bad_response = self.client.post(
            'http://127.0.0.1:8000/api/v1/subscribe/',
            data=json.dumps(self.subscribe1),
            content_type='application/json'
        )
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(bad_response.json(), {'non_field_errors': ['The fields user, user_to must make a unique set.']})

    def test_create_subscribe_invalid(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/subscribe/',
            data=json.dumps(self.subscribe3),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_create_subscribe_not_auth(self):
        self.client.logout()
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/subscribe/',
            data=json.dumps(self.subscribe2),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
