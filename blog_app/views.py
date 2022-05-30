from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, permissions, status, mixins
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post, Subscribe, CheckPost
from .serializers import (PostCreateSerializer, PostSerializer, SubscribeSerializer, PostSubscribeSerializer,
                          CreateSubscribeSerializer, CreateSubscribeResponseSerializer)
from .paginations import MyPagination


class CreatePostAPIView(generics.CreateAPIView):
    """
    Create new post.\n
    Create post by authorized user.
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_INTEGER,
                                    description='type: string, title: Title, maxLength: 250, minLength: 1'),
            'text': openapi.Schema(type=openapi.TYPE_INTEGER, description='type: string, title: Text, minLength: 1'),
        }), responses={
        status.HTTP_200_OK: openapi.Response(
            description="Return all fields created post.",
            schema=PostCreateSerializer,
        )
    })
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAllPostsAPIVew(generics.ListAPIView):
    """
    List all posts.\n
    List all posts. If the user is logged in, it will return all the posts of other users.
    Sort by post creation date, fresh first.
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Post.objects.all().order_by('-created_at')
        return Post.objects.exclude(user=self.request.user.id).order_by('-created_at')


class CreateSubscribeUserAPIView(generics.CreateAPIView):
    """
    Create new subscribe.\n
    Create subscribe authorized user to another user's post.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSubscribeSerializer
        # if self.request.method == 'PATCH':
        #     return SubscribeSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_to': openapi.Schema(type=openapi.TYPE_INTEGER),
        }), responses={
        status.HTTP_200_OK: openapi.Response(
            description="Return id subscribe, post and user.",
            schema=CreateSubscribeResponseSerializer,
        )
    })
    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_to = get_object_or_404(get_user_model(), id=self.request.data.get('user_to'))
        if user_to == self.request.user:
            raise APIException('Do you want to subscribe to yourself.')
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    #
    # @swagger_auto_schema(request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     properties={
    #         'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id of the selected post'),
    #     }),
    #     responses={
    #         status.HTTP_200_OK: openapi.Response(
    #             description="response description",
    #             schema=SubscribeSerializer,
    #         )
    #     }
    # )
    # def patch(self, request, *args, **kwargs):
    #     """
    #     Marks the post as read.\n
    #     Update subscribe authorized user by pk post.
    #     """
    #     return self.update(request, *args, **kwargs)
    #
    # def get_object(self, post_id: int, user):
    #     return get_object_or_404(Subscribe, user=user, post=post_id)
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object(request.data.get('post'), request.user)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class DeleteSubscribeUserAPIView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    Delete subscribe authorized user by pk post.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, user_to: int, user):
        return get_object_or_404(Subscribe, user=user, user_to=user_to)

    def delete(self, request, user_to: int, *args, **kwargs):
        """
        Delete subscribe.\n
        Delete subscribe authorized user by pk post in url parameter.
        Example url: http://127.0.0.1:8000/api/v1/subscribe/1/
        """
        subscribe = self.get_object(user_to, request.user)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSubscribeAPIView(generics.ListAPIView):
    """
    All posts from subscribers' feed\n
    List subscribes by user.Sort by post creation date, fresh first.
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend,)

    # filterset_fields = ('readed',)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('readed', openapi.IN_QUERY, description='filter by readed.',
                                             type=openapi.TYPE_BOOLEAN)])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        subscibers = Subscribe.objects.filter(user=self.request.user).select_related('user_to')
        subscribe_user_id = []
        for sub in subscibers:
            subscribe_user_id.append(sub.user_to.id)

        posts = Post.objects.filter(user__id__in=subscribe_user_id).order_by('-created_at')
        return posts


class MarkPostHowViewAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated,)

    # @swagger_auto_schema(request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     properties={
    #         'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id of the selected post'),
    #     }),
    #     responses={
    #         status.HTTP_200_OK: openapi.Response(
    #             description="response description",
    #             schema=SubscribeSerializer,
    #         )
    #     }
    # )
    def patch(self, request, *args, **kwargs):
        """
        Marks the post as read.\n
        Update subscribe authorized user by pk post.
        """
        return self.update(request, *args, **kwargs)

    def get_object(self, post_id: int, user):
        return get_object_or_404(CheckPost, post=post_id, user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(request.data.get('post'), request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

        # users_to = [user.user_to.id for user in subscibers]
        # posts = Post.objects.filter(user__in=users_to).order_by('-created_at')
        # return posts

        # return Post.objects.filter(user=self.request.user).order_by('-user_to__created_at')
