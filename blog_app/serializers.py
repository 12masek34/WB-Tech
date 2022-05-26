from rest_framework import serializers

from .models import Post, Subscribe


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Create post and set user field from request user.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'user')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'user')


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscribe
        fields = ('post', 'user')
