from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from users.serializers import UserSerializer, RegisterSerializer
from .repository import *
from .usecases.registerUsecase import UserRegisterUsecase
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(CreateAPIView):

    serializer_class = RegisterSerializer

    # queryset = Invitation.objects.all()

    def perform_create(self, serializer):
        data = serializer.validated_data
        usecase = UserRegisterUsecase(self.repository, data["username"], data["email"], data["password"], data["is_superuser"])
        return usecase.execute()

    @property
    def repository(self):
        return UserRepository()
