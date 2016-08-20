from django.contrib.auth.models import User

# Create your views here.
from hropapi.models import Hrop
from hropapi.serializers import UserSerializer, HropSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HropViewSet(viewsets.ModelViewSet):
    queryset = Hrop.objects.all()
    serializer_class = HropSerializer


class RegistrationsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialized = UserSerializer(data=request.data)

        if serialized.is_valid():
            serialized.create(request.data)

            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
