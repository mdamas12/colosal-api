from rest_framework import serializers

from panel.products.serializers import ProductMixinSerializer, ProductDetailSerializer
from panel.providers.serializers import ProviderMixinSerializer, ProviderDetailSerializer
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
    #purchase = PurchaseMixinSerializer()
    #purchase = serializers.IntegerField()
    purchase = serializers.IntegerField(read_only=True)

    class Meta:
        model = PurchaseDetail
        fields = ('__all__')


class PurshaseDetailCreateSendSerializer(serializers.ModelSerializer):
    #purchase = PurchaseMixinSerializer()
    #purchase = serializers.IntegerField()

    class Meta:
        model = PurchaseDetail
        fields = ('__all__')


class ListPurshaseDetailSerializer(serializers.ModelSerializer):
    #purchase = PurchaseMixinSerializer()
    #purchase = serializers.IntegerField()
    product = ProductDetailSerializer(many=False)
    #Provider = ProviderMixinSerializer(many=false)
    class Meta:
        model = PurchaseDetail
        fields = (
            'id',
            'purchase',
            'purchase_price',
            'purchase_quantity',
            'purchase_Received',
            'status',
            'product',
        )

class ListPurshaseSerializer(serializers.ModelSerializer):
    PurchaseDetail = ListPurshaseDetailSerializer(many=True)
    provider = ProviderDetailSerializer(many=False)
    class Meta:
        model = Purchase
        fields = (
            'id',
            'date',
            'description',
            'invoice',
            'coin',
            'amount',
            'provider',
            'PurchaseDetail'

        )