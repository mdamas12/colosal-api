from rest_framework import serializers

from profileUser.models import Profile
from users.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('__all__')
