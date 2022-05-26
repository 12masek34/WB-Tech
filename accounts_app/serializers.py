from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data) -> UserModel:
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password',)


class UserCountPostSerializer(UserSerializer):
    """
    User serializer expanded by field "count_post".
    """
    count_post = serializers.IntegerField()

    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = UserSerializer.Meta.fields + ('count_post',)
