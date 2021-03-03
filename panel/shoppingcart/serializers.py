from rest_framework import serializers

from panel.products.serializers import ProductDetailSerializer

from .models import *

class ShoppingcartSerializer(serializers.ModelSerializer):
    #customer = serializers.IntegerField(read_only=True)
    class Meta:
        model = Shoppingcart
        fields = ('__all__')

class ShoppingcartDetailSerializer(serializers.ModelSerializer):
    #customer = serializers.IntegerField(read_only=True)
    product = ProductDetailSerializer(many=False)
    class Meta:
        model = Shoppingcart
        fields = (
            'id',
            'customer',
            'product',
            'quantity',
            'amount',
            'status',

        )


class ShcCustomerSerializer(serializers.ModelSerializer):
    shoppingcart = ShoppingcartDetailSerializer(many=True)

    class Meta:
        model = Shoppingcart
        fields = (
            'id',
            'fullname',
            'shoppingcart'
        )

