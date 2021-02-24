from rest_framework import serializers
from panel.products.serializers import ProductListSearchSerializer
from panel.customers.serializers import CustomerDetailSerializer
from panel.payments.serializers import listpaymentsSerializer
from .models import *

# serializador para guardar una venta
class SaleSerializer(serializers.ModelSerializer):
    customer = serializers.IntegerField(read_only=True)
    bank = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(max_digits=19, decimal_places=2, required=False) 
    status = serializers.CharField(required=False)
  

    class Meta:
        model = Sale
        fields = ('__all__')

class SaleDetailSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(read_only=True)
    sale = serializers.IntegerField(read_only=True)
    status = serializers.CharField(required=False)
    class Meta:
        model = SaleDetail
        fields = ('__all__')

class SaleDetailViewSerializer(serializers.ModelSerializer):
    product = ProductListSearchSerializer(many=False)
    #sale = SaleSerializer()

    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale_price',
            'quantity_sold',
            'amount',
            'status',
            'product',
        )


class SaleViewchSerializer(serializers.ModelSerializer):
    detail_sale = SaleDetailViewSerializer(many=True)
    customer = CustomerDetailSerializer()
    bank = listpaymentsSerializer()

    class Meta:
        model = Sale
        fields = (
            'id',
            'created',
            'customer',
            'PaymentType',
            'bank',
            'coin',
            'amount',
            'status',
            'detail_sale'

        )

