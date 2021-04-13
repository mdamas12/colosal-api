from rest_framework import serializers

from panel.products.serializers import ProductListSearchSerializer
from  users.serializers import UserSerializer

from .models import *

class ShoppingcartSerializer(serializers.ModelSerializer):
    #customer = serializers.IntegerField(read_only=True)
    #product = serializers.IntegerField(read_only=True)


    class Meta:
        model = Shoppingcart
        fields = ('__all__')

class ShoppingcartEditSerializer(serializers.ModelSerializer):
    customer = serializers.IntegerField(read_only=True)
    product = serializers.IntegerField(read_only=True)


    class Meta:
        model = Shoppingcart
        fields = ('__all__')

class ShoppingcartDetailSerializer(serializers.ModelSerializer):
    #customer = UserSerializer(many=False)
    product = ProductListSearchSerializer(many=False)
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

