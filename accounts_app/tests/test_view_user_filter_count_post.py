from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.db.models import Count

from accounts_app.serializers import UserCountPostSerializer

client = APIClient()


class GetAllUsersWithFilterTest(APITestCase):
    """
    Test module for GET all users with filter API
    """

    def setUp(self):
        users = [User(username='Test%s' % i, password='password%s' % i) for i in range(15)]
        User.objects.bulk_create(users)

    def test_get_all_users_filter_positive(self):
        response = client.get('http://127.0.0.1:8000/api/v1/users/', data={'count_post': 0})
        users = User.objects.all().annotate(count_post=Count('post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()['results'], list)
        self.assertIn('id', response.json()['results'][0])
        self.assertIn('username', response.json()['results'][0])
        self.assertIn('count_post', response.json()['results'][0])

    def test_get_all_users_with_filter_negative(self):
        response = client.get('http://127.0.0.1:8000/api/v1/users/', data={'count_post': 1})
        self.assertEqual(response.json()['results'], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
