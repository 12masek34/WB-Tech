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


class PostSubscribeSerializer(serializers.ModelSerializer):
    """
    All subscribe by user.
    """
    post = PostSerializer(read_only=True)

    class Meta:
        model = Subscribe
        fields = ('id', 'post', 'readed')


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Subscribe by user.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscribe
        fields = ('post', 'user')
