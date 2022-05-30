from django.urls import path

from .views import (CreatePostAPIView, ListAllPostsAPIVew, CreateSubscribeUserAPIView,
                    DeleteSubscribeUserAPIView, ListSubscribeAPIView, MarkPostHowViewAPIView)

urlpatterns = [
    path('post/', CreatePostAPIView.as_view()),
    path('posts/', ListAllPostsAPIVew.as_view()),
    path('subscribe/', CreateSubscribeUserAPIView.as_view()),
    path('subscribe/', MarkPostHowViewAPIView.as_view()),
    path('subscribe/<int:user_to>/', DeleteSubscribeUserAPIView.as_view()),
    path('subscribers/posts/', ListSubscribeAPIView.as_view()),
]
