from rest_framework import serializers
from .models import *


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class CharacteristicViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = (
            'id',
            'name',
<<<<<<< HEAD
        )
=======
        )
>>>>>>> master
