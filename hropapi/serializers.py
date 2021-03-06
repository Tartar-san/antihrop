from django.db import models

from django.contrib.auth.models import User
from hropapi.models import Hrop
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id','username', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class HropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hrop
        fields = ('time', 'period', 'response_time', 'intensity', 'track_name', 'volume_track')

    def create(self, validated_data):
        return Hrop.objects.create(**validated_data)
