import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..exception import APIException
from ..models import Post, Subscribe


class ListSubscribersTest(APITestCase):
    """
     Test module for test list all subscribers API
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

        users = [User(username='Test%s' % i, password='test%s' % i) for i in range(10)]
        users = User.objects.bulk_create(users)

        Subscribe.objects.create(user=self.user, user_to=users[0])
        Subscribe.objects.create(user=self.user, user_to=users[1])
        Subscribe.objects.create(user=self.user, user_to=users[2])

        posts = [Post(title='title', text='text', user=users[0]) for _ in range(15)]
        Post.objects.bulk_create(posts)

        self.post = Post.objects.create(title='test', text='text', user=users[0])
        Post.objects.create(title='test', text='text', user=users[1])
        Post.objects.create(title='test', text='text', user=users[2])

    def test_get_list_subscribers(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()['results'], list)
        self.assertIn('id', response.json()['results'][0])
        self.assertIn('title', response.json()['results'][0])
        self.assertIn('text', response.json()['results'][0])
        self.assertIn('user', response.json()['results'][0])
        self.assertIn('created_at', response.json()['results'][0])

    def test_pagination_list_subscribers(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/')

        subscribers = Subscribe.objects.filter(user=self.user)

        ids = []
        for i in subscribers:
            ids.append(i.user_to.id)

        posts = Post.objects.filter(user__in=ids).all()

        self.assertIn('count', response.json())
        self.assertIn('next', response.json())
        self.assertIn('previous', response.json())
        self.assertTrue(len(response.json()['results']), 10)

    def test_mark_readed_post(self):
        response = self.client.get(
            f'http://127.0.0.1:8000/api/v1/post/{self.post.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertIn('title', response.json())
        self.assertIn('text', response.json())
        self.assertIn('user', response.json())
        self.assertIn('created_at', response.json())

    def test_filter_by_readed_post(self):
        response1 = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/')

        self.client.get(
            f'http://127.0.0.1:8000/api/v1/post/{self.post.id}/')

        response2 = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/', {'readed': 'true'})

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.json()['count'], 1)

        response3 = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/', {'readed': 'false'})

        self.assertNotEqual(response1.json()['count'], response3.json()['count'])

    def test_error_filter_readed_post(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/', {'readed': 'some'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detail': APIException.readed_parameter}
                         )
