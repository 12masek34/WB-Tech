from django.urls import path

from .views import CreatePostAPIView, ListAllPostsAPIVew, SubscribeUserAPIView

urlpatterns = [
    path('post/', CreatePostAPIView.as_view()),
    path('posts/', ListAllPostsAPIVew.as_view()),
    path('subscribe/', SubscribeUserAPIView.as_view()),
]
