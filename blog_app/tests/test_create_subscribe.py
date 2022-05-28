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

        users = [User(username='Test%s' % i, password='password%s' % i) for i in range(10)]

        posts = [Post(title='Test%s' % i, text='password%s' % i) for i in range(10)]

        for post in posts:
            post.user = users[posts.index(post)]

        User.objects.bulk_create(users)
        Post.objects.bulk_create(posts)


    def test_create_valid_post(self):
        response = self.client.post(
            'http://127.0.0.1:8000/api/v1/subscribe/',
            data=json.dumps(self.valid_post),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)