from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)  # serializers.CharField()
    bio = serializers.CharField(allow_blank=True, required=False)  # serializers.CharField()
    profile_picture = serializers.CharField(allow_blank=True, required=False)  # serializers.CharField()
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers_count', 'following_count']

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)  # serializers.CharField()
    email = serializers.CharField(max_length=255)  # serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)  # Generate auth token for new user
        return user
