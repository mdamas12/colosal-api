from django.contrib.auth.models import User
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response

from panel.products.models import *
from panel.payments.models import * 
from panel.shoppingcart.models import * 

class Sale(TimeStampedModel):

    COINS = Choices('USD', 'BS')

    PaymentType = Choices('ZELLE', 'TRANSFERENCIA BS', 'TRANSFERENCIA $', 'PAGO MOVIL', 'EFECTIVO')
    description = models.TextField(null=True,blank=True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payment_type = models.CharField(max_length=20, choices=PaymentType, default="TRANSFERENCIA BS")
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, null=True)
    coin = models.CharField(max_length=20,choices=COINS,default="USD")
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    status = models.CharField(max_length=20, null=True, blank=True)
    reference = models.CharField(max_length=40, null=True, blank=True )

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self): return self.customer

class SaleDetail(TimeStampedModel):

    #STATUS = Choices('Imcomplete', 'Complete' )

    sale = models.ForeignKey(Sale, related_name='detail_sale',  on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, related_name='SaleProduct', on_delete=models.DO_NOTHING, null=True)
    promotion = models.ForeignKey(Promotion, related_name='SalePromotion',  on_delete=models.DO_NOTHING, null=True)
    sale_price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    quantity_sold = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    status = models.CharField(max_length=20,default="POR ENTREGAR", blank=True, null=True)
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de ventas"

    def __str__(self): return self.amount