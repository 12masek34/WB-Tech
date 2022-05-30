from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Post, Subscribe


class SubscribeTest(TestCase):
    """
    Test module for Subscribe model
    """

    def setUp(self):
        users = [User(username='Test%s' % i, password='test%s' % i) for i in range(10)]
        users = User.objects.bulk_create(users)

        Subscribe.objects.create(user=users[0], user_to=users[1])
        Subscribe.objects.create(user=users[1], user_to=users[0])
        Subscribe.objects.create(user=users[2], user_to=users[1])

    def test_subscribe(self):
        subscribe1 = Subscribe.objects.first()

        self.assertIsInstance(subscribe1.user, User)
        self.assertIsInstance(subscribe1.user_to, User)
