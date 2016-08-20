import fill_data
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


class HropsView(APIView):
    def get(self, request):

        queryset = Hrop.objects.filter(user=request.user)
        serializer = HropSerializer(queryset, many=True)

        # fill_data.fill(31)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = HropSerializer(data=data)

        if serializer.is_valid():
            data.update({"user": request.user})
            serializer.create(data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialized = UserSerializer(data=request.data)

        if serialized.is_valid():
            serialized.create(request.data)

            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
