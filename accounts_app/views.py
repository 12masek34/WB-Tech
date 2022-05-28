from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.exceptions import APIException

from .serializers import UserSerializer, UserCountPostSerializer, UserResponseSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """
    Registers a new user.
    """
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="response description",
                schema=UserResponseSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListUsersAPIView(generics.ListAPIView):
    """
    Get all users.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCountPostSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('count_post', openapi.IN_QUERY, description='filter by count_post.',
                                             type=openapi.TYPE_NUMBER)])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):

        count_post = self.request.query_params.get('count_post')

        if count_post is None:
            return get_user_model().objects.annotate(
                count_post=Count('post')
            )
        else:
            try:
                return get_user_model().objects.annotate(
                    count_post=Count('post')
                ).filter(count_post=count_post)
            except ValueError:
                raise APIException('Parameter "count_post" must be nuber.')
