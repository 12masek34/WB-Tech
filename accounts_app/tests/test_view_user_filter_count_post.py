from rest_framework import status
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db.models import Count

from accounts_app.serializers import UserCountPostSerializer

client = Client()


class GetAllUsersWithFilterTest(TestCase):
    """ Test module for GET all users with filter API """

    def setUp(self):
        User.objects.create(
            username='Test1', password='test1')
        User.objects.create(
            username='Test2', password='test2')
        User.objects.create(
            username='Test3', password='test3')
        User.objects.create(
            username='Test4', password='test4')

    def test_get_all_users_with_filter_positive(self):
        response = client.get('http://127.0.0.1:8000/api/v1/users/', data={'count_post': 0})
        users = User.objects.all().annotate(count_post=Count('post'))
        serializer = UserCountPostSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_with_filter_negative(self):
        response = client.get('http://127.0.0.1:8000/api/v1/users/', data={'count_post': 1})
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


