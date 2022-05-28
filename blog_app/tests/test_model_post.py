import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Post


class PostsTest(TestCase):
    """
    Test module for Post model
    """

    def setUp(self):
        user1 = User.objects.create(username='Test1', password='test1')
        user2 = User.objects.create(username='Test2', password='test2')
        Post.objects.create(title='title1', text='text1', user=user1)
        Post.objects.create(title='title2', text='text2', user=user2)

    def test_posts(self):
        post1 = Post.objects.get(title='title1')
        user1 = User.objects.get(username='Test1')

        post2 = Post.objects.get(title='title2')
        user2 = User.objects.get(username='Test2')

        self.assertEqual(post1.title, 'title1')
        self.assertEqual(post1.text, 'text1')
        self.assertIsInstance(post1.created_at, datetime.datetime)
        self.assertEqual(post1.user, user1)

        self.assertEqual(post2.title, 'title2')
        self.assertEqual(post2.text, 'text2')
        self.assertIsInstance(post2.created_at, datetime.datetime)
        self.assertEqual(post2.user, user2)
