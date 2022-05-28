from django.contrib.auth.models import User
from django.test import TestCase


class UsersTest(TestCase):
    """
    Test module for User model
    """

    def setUp(self):
        User.objects.create_user(username='Test1', password='test1')
        User.objects.create_user(username='Test2', password='test2')

    def test_users(self):
        user1 = User.objects.get(username='Test1')
        user2 = User.objects.get(username='Test2')

        self.assertEqual(user1.username, 'Test1')
        self.assertNotEqual(user1.password, 'test1')

        self.assertEqual(user2.username, 'Test2')
        self.assertNotEqual(user2.password, 'test2')
