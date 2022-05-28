from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Post, Subscribe


class PostsTest(TestCase):
    """ Test module for Subscribe model """

    def setUp(self):
        user1 = User.objects.create(username='Test1', password='test1')
        user2 = User.objects.create(username='Test2', password='test2')

        post1 = Post.objects.create(title='title1', text='text1', user=user1)
        post2 = Post.objects.create(title='title2', text='text2', user=user2)

        Subscribe.objects.create(user=user1, post=post2)
        Subscribe.objects.create(user=user2, post=post1)

    def test_subscribe(self):
        subscribe1 = Subscribe.objects.get(id=1)
        subscribe2 = Subscribe.objects.get(id=2)

        user1 = User.objects.get(username='Test1')
        user2 = User.objects.get(username='Test2')

        post1 = Post.objects.get(title='title1')
        post2 = Post.objects.get(title='title2')

        self.assertEqual(subscribe1.user, user1)
        self.assertEqual(subscribe1.post, post2)
        self.assertFalse(subscribe1.readed)

        self.assertEqual(subscribe2.user, user2)
        self.assertEqual(subscribe2.post, post1)
        self.assertFalse(subscribe2.readed)