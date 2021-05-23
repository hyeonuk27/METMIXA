from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # image = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname',)
        # read_only_fields = ('image',)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('nickname', 'image',)
