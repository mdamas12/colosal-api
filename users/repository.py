from django.contrib.auth.models import User
from django.db.models import Q


class UserRepository(object):

    def find_user(self, query):
        return User.objects.filter(Q(username__contains=query) | Q(first_name__contains=query))

    def create_user(self,data):
        return User.objects.create_user(username=data["email"], email=data["email"], password=data["password"], first_name=data["first_name"], is_superuser=data["is_superuser"]).save()
