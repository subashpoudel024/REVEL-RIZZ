from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PickupLineRequestSerializer(serializers.Serializer):
    user_query = serializers.CharField()
    tones = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    attributes = serializers.ListField(
        child=serializers.CharField(), required=False
    )


class ReplyRequestSerializer(serializers.Serializer):
    image_base64 = serializers.CharField(
        help_text="Base64-encoded image containing the conversation."
    )
    tones = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of tones for generating replies, e.g., ['friendly', 'funny']"
    )


class LooksAnalyzerRequestSerializer(serializers.Serializer):
    image_base64 = serializers.CharField(
        required=False,
        help_text="Base64-encoded image for looks analysis."
    )
    user_query = serializers.CharField(
        required=False,
        help_text="Optional text query describing the user or looks."
    )