from django.shortcuts import get_list_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post, Subscribe
from .serializers import PostCreateSerializer, PostSerializer, SubscribeSerializer
from .paginations import MyPagination


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


class CreateSubscribeUserAPIView(generics.CreateAPIView):
    """
    Create subscribe authorized user by pk post.
    """
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.request.data.get('post'))
        if post.user == self.request.user:
            raise APIException('You are the author of this post.')
        serializer.save(user=self.request.user)


class DeleteSubscribeUserAPIView(generics.GenericAPIView):
    """
    Delete subscribe authorized user by pk post.
    """
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, post_id: int, user):
        return get_object_or_404(Subscribe, user=user, post=post_id)

    def delete(self, request, post_id: int):
        subscribe = self.get_object(post_id, request.user)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSubscribeAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = MyPagination

    def get_queryset(self):
        subscribers = get_list_or_404(Subscribe.objects.order_by('-post__created_at'), user=self.request.user)
        subscribers = [subscribe.post for subscribe in subscribers]
        return subscribers
