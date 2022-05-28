from django.urls import path

from .views import (CreatePostAPIView, ListAllPostsAPIVew, CreateOrUpdateSubscribeUserAPIView,
                    DeleteSubscribeUserAPIView, ListSubscribeAPIView)

urlpatterns = [
    path('post/', CreatePostAPIView.as_view()),
    path('posts/', ListAllPostsAPIVew.as_view()),
    path('subscribe/', CreateOrUpdateSubscribeUserAPIView.as_view()),
    path('subscribe/<int:post_id>/', DeleteSubscribeUserAPIView.as_view()),
    path('subscribers/', ListSubscribeAPIView.as_view()),
]
