from django.contrib.auth.models import User
from django.db.models import Q
from profileUser.models import Profile

class UserRepository(object):

    def find_user(self, query):
        return User.objects.filter(Q(username__contains=query) | Q(first_name__contains=query))

    def create_user(self,data):
        user = User.objects.create_user(username=data["email"], email=data["email"], password=data["password"], first_name=data["first_name"], is_superuser=data["is_superuser"]).save()
        if data['phone'] is not None:
            profile = Profile()
            profile.user = user
            profile.phone = data['phone']
            profile.save()
        return user 
