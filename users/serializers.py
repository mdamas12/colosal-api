from rest_auth.registration.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from profileUser.models import Profile

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    def get_phone(self, obj):
        try:
            profile = Profile.objects.get(user__id=obj.id)
            return profile.phone
        except Profile.DoesNotExist:
            return ''

    class Meta:
        model = User
        #fields = '__all__'
        exclude = ('user_permissions','groups')


class UserEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)


class RegisterSerializer(RegisterSerializer):
    is_superuser = serializers.BooleanField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    phone = serializers.SerializerMethodField()

    def get_phone(self, obj):
        try:
            profile = Profile.objects.get(user__username=obj["username"])
            return profile.phone
        except Profile.DoesNotExist:
            return ''
    
    def save(self, validated_data):
        user = super(RegisterSerializer, self).save(validated_data)
        print(user)
        if "phone" in validated_data.data:
            try:
                profile = Profile.objects.get(user=user)
                profile.phone = validated_data.data["phone"]
                profile.save()
            except Profile.DoesNotExist:
                profile = Profile()
                profile.user = user
                profile.phone = validated_data.data["phone"]
                profile.save()
        #user.password = make_password(validated_data.data["password"])
        user.first_name = validated_data.data["first_name"]
        user.is_superuser = validated_data.data["is_superuser"]
        user.save()
        return user
