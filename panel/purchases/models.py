from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response

from panel.products.models import *
from panel.providers.models import * 

class Purchase(TimeStampedModel):

    COINS = Choices('USD', 'BS')

    date = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    invoice = models.TextField(null=True,blank=True)
    coin = models.CharField(max_length=20,choices=COINS,default="USD")
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self): return self.date

class PurchaseDetail(TimeStampedModel):

    #STATUS = Choices('Imcomplete', 'Complete' )

    purchase = models.ForeignKey(Purchase, related_name='PurchaseDetail', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='PurchaseProduct', on_delete=models.PROTECT)
    purchase_price = models.DecimalField(max_digits=19, decimal_places=2)
    purchase_quantity = models.IntegerField(default=0)
    purchase_Received = models.IntegerField(default=0)
    status = models.CharField(max_length=20,default="Incomplete")

    class Meta:
        verbose_name = "Detalle de producto"
        verbose_name_plural = "Detalles de productos"

    def __str__(self): return self.product