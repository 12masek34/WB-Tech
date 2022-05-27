from django.contrib.auth.models import User
from django.test import TestCase


class PuppyTest(TestCase):
    """ Test module for User model """

    def setUp(self):
        User.objects.create(
            username='Test1', password='test1')
        User.objects.create(
            username='Test2', password='test2')

    def test_users(self):
        user1 = User.objects.get(username='Test1')
        user2 = User.objects.get(username='Test2')
        self.assertEqual(user1.username, 'Test1')
        self.assertEqual(user2.username, 'Test2')
