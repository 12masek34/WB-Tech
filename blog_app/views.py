from rest_framework import generics, permissions
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404

from .models import Post, Subscribe
from .serializers import PostCreateSerializer, PostSerializer, SubscribeSerializer


class CreatePostAPIView(generics.CreateAPIView):
    """
    Create post by user.
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListAllPostsAPIVew(generics.ListAPIView):
    """
    List all posts other users.
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user.id).order_by('-created_at')


class SubscribeUserAPIView(generics.CreateAPIView):
    """
    Create subscribe authorized user.
    """
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.request.data.get('post'))
        if post.user == self.request.user:
            raise APIException('You are the author of this post.')
        serializer.save(user=self.request.user)
