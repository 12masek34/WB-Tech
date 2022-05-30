import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Subscribe


class DeleteSubscribeTest(APITestCase):
    """
     Test module for test delte subscribe API
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

        self.user2 = User.objects.create(username='Test2', password='test2')
        user3 = User.objects.create(username='Test3', password='test3')
        self.post = Post.objects.create(title='title2', text='text2', user=self.user2)

        self.subscribe = Subscribe.objects.create(user=self.user, user_to=self.user2)
        Subscribe.objects.create(user=self.user2, user_to=user3)

    def test_delete_subscribe(self):
        id_ = self.user2.id
        response = self.client.delete(
            f'http://127.0.0.1:8000/api/v1/subscribe/{id_}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        subscribe = Subscribe.objects.filter(user_to__id=self.user2.id)
        self.assertEqual(len(subscribe), 0)
