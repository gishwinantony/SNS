from .models import CustomUser,FriendRequests
from rest_framework import serializers
from django.contrib.auth.hashers import make_password



class UserRegister(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = ['password', 'email','name' ]
                
            def validate_email(self, value):
                if CustomUser.objects.filter(email=value).exists():
                    raise serializers.ValidationError("A user with this email already exists.")
                return value

            def create(self, validated_data):
                password = validated_data.pop('password')
                user = CustomUser(**validated_data)
                user.password=make_password(password)
                user.save()
                return user
        
class FriendRequestsSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    requested_name = serializers.CharField(source='requested.name', read_only=True)

    class Meta:
        model = FriendRequests
        fields = ['id', 'sender_name','requested_name','sender_email']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomSearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email']


class FriendSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    requested = CustomUserSerializer()

    class Meta:
        model = FriendRequests
        fields = '__all__'