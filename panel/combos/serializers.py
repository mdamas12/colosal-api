from rest_framework import serializers
from .models import *


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class PromotionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionDetail
        fields = '__all__'
