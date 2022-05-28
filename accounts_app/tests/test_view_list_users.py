from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.db.models import Count

from accounts_app.serializers import UserCountPostSerializer

client = APIClient()


class GetAllUsersTest(APITestCase):
    """
    Test module for GET all users API
    """

    def setUp(self):
        User.objects.create(
            username='Test1', password='test1')
        User.objects.create(
            username='Test2', password='test2')
        User.objects.create(
            username='Test3', password='test3')
        User.objects.create(
            username='Test4', password='test4')

    def test_get_all_users(self):
        response = client.get('http://127.0.0.1:8000/api/v1/users/')
        users = User.objects.all().annotate(count_post=Count('post'))
        serializer = UserCountPostSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
