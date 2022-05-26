from rest_framework import serializers

from .models import Post, Subscribe


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Create post.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'user')


class PostSerializer(PostCreateSerializer):
    """
    All fields of post.
    """
    class Meta(PostCreateSerializer.Meta):
        fields = ('id',) + PostCreateSerializer.Meta.fields + ('created_at',)


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscribe
        fields = ('post', 'user')
