from django.contrib.auth.models import User
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


class CreateSubscribeSerializer(serializers.ModelSerializer):
    """
    Create subscribe serializer.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscribe
        fields = ('post', 'user')

    def create(self, validated_data):
        user = validated_data.pop('user')
        post = validated_data.pop('post')
        instance = Subscribe.objects.create(
            user=user,
            post=post,
            **validated_data
        )
        return instance


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Subscribe by user.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    readed = serializers.BooleanField(required=False)

    class Meta:
        model = Subscribe
        fields = ('post', 'user', 'readed')

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.post = validated_data.get('post', instance.post)
        instance.readed = True
        instance.save()
        return instance
