from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, mixins
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.db.utils import IntegrityError

from .models import Post, Subscribe
from .serializers import PostCreateSerializer, PostSerializer, SubscribeSerializer, PostSubscribeSerializer
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
        try:
            serializer.save(user=self.request.user, post=post)
        except IntegrityError:
            raise APIException('You have already subscribed to this post.')


class DeleteSubscribeUserAPIView(generics.GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """
    Delete or update subscribe authorized user by pk post.
    """
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, post_id: int, user):
        return get_object_or_404(Subscribe, user=user, post=post_id)

    def delete(self, request, post_id: int, *args, **kwargs):
        """
        Delete subscribe authorized user by pk post.
        """
        subscribe = self.get_object(post_id, request.user)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        """
        Update subscribe authorized user by pk post.
        """
        return self.update(request, *args, **kwargs)

    def update(self, request, post_id: int, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(post_id, request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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
