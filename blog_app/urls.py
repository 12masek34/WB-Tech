from django.urls import path

from .views import CreatePostAPIView, ListAllPostsAPIVew, CreateSubscribeUserAPIView, DeleteSubscribeUserAPIView

urlpatterns = [
    path('post/', CreatePostAPIView.as_view()),
    path('posts/', ListAllPostsAPIVew.as_view()),
    path('subscribe/', CreateSubscribeUserAPIView.as_view()),
    path('subscribe/<int:pk>/', DeleteSubscribeUserAPIView.as_view()),
]
