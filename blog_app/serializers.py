from rest_framework import serializers

from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Create post and set user field from request user.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'user')
