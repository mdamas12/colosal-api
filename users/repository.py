from django.contrib.auth.models import User


class UserRepository(object):

    def create_user(self, username, email, password, is_superuser):
        return User.objects.create_user(username=username, email=email, password=password, is_superuser=is_superuser)