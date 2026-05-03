from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from typing import Any





class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email = validated_data.get('email', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        write_only=True,
        max_length=30,
        trim_whitespace=True
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        max_length=30,
        trim_whitespace=True
    )

    def validate(self, attrs: dict[str, str]) -> dict[str, Any]:
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                {
                "message": "Must include both username and password to log in. "
                }
            )
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                {
                "message": "Invalid username or password."
                }
            )
        attrs['user'] = user
        return attrs
