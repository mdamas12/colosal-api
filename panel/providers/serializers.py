from rest_framework import serializers

from .models import *

class ProviderMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('__all__')


