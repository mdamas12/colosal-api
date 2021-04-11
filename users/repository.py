from django.contrib.auth.models import User
from django.db.models import Q


class UserRepository(object):

    def find_user(self, query):
        return User.objects.filter(Q(username__contains=query) | Q(first_name__contains=query))