from rest_auth.registration.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        #fields = '__all__'
        exclude = ('user_permissions','groups')


class RegisterSerializer(RegisterSerializer):
    is_superuser = serializers.BooleanField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    
    def save(self, validated_data):
       
        user = super(RegisterSerializer, self).save(validated_data)
        #user.password = make_password(validated_data.data["password"])
        user.first_name = validated_data.data["first_name"]
        user.is_superuser = validated_data.data["is_superuser"]
        user.save()
        return user
