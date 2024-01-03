from knox.views import LoginView as KnoxLoginView

from django.contrib.auth import login

from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from appAuth.serializers import UserSerializer, AuthSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class LoginView(KnoxLoginView):
    """
        Login view extending KnoxLoginView
        to handle login requests
    """

    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
