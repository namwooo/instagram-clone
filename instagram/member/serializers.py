from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'age',
        )


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'age',
        )

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Override validate() to check if password and password confirmation match.

        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("password doesn't match")
        return data

    def create(self, validated_data):
        """
        This is the place where a new user is created.

        """
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            age=validated_data['age'],
        )

    def to_representation(self, instance):
        """
        Reformat to represent User instance.

        """
        ret = super().to_representation(instance)
        data = {
            'user': ret,
        }
        return data
