from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.repository import UserRepository
from users.serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User

from users.usecases.registerUsecase import UserRegisterUsecase
from users.usecases.usescases import *
from profileUser.models import Profile

class UserSetDataView(CreateAPIView, UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        usecase = UserRegister(self.repository, serializer.data)
        return usecase.execute()

    def perform_update(self, serializer):
        if "phone" in self.request.data:
            try:
                profile = Profile.objects.get(user=serializer.instance)
                profile.phone = self.request.data["phone"]
                profile.save()
            except Profile.DoesNotExist:
                profile = Profile()
                profile.user = serializer.instance
                profile.phone = self.request.data["phone"]
                profile.save()

        serializer.instance.set_password(serializer.validated_data["password"])
        serializer.validated_data.pop("password")
        serializer.save()

    @property
    def repository(self):
        return UserRepository()


class UserFindView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        usecase = UserFindList(self.repository, query)
        return usecase.execute()

    @property
    def repository(self):
        return UserRepository()


class UserRetrieveView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  UserSetDataView,
                  viewsets.GenericViewSet):
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
