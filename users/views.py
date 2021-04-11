from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from users.repository import UserRepository
from users.serializers import UserSerializer
from django.contrib.auth.models import User

from users.usecases.usescases import UserFindList


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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