from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.exceptions import APIException

from .serializers import UserSerializer, UserCountPostSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """
    Registers a new user.
    """
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class ListUsersAPIView(generics.ListAPIView):
    """
    Get all users.
    Filter by url parameter, example - /?count_post=1
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCountPostSerializer

    users_params = openapi.Parameter('count_post', openapi.IN_QUERY, description='filter by count_post.',
                                   type=openapi.TYPE_NUMBER)

    @swagger_auto_schema(manual_parameters=[users_params])
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
