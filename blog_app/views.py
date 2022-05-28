from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, mixins
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.utils import IntegrityError

from .models import Post, Subscribe
from .serializers import (PostCreateSerializer, PostSerializer, SubscribeSerializer, PostSubscribeSerializer,
                          CreateSubscribeSerializer)
from .paginations import MyPagination


class CreatePostAPIView(generics.CreateAPIView):
    """
    Create post by authorized user.
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListAllPostsAPIVew(generics.ListAPIView):
    """
    List all posts. If the user is logged in, it will return all the posts of other users.
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Post.objects.all().order_by('-created_at')
        return Post.objects.exclude(user=self.request.user.id).order_by('-created_at')


class CreateSubscribeUserAPIView(generics.CreateAPIView):
    """
    Create subscribe authorized user to another user's post.
    """
    serializer_class = CreateSubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='The id of the post to subscribe to.'),
        }))
    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.request.data.get('post'))
        if post.user == self.request.user:
            raise APIException('You are the author of this post.')
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeleteSubscribeUserAPIView(generics.GenericAPIView,
                                 mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """
    Delete or update subscribe authorized user by pk post.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, post_id: int, user):
        return get_object_or_404(Subscribe, user=user, post=post_id)

    def delete(self, request, post_id: int, *args, **kwargs):
        """
        Delete subscribe authorized user by pk post.
        Exampl url: http://127.0.0.1:8000/api/v1/subscribe/1/
        """
        subscribe = self.get_object(post_id, request.user)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema()
    def patch(self, request, *args, **kwargs):
        """
        Update subscribe authorized user by pk post.
        """
        return self.update(request, *args, **kwargs)

    def update(self, request, post_id: int, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(post_id, request.user)
        serializer = SubscribeSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ListSubscribeAPIView(generics.ListAPIView):
    """
    List subscribes by user.
    """
    serializer_class = PostSubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('readed',)

    def get_queryset(self):
        return Subscribe.objects.filter(user=self.request.user).order_by('-post__created_at')
