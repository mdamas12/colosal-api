from rest_framework import serializers

from panel.products.serializers import ProductMixinSerializer
from panel.providers.serializers import ProviderMixinSerializer
from panel.purchases.models import *


class PurchaseMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('__all__')

class PurshaseDetailSerializer(serializers.ModelSerializer):
    
    #product = ProductMixinSerializer()
    class Meta:
        model = PurchaseDetail
        fields = ('__all__')


class PurshaseDetailCreateSerializer(serializers.ModelSerializer):
    # product = ProductMixinSerializer()
    id = serializers.IntegerField()

    class Meta:
        model = PurchaseDetail
        fields = ('id','purchase_price','purchase_quantity','purchase_Received','status')


