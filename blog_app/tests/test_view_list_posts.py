import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Post


class ListPostsTest(APITestCase):
    """
     Test module for test list all posts API
    """

    def setUp(self):
        self.user_id = User.objects.create_user(username='test', password='test').id
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

    def test_list_posts(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/posts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()['results'], list)
        self.assertIn('id', response.json()['results'][0])
        self.assertIn('title', response.json()['results'][0])
        self.assertIn('text', response.json()['results'][0])
        self.assertIn('user', response.json()['results'][0])
        self.assertIn('created_at', response.json()['results'][0])

    def test_list_post_ordering(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/posts/')

        posts = Post.objects.all().order_by('-created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(posts[0].id, response.json()['results'][0]['id'])
        self.assertEqual(posts[5].id, response.json()['results'][5]['id'])
        self.assertEqual(posts[9].id, response.json()['results'][9]['id'])

