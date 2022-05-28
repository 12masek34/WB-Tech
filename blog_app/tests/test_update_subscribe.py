import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Subscribe


class UpdateSubscribeTest(APITestCase):
    """
     Test module for test update subscribe API
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


        user2 = User.objects.create(username='Test2', password='test2')

        post1 = Post.objects.create(title='title1', text='text1', user=self.user)
        post2 = Post.objects.create(title='title2', text='text2', user=user2)

        Subscribe.objects.create(user=self.user, post=post2)
        Subscribe.objects.create(user=user2, post=post1)

        self.post1 = {
            'post': 47
        }

    def test_update_subscribe(self):
        subscribe = Subscribe.objects.filter(post__id=47)
        readed = subscribe[0].readed

        response = self.client.patch(
            'http://127.0.0.1:8000/api/v1/subscribe/',
            data=json.dumps(self.post1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(readed, response.json()['readed'])
        self.assertIn('id', response.json())
        self.assertIn('post', response.json())
        self.assertIn('id', response.json()['post'])
        self.assertIn('title', response.json()['post'])
        self.assertIn('text', response.json()['post'])
        self.assertIn('user', response.json()['post'])
        self.assertIn('created_at', response.json()['post'])
        self.assertIn('user', response.json())
        self.assertIn('readed', response.json())


