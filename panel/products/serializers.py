from rest_framework import serializers

from panel.brands.serializers import BrandSerializer, BrandDetailSerializer
from panel.categories.serializers import CategorySerializer, CategoriesDetailSerializer
from .models import *

class ProductMixinSerializer(serializers.ModelSerializer):
    category = CategoriesDetailSerializer(many=False)
    brand = BrandDetailSerializer(many=False)

    class Meta:
        model = Product
        fields = ('__all__')

class ProductDetailMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetail
        fields = ('__all__')

class ProductGalleryMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductGallery
        fields = ('__all__')


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ('__all__')

class ProductDetailSerializer(serializers.ModelSerializer):
    #purchase = PurchaseMixinSerializer()
    #purchase = serializers.IntegerField()
    category = CategoriesDetailSerializer(many=False)
    brand = BrandDetailSerializer(many=False)
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'category',
            'brand',
            'quantity',
        )