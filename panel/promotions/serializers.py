from rest_framework import serializers
from .models import *
from panel.products.serializers import ProductListSearchSerializer
from panel.categories.serializers import CategoriesDetailSerializer


class PromotionSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(read_only=True)
    image = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    class Meta:
        model = Promotion
        fields = '__all__'

class PromotionDetailSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(read_only=True)
    class Meta:
        model = PromotionDetail
        fields = '__all__'

class PromotionDetailViewSerializer(serializers.ModelSerializer):
    product = ProductListSearchSerializer()
    class Meta:
        model = PromotionDetail
        fields = '__all__'


class PromotionFullSerializer(serializers.ModelSerializer):
    category = CategoriesDetailSerializer(many=False)
    promotion_detail = PromotionDetailViewSerializer(many=True)
    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'description',
            'coin',
            'price',
            'quantity',
            'image',
            'category',
            'promotion_detail'
            
        )