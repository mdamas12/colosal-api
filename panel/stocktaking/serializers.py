from rest_framework import serializers

from panel.products.serializers import ProductMixinSerializer
from .models import *

class ProviderMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('__all__')

class PurchaseMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('__all__')

class PurshaseDetailSerializer(serializers.ModelSerializer):
    
    product = ProductMixinSerializer()
    class Meta:
        model = PurchaseDetail
        fields = ('__all__')


