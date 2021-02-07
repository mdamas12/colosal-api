from rest_auth.registration.serializers import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(RegisterSerializer):
    is_staff = serializers.BooleanField()
    email = serializers.EmailField()

    def save(self, validated_data):
        user = super(RegisterSerializer, self).save(validated_data)
        print(validated_data.data)
        user.is_staff = validated_data.data["is_staff"]
        user.save()
        return user
