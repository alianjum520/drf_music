from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = ['phone','age']




class RegisterUserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(required=True)
    password = serializers.CharField(style = {'input_type':'password'}, write_only = True,required=True,validators=[validate_password])
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only = True,required=True,)



    class Meta:

        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
            'profile',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data ['last_name'],
        )
        user.set_password(validated_data['password'])
        profile_data=UserProfile.objects.create(
            user=user,
            phone = profile_data['phone'],
            age = profile_data['age'],

            )
        user.save()

        return user



class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')