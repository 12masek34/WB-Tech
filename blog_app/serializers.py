from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Subscribe


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Create post.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'user')


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
        fields = ('id', 'post', 'user')

    def create(self, validated_data):
        post = validated_data.pop('post')
        instance = Subscribe.objects.create(
            post=post,
            **validated_data
        )
        return instance


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Subscribe by user.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    post = PostSerializer(read_only=True)

    class Meta:
        model = Subscribe
        fields = ('id', 'post', 'user', 'readed')

    def update(self, instance, validated_data):
        instance.readed = True
        instance.save()
        return instance


class SubscribeResponseSerializer(serializers.ModelSerializer):
    """
    only for the  openapi scheme.
    """
    class Meta:
        model = Subscribe
        fields = ('id', 'user', 'post', 'readed')


class CreateSubscribeResponseSerializer(serializers.ModelSerializer):
    """
    only for the  openapi scheme.
    """
    class Meta:
        model = Subscribe
        fields = ('id', 'post', 'user')