from django.urls import path

from .views import CreatePostView, ListAllPosts

urlpatterns = [
    path('post/', CreatePostView.as_view()),
    path('posts/', ListAllPosts.as_view())
]
