from rest_framework import serializers

from panel.products.serializers import ProductMixinSerializer
from panel.providers.serializers import ProviderMixinSerializer
from panel.purshases.models import *


class PurchaseMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('__all__')

class PurshaseDetailSerializer(serializers.ModelSerializer):
    
    #product = ProductMixinSerializer()
    class Meta:
        model = PurchaseDetail
        fields = ('__all__')


