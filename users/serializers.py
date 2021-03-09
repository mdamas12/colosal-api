from rest_auth.registration.serializers import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        #exclude = ('password',)


class RegisterSerializer(RegisterSerializer):
    is_superuser = serializers.BooleanField()
    email = serializers.EmailField()

    def save(self, validated_data):
        user = super(RegisterSerializer, self).save(validated_data)
        #print(validated_data.data)
        user.is_superuser = validated_data.data["is_superuser"]
        user.save()
        return user
