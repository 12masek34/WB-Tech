# import json
#
# from django.contrib.auth.models import User
# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase
#
# from ..models import Post, Subscribe
#
#
# class UpdateSubscribeTest(APITestCase):
#     """
#      Test module for test update subscribe API
#     """
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='test', password='test')
#         self.client = APIClient()
#
#         self.login = {
#             'username': 'test',
#             'password': 'test',
#         }
#
#         self.token = self.client.post(
#             'http://127.0.0.1:8000/api/v1/token/',
#             data=json.dumps(self.login),
#             content_type='application/json'
#         )
#
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.json()['access'])
#
#         users = [User(username='Test%s' % i, password='test%s' % i) for i in range(10)]
#         users = User.objects.bulk_create(users)
#
#         self.subscribe = Subscribe.objects.create(user=self.user, user_to=users[1])
#         Subscribe.objects.create(user=users[1], user_to=users[2])
#
#         self.user_to = {
#             'user_to': users[1].id
#         }
#
#     def test_update_subscribe(self):
#         subscribe = Subscribe.objects.get(id=self.subscribe.id)
#         readed = subscribe.readed
#
#         response = self.client.patch(
#             'http://127.0.0.1:8000/api/v1/subscribe/',
#             data=json.dumps(self.user_to),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertNotEqual(readed, response.json()['readed'])
#         self.assertIn('id', response.json())
#         self.assertIn('post', response.json())
#         self.assertIn('id', response.json()['post'])
#         self.assertIn('title', response.json()['post'])
#         self.assertIn('text', response.json()['post'])
#         self.assertIn('user', response.json()['post'])
#         self.assertIn('created_at', response.json()['post'])
#         self.assertIn('user', response.json())
#         self.assertIn('readed', response.json())
