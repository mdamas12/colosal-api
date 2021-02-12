from rest_framework import serializers
from .models import *


class PromotionSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(read_only=True)
    class Meta:
        model = Promotion
        fields = '__all__'

class PromotionDetailSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(read_only=True)
    class Meta:
        model = PromotionDetail
        fields = '__all__'

class PromotionDetailViewSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(read_only=True)
    class Meta:
        model = PromotionDetail
        fields = '__all__'