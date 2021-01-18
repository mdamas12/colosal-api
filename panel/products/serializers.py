from rest_framework import serializers

from panel.brands.serializers import BrandSerializer
from panel.categories.serializers import CategorySerializer
from .models import *

class ProductMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ('__all__')