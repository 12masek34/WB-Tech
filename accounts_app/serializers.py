from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if validated_data['password1'] == validated_data['password2']:
            return get_user_model().objects.create_user(
                username=validated_data['username'],
                password=validated_data['password1'],
            )
        raise serializers.ValidationError('field password1 must by equal password2.')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password1', 'password2')


class UserCountPostSerializer(UserSerializer):
    """
    User serializer expanded by field "count_post".
    """
    count_post = serializers.IntegerField()

    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'username', 'count_post',)


class UserResponseSerializer(serializers.ModelSerializer):
    """
     Only for the  openapi scheme.
    """
    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'username')
