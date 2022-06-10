from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, mixins, generics
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from app.serializers import MyTokenObtainPairSerializer, UserSerializer, UserSerializerToken, UserSerializer


class UserPagination(PageNumberPagination):
    page_size = 5


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data["name"],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerToken(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        message = {'detail': 'User already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class GetUsers(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination
    serializer_class = UserSerializer

    def get(self, request):
        return self.list(request)


class GetUserDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        data = request.data
        user = self.get_object()
        user.first_name = data['name']
        user.username = data['email']
        user.is_staff = data['isAdmin']
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class UserProfile(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user1 = request.user
        user2 = User.objects.get(id=pk)
        if user1 == user2:
            serializer = UserSerializer(user1, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            message = {'detail': 'User does not have permissions'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        user.delete()
        return Response({'detail': 'User was successfully deleted'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, pk):
    user = request.user
    print('user', user)
    data = request.data
    user.username = data['email']
    user.email = data['email']
    user.first_name = data['name']
    if data['password'] != "":
        user.password = make_password(data['password'])
    user.save()
    serializer = UserSerializerToken(user, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetAllUserUpdate(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        data = request.data
        user = User.objects.get(pk=pk)
        user.email = data["email"]
        user.username = data["email"]
        user.firstname = data["name"]
        user.is_staff = data["isAdmin"]
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({'detail': 'User was successfully deleted'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def adminGetUser(request, pk):

    if request.method == "GET":
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        data = request.data
        user = User.objects.get(pk=pk)
        user.is_staff = data["isAdmin"]
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "DELETE":
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({'detail': 'User was successfully deleted'})
