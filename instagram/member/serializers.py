from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from member.models import User


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
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'age',
            'token',
        )

    def get_token(self, obj):
        token = Token.objects.get_or_create(user=obj)[0].key
        return token

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("password doesn't match")
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            age=validated_data['age'],
        )

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        data = {
            'user': ret,
            'token': obj.token
        }
        return data
