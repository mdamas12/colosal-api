from rest_framework import serializers
from panel.payments.models import *





class BankSerializer(serializers.ModelSerializer):
    
    #product = ProductMixinSerializer()
    class Meta:
        model = Bank
        fields = ('__all__')


class MethodSerializer(serializers.ModelSerializer):
    #purchase = PurchaseMixinSerializer()
    #purchase = serializers.IntegerField()
    bank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Method
        fields = ('__all__') 


class MethodDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Method
        fields = ('__all__') 

class listpaymentsSerializer(serializers.ModelSerializer):
    methods = MethodDetailSerializer(many=True)
    class Meta:
        model = Bank
        fields = (
            'id',
            'name',
            'account_owner',
            'account_number',
            'owner_id',
            'email',
            'phone',
            'currency',
            'methods',

        )
