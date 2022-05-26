from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password',)


class UserCountPostSerializer(UserSerializer):
    """
    User serializer expanded by field "count_post".
    """
    count_post = serializers.IntegerField()

    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = UserSerializer.Meta.fields + ('count_post',)
