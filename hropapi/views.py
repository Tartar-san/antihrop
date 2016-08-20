from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from hropapi.models import Hrop
from hropapi.serializers import UserSerializer, HropSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HropViewSet(viewsets.ModelViewSet):
    queryset = Hrop.objects.all()
    serializer_class = HropSerializer