import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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

        Post.objects.create(title='test', text='text', user=users[0])
        Post.objects.create(title='test', text='text', user=users[1])
        Post.objects.create(title='test', text='text', user=users[2])


    def test_create_subscribe(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/posts/')

        subscribers = Subscribe.objects.filter(user=self.user)
        print(response.json())
#
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()['results'], list)
        self.assertEqual(len(response.json()['results']), len(subscribers))
        self.assertIn('id', response.json()['results'][0])
        self.assertIn('title', response.json()['results'][0])
        self.assertIn('text', response.json()['results'][0])
        self.assertIn('user', response.json()['results'][0])
        self.assertIn('created_at', response.json()['results'][0])


    def tests_subscribers_ordering(self):
        response = self.client.get(
            'http://127.0.0.1:8000/api/v1/subscribers/')

        subscribers = Subscribe.objects.filter(user=self.user).order_by('-post__created_at')

        self.assertEqual(response.json()['results'][0]['id'], subscribers[0].id)
        self.assertEqual(response.json()['results'][1]['id'], subscribers[1].id)
        self.assertEqual(response.json()['results'][2]['id'], subscribers[2].id)

#     def test_filer_list_subscribers(self):
#         response = self.client.get(
#             'http://127.0.0.1:8000/api/v1/subscribers/?readed=true')
#         subscribe = Subscribe.objects.get(user=self.user, readed=True)
#         self.assertEqual(response.json()['results'][0]['id'], subscribe.id)
#
#     def test_pagination_list_subscribers(self):
#         response = self.client.get(
#             'http://127.0.0.1:8000/api/v1/subscribers/')
#         self.assertIn('count', response.json())
#         self.assertIn('next', response.json())
#         self.assertIn('previous', response.json())
