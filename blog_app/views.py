from rest_framework import generics, permissions

from .models import Post
from .serializers import PostCreateSerializer


class CreatePostView(generics.CreateAPIView):
    """
    Create post by user.
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
